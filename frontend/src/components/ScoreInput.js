import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { UNIVERSAL_NATURAL_CLUSTERS, UNIVERSAL_HUMAN_CLUSTERS } from '../data/constants';

function ScoreInput({ selectedUniv, selectedDivision, deptName, scores, onDeptNameChange, onScoreChange, onBack, onPredict, loading }) {
  const [examType, setExamType] = useState(null);
  const [validationError, setValidationError] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  // 서울시립대 확인용
  const isUOS = () => {
    if (!selectedUniv || !selectedUniv.name) return false;
    return selectedUniv.name.includes('서울시립'); 
  };

  useEffect(() => {
    if (selectedUniv && selectedDivision) {
      // 🚨 [수정됨] 서울시립대 로직 (인문=영어만, 자연=수학만)
      if (isUOS()) {
        if (selectedDivision === 'Humanities') {
          setExamType('ENG_ONLY'); // 인문: 영어 필기 100%
        } else {
          setExamType('MATH_ONLY'); // 자연: 수학 필기 100%
        }
        return;
      }

      const examInfo = selectedUniv.exam_info?.[selectedDivision];
      if (examInfo) {
        setExamType(examInfo.subjects);
      } else {
        const examTypeKey = selectedDivision === 'Natural' ? 'exam_type_natural' : 'exam_type_humanities';
        setExamType(selectedUniv[examTypeKey]);
      }
    }
  }, [selectedUniv, selectedDivision]);

  const handleScoreChange = (subject, value) => {
    if (value && (parseFloat(value) < 0 || parseFloat(value) > 100)) {
      setValidationError('점수는 0~100 범위여야 합니다');
      return;
    }
    setValidationError('');
    
    onScoreChange({
      ...scores,
      [subject]: value
    });
  };

  const handleSimulation = () => {
    const isHumanities = selectedDivision === 'Humanities';
    const simulationScores = {
      eng: isHumanities ? '80' : '70',
      math: isHumanities ? '' : '70'
    };
    
    onScoreChange(simulationScores);
    alert('가상 점수(평균)가 입력되었습니다.');
  };

  // 상단 안내 박스 문구 설정
  const getExamTypeInfo = () => {
    if (isUOS()) {
        if (selectedDivision === 'Humanities') {
            return {
                title: '2단계 전공영어 점수 입력',
                description: '1단계 공인영어 통과 후, 2단계 필기 점수를 입력하세요.',
                color: '#2196f3',
                bgColor: '#e3f2fd'
            };
        } else {
            return {
                title: '2단계 전공수학 점수 입력',
                description: '1단계 공인영어 통과 후, 2단계 필기 점수를 입력하세요.',
                color: '#ff9800',
                bgColor: '#fff3e0'
            };
        }
    }

    if (examType === 'Math Only' || examType === 'MATH_ONLY') {
      return {
        title: '수학 기출 점수 입력 (영어 반영 X)',
        description: '이 대학은 수학 100% 전형입니다',
        color: '#ff9800',
        bgColor: '#fff3e0'
      };
    } else if (examType === 'English Only' || examType === 'ENG_ONLY') {
      return {
        title: '영어 기출 점수 입력 (수학 반영 X)',
        description: '이 대학은 영어 100% 전형입니다',
        color: '#2196f3',
        bgColor: '#e3f2fd'
      };
    } else {
      return {
        title: '영어 + 수학 기출 점수 입력',
        description: '이 대학은 영어+수학 종합 전형입니다',
        color: '#4caf50',
        bgColor: '#e8f5e8'
      };
    }
  };

  const isValid = () => {
    if (!selectedCategory) return false;
    if (validationError) return false;
    
    // [수정됨] 서울시립대 유효성 검사
    if (isUOS()) {
       if (selectedDivision === 'Humanities') {
         return scores.eng && parseFloat(scores.eng) >= 0 && parseFloat(scores.eng) <= 100;
       } else {
         return scores.math && parseFloat(scores.math) >= 0 && parseFloat(scores.math) <= 100;
       }
    }

    const examInfo = selectedUniv?.exam_info?.[selectedDivision];
    if (examInfo) {
      if (!examInfo.has_eng && examInfo.has_math) {
        return scores.math && parseFloat(scores.math) >= 0 && parseFloat(scores.math) <= 100;
      } else if (examInfo.has_eng && !examInfo.has_math) {
        return scores.eng && parseFloat(scores.eng) >= 0 && parseFloat(scores.eng) <= 100;
      } else if (examInfo.has_eng && examInfo.has_math) {
        return scores.eng && scores.math && 
               parseFloat(scores.eng) >= 0 && parseFloat(scores.eng) <= 100 &&
               parseFloat(scores.math) >= 0 && parseFloat(scores.math) <= 100;
      }
    } else {
      if (examType === 'MATH_ONLY') {
        return scores.math && parseFloat(scores.math) >= 0 && parseFloat(scores.math) <= 100;
      } else if (examType === 'ENG_ONLY') {
        return scores.eng && parseFloat(scores.eng) >= 0 && parseFloat(scores.eng) <= 100;
      } else {
        return scores.eng && scores.math && 
               parseFloat(scores.eng) >= 0 && parseFloat(scores.eng) <= 100 &&
               parseFloat(scores.math) >= 0 && parseFloat(scores.math) <= 100;
      }
    }
    return false;
  };

  const handlePredict = () => {
    const requestData = {
      university_name: selectedUniv.name,
      dept_name: deptName || '',
      user_division: selectedDivision,
      category_code: selectedCategory,
      score_eng: 0,
      score_math: 0
    };

    // [수정됨] 서울시립대 전송 데이터 처리
    if (isUOS()) {
      if (selectedDivision === 'Humanities') {
        requestData.score_eng = parseFloat(scores.eng) || 0;
      } else {
        requestData.score_math = parseFloat(scores.math) || 0;
      }
    } 
    else {
      const examInfo = selectedUniv?.exam_info?.[selectedDivision];
      if (examInfo) {
        if (examInfo.has_eng) requestData.score_eng = parseFloat(scores.eng) || 0;
        if (examInfo.has_math) requestData.score_math = parseFloat(scores.math) || 0;
      } else {
        if (examType === 'MATH_ONLY') {
          requestData.score_math = parseFloat(scores.math) || 0;
        } else if (examType === 'ENG_ONLY') {
          requestData.score_eng = parseFloat(scores.eng) || 0;
        } else {
          requestData.score_eng = parseFloat(scores.eng) || 0;
          requestData.score_math = parseFloat(scores.math) || 0;
        }
      }
    }

    onPredict(requestData);
  };

  const examInfoDisplay = getExamTypeInfo();

  return (
    <motion.div 
      className="card"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="step-indicator">
        <div className="step completed">1</div>
        <div className="step active">2</div>
        <div className="step inactive">3</div>
      </div>

      <h2 style={{ textAlign: 'center', marginBottom: '1rem', color: '#495057' }}>
        점수 입력 <span style={{color: 'red', fontSize:'0.8em'}}>🔴</span>
      </h2>

      <div style={{ 
        background: examInfoDisplay.bgColor,
        border: `2px solid ${examInfoDisplay.color}`,
        padding: '1.5rem', 
        borderRadius: '12px', 
        marginBottom: '2rem',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '1.1rem', fontWeight: '700', color: examInfoDisplay.color, marginBottom: '0.5rem' }}>
          {examInfoDisplay.title}
        </div>
        <div style={{ fontSize: '0.95rem', color: '#666' }}>
          {selectedUniv?.name} - {selectedDivision === 'Natural' ? '자연계열' : '인문계열'}
        </div>
        <div style={{ fontSize: '0.9rem', color: '#888', marginTop: '0.5rem' }}>
          {examInfoDisplay.description}
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">지원 모집 단위(학과 군) 선택 *</label>
        <select
          className="form-input"
          value={selectedCategory}
          onChange={(e) => {
            setSelectedCategory(e.target.value);
            const selectedOption = selectedDivision === 'Natural' 
              ? UNIVERSAL_NATURAL_CLUSTERS.find(item => item.value === e.target.value)
              : UNIVERSAL_HUMAN_CLUSTERS.find(item => item.value === e.target.value);
            onDeptNameChange(selectedOption?.label || e.target.value);
          }}
          style={{ fontSize: '1rem', padding: '12px' }}
        >
          <option value="">모집 단위를 선택하세요</option>
          {selectedDivision === 'Natural' 
            ? UNIVERSAL_NATURAL_CLUSTERS.map(cluster => (
                <option key={cluster.value} value={cluster.value}>
                  {cluster.label}
                </option>
              ))
            : UNIVERSAL_HUMAN_CLUSTERS.map(cluster => (
                <option key={cluster.value} value={cluster.value}>
                  {cluster.label}
                </option>
              ))
          }
        </select>
      </div>

      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <button
          type="button"
          onClick={handleSimulation}
          style={{
            background: '#6c757d',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '20px',
            fontSize: '0.85rem',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
          onMouseOver={(e) => e.target.style.background = '#5a6268'}
          onMouseOut={(e) => e.target.style.background = '#6c757d'}
        >
          🎲 점수가 없다면? 합격자 평균으로 시뮬레이션
        </button>
      </div>

      <div style={{ 
        background: '#f8f9fa', 
        border: '1px solid #dee2e6',
        padding: '1rem', 
        borderRadius: '8px', 
        marginBottom: '1.5rem',
        textAlign: 'center'
      }}>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#495057', fontWeight: '500' }}>
          본인의 기출 최고 점수(Career High)를 입력하세요
        </p>
      </div>

      {/* 영어 점수: 시립대 인문계열 또는 원래 영어 있는 경우 */}
      {((selectedUniv?.exam_info?.[selectedDivision]?.has_eng) || 
        (examType === 'ENG_ONLY' || examType === 'ENG_MATH') || 
        (isUOS() && selectedDivision === 'Humanities')) && (
        <div className="form-group">
          <label className="form-label">영어 점수 *</label>
          <input
            type="number"
            className="form-input"
            placeholder="영어 점수 (0-100)"
            value={scores.eng}
            onChange={(e) => handleScoreChange('eng', e.target.value)}
            disabled={!isUOS() && selectedUniv?.exam_info?.[selectedDivision]?.has_eng === false}
            min="0"
            max="100"
            step="1"
            style={{ 
              fontSize: '1.1rem', 
              padding: '12px', 
              textAlign: 'center',
              backgroundColor: (!isUOS() && selectedUniv?.exam_info?.[selectedDivision]?.has_eng === false) ? '#f5f5f5' : 'white',
              color: (!isUOS() && selectedUniv?.exam_info?.[selectedDivision]?.has_eng === false) ? '#999' : 'inherit'
            }}
          />
        </div>
      )}

      {/* 수학 점수: 시립대 자연계열 또는 원래 수학 있는 경우 */}
      {((selectedUniv?.exam_info?.[selectedDivision]?.has_math) || 
        (examType === 'MATH_ONLY' || examType === 'ENG_MATH') || 
        (isUOS() && selectedDivision === 'Natural')) && (
        <div className="form-group">
          <label className="form-label">수학 점수 *</label>
          <input
            type="number"
            className="form-input"
            placeholder="수학 점수 (0-100)"
            value={scores.math}
            onChange={(e) => handleScoreChange('math', e.target.value)}
            disabled={!isUOS() && selectedUniv?.exam_info?.[selectedDivision]?.has_math === false}
            min="0"
            max="100"
            step="1"
            style={{ 
              fontSize: '1.1rem', 
              padding: '12px', 
              textAlign: 'center',
              backgroundColor: (!isUOS() && selectedUniv?.exam_info?.[selectedDivision]?.has_math === false) ? '#f5f5f5' : 'white',
              color: (!isUOS() && selectedUniv?.exam_info?.[selectedDivision]?.has_math === false) ? '#999' : 'inherit'
            }}
          />
        </div>
      )}

      {validationError && (
        <div style={{ 
          color: '#dc3545', 
          textAlign: 'center', 
          marginBottom: '1rem', 
          fontSize: '0.9rem',
          fontWeight: '600',
          background: '#f8d7da',
          padding: '8px',
          borderRadius: '6px'
        }}>
          {validationError}
        </div>
      )}

      <div style={{ 
        display: 'flex', 
        gap: '1rem', 
        justifyContent: 'center', 
        marginTop: '2rem' 
      }}>
        <button 
          className="btn btn-secondary"
          onClick={onBack}
          disabled={loading}
          style={{ padding: '12px 24px', fontSize: '1rem' }}
        >
          이전
        </button>
        
        <button 
          className="btn btn-primary"
          onClick={handlePredict}
          disabled={!isValid() || loading}
          style={{ padding: '12px 32px', fontSize: '1rem', fontWeight: '600' }}
        >
          {loading ? (
            <>
              <div className="loading-spinner"></div>
              분석 중...
            </>
          ) : (
            '합격 가능성 분석'
          )}
        </button>
      </div>

      {!isValid() && !validationError && (
        <p style={{ 
          textAlign: 'center', 
          color: '#6c757d', 
          marginTop: '1rem', 
          fontSize: '0.9rem'
        }}>
          모집 단위 선택과 모든 필수 점수를 입력해주세요
        </p>
      )}
    </motion.div>
  );
}

export default ScoreInput;