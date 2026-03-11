import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

const API_BASE = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8000';

function UniversitySelector({ selectedUniv, selectedDivision, onUnivSelect, onDivisionSelect, onNext }) {
  const [universities, setUniversities] = useState(null);

  useEffect(() => {
    fetchUniversities();
  }, []);

  const fetchUniversities = async () => {
    try {
      const response = await axios.get(`${API_BASE}/universities`);
      if (Array.isArray(response.data)) {
        setUniversities(response.data);
      } else {
        setUniversities([]);
      }
    } catch (error) {
      console.error(error);
      setUniversities([]);
      alert('서버 연결 실패');
    }
  };

  const handleUnivChange = (e) => {
    if (!Array.isArray(universities)) return;
    const univ = universities.find(u => u.id === parseInt(e.target.value));
    onUnivSelect(univ);
  };

  const handleDivisionSelect = (division) => {
    onDivisionSelect(division);
  };

  // [수정됨] 서울시립대 상세 전형 안내
  const getExamTypeDisplay = () => {
    if (!selectedUniv || !selectedDivision) return '영어+수학 입력';
    
    // 🚨 서울시립대 예외 처리 (상세 텍스트 표시)
    if (selectedUniv.name.includes('서울시립')) {
      if (selectedDivision === 'Humanities') {
        return '1단계: 공인영어 / 2단계: 영어 필기 (100%)';
      } else {
        return '1단계: 공인영어 / 2단계: 수학 필기 (100%)';
      }
    }

    const examInfo = selectedDivision === 'Natural' 
      ? selectedUniv.exam_info?.Natural 
      : selectedUniv.exam_info?.Humanities;
    
    if (!examInfo) return '전형 정보 로딩 중...';
    
    if (!examInfo.has_eng && examInfo.has_math) return '수학 100% 전형';
    if (examInfo.has_eng && !examInfo.has_math) return '영어 100% 전형';
    if (examInfo.has_eng && examInfo.has_math) return '영어+수학 복합 전형';
    
    return '전형 정보 불명';
  };

  return (
    <motion.div 
      className="card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="step-indicator">
        <div className="step active">1</div>
        <div className="step inactive">2</div>
        <div className="step inactive">3</div>
      </div>

      <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: '#495057' }}>
        🏫 지원 대학 및 계열 선택
      </h2>

      <div className="form-group">
        <label className="form-label">대학 선택</label>
        <select 
          className="form-select"
          value={selectedUniv?.id || ''}
          onChange={handleUnivChange}
        >
          <option value="">대학을 선택하세요</option>
          {universities === null ? (
            <option disabled>로딩 중...</option>
          ) : Array.isArray(universities) && universities.length > 0 ? (
            universities.map(univ => (
              <option key={univ.id} value={univ.id}>{univ.name}</option>
            ))
          ) : (
            <option disabled>데이터를 불러올 수 없습니다</option>
          )}
        </select>
      </div>

      {selectedUniv && (
        <div className="form-group">
          <label className="form-label">계열 선택</label>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
            <button
              className={`btn ${selectedDivision === 'Humanities' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => handleDivisionSelect('Humanities')}
              style={{ flex: 1, padding: '1rem' }}
            >
              📚 인문계열
            </button>
            <button
              className={`btn ${selectedDivision === 'Natural' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => handleDivisionSelect('Natural')}
              style={{ flex: 1, padding: '1rem' }}
            >
              🔬 자연계열
            </button>
          </div>
        </div>
      )}

      {selectedUniv && selectedDivision && (
        <motion.div
          initial={{ opacity: 0 }}s
          animate={{ opacity: 1 }}
          style={{ textAlign: 'center', marginTop: '2rem' }}
        >
          <div style={{ 
            background: '#f8f9fa', 
            padding: '1rem', 
            borderRadius: '10px', 
            marginBottom: '1.5rem' 
          }}>
            <strong>{selectedUniv.name} - {selectedDivision === 'Natural' ? '자연계열' : '인문계열'}</strong>
            <br />
            <span style={{ color: '#1976d2', fontWeight: '600' }}>
              {getExamTypeDisplay()}
            </span>
          </div>
          
          <button 
            className="btn btn-primary"
            onClick={onNext}
          >
            다음 단계 →
          </button>
        </motion.div>
      )}
    </motion.div>
  );
}

export default UniversitySelector;