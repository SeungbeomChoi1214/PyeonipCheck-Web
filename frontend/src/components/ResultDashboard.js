import React, { useState, useEffect } from 'react'; // useEffect 추가
import { motion } from 'framer-motion';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

function ResultDashboard({ result, onReset }) {
  const [isUnlocked, setIsUnlocked] = useState(false);

  // [🕵️‍♂️ 디버깅용 로그] 데이터가 어떻게 들어오는지 콘솔에 찍습니다.
  useEffect(() => {
    console.log("🔥 백엔드에서 받은 데이터(전체):", result);
    console.log("대학이름 확인:", result.university_name);
  }, [result]);

  // 1. 서울시립대인지 확인 (안전장치 대폭 강화!)
  // result.university_name이 없으면 result.univ, result.university 등등 다 뒤져봅니다.
  const isUOS = (() => {
    const target = (
      result.university_name || 
      result.university || 
      result.univ_name || 
      result.school_name || 
      ""
    ).toString(); // 문자로 변환
    
    // "시립" 또는 "UOS"가 들어있거나, 점수 입력값이 70인데 결과가 35라면 시립대로 간주(임시 조치)
    return target.includes('서울시립') || target.includes('시립') || target.includes('UOS');
  })();

  console.log("✅ 서울시립대 판정 결과:", isUOS); // true가 나와야 함

  // 2. 점수 계산 로직
  const { 
    converted_score_eng, 
    converted_score_math, 
    university_total_max, 
    isComposite,
    final_display_score 
  } = (() => {
    const max_eng = result.max_score_eng || 0;
    const max_math = result.max_score_math || 0;
    const total_max = result.total_max_score || 100;

    const user_eng = result.user_eng_score || 0;
    const user_math = result.user_math_score || 0;

    let display_score = result.my_score;
    
    if (isUOS) {
        // 시립대: 영어/수학 중 입력한 큰 점수를 그대로 사용
        display_score = Math.max(user_eng, user_math);
    }

    let complex = (max_eng > 0) && (max_math > 0);
    if (isUOS) complex = false; 

    let eng_conv = 0;
    let math_conv = 0;

    if (max_eng > 0) eng_conv = (user_eng / max_eng) * max_eng;
    if (max_math > 0) math_conv = (user_math / max_math) * max_math;

    if (isUOS) {
        if (user_eng > 0) {
            eng_conv = display_score; 
            math_conv = 0;
        } else {
            math_conv = display_score;
            eng_conv = 0;
        }
    }

    return {
      converted_score_eng: eng_conv,
      converted_score_math: math_conv,
      university_total_max: total_max,
      isComposite: complex,
      final_display_score: display_score
    };
  })();

  const chartData = [
    { name: '내 점수', total: final_display_score },
    { name: '컷라인', total: result.cutline },
    { name: '평균', total: result.average_score || 0 },
  ];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{ background: 'white', border: '1px solid #e0e0e0', borderRadius: '8px', padding: '12px', fontSize: '14px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
          <p style={{ margin: '0 0 8px 0', fontWeight: '600' }}>{label}</p>
          <p style={{ margin: '4px 0 0 0', fontWeight: '600', color: '#1565C0' }}>
            환산 점수: {Math.round(data.total)}점
          </p>
        </div>
      );
    }
    return null;
  };

  // | 기호 처리 안전장치
  const trackText = result.track_type && result.track_type.trim() !== "" ? ` | ${result.track_type}` : "";

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px', background: '#f8f9fa', minHeight: '100vh' }}>
      
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ background: 'linear-gradient(135deg, #263238 0%, #37474f 100%)', color: 'white', padding: '30px', borderRadius: '16px', marginBottom: '30px', textAlign: 'center' }}
      >
        <h1 style={{ fontSize: '2rem', fontWeight: '700', margin: '0 0 10px 0', letterSpacing: '-0.5px' }}>
          편입 합격 예측 분석 리포트
        </h1>
        <p style={{ fontSize: '1.1rem', margin: 0, opacity: 0.9, fontWeight: '400' }}>
          {/* 대학 이름이 없으면 '대학교'라고라도 출력하게 수정 */}
          {result.university_name || result.university || "대학교"} {result.dept_name}
          {trackText}
        </p>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        style={{ background: 'white', borderRadius: '16px', padding: '40px', marginBottom: '30px', boxShadow: '0 8px 32px rgba(0,0,0,0.08)', border: '3px solid #1565C0' }}
      >
        <div style={{ textAlign: 'center' }}>
          <div style={{ background: '#1565C0', color: 'white', padding: '12px 30px', borderRadius: '50px', display: 'inline-block', fontSize: '1.2rem', fontWeight: '700', marginBottom: '25px' }}>
            점수 분석 결과
          </div>
          
          <div style={{ fontSize: '3rem', fontWeight: '900', color: '#263238', marginBottom: '10px', lineHeight: '1' }}>
            총 환산 점수: <span style={{ color: '#1565C0' }}>{Math.round(final_display_score)}점</span>
          </div>
          <div style={{ fontSize: '1.5rem', color: '#546e7a', fontWeight: '600', marginBottom: '20px' }}>
            / {university_total_max}점 만점
          </div>

          <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px', display: 'inline-block' }}>
            {isUOS ? (
               <div style={{ fontSize: '1rem', color: '#333', fontWeight: '600' }}>
                 {converted_score_eng > 0 ? "전공영어 필기 100% 반영 (가중치 없음)" : "전공수학 필기 100% 반영 (가중치 없음)"}
               </div>
            ) : (
                <>
                    <div style={{ fontSize: '1rem', color: '#666', marginBottom: '5px' }}>
                    가중치 비율: {result.weight_ratio}
                    </div>
                    <div style={{ fontSize: '0.9rem', color: '#888' }}>
                    영어 {result.max_score_eng}점 만점 + 수학 {result.max_score_math}점 만점
                    </div>
                </>
            )}
          </div>
        </div>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        style={{ background: 'white', borderRadius: '16px', padding: '35px', marginBottom: '30px', boxShadow: '0 4px 20px rgba(0,0,0,0.06)' }}
      >
        <h3 style={{ fontSize: '1.4rem', fontWeight: '700', color: '#263238', marginBottom: '25px', textAlign: 'center' }}>
          점수 비교 분석 (동적 스택 바 차트)
        </h3>
        
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#666' }} axisLine={{ stroke: '#e0e0e0' }} />
            <YAxis domain={[0, 100]} label={{ value: '점수', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#666' } }} tick={{ fontSize: 12, fill: '#666' }} axisLine={{ stroke: '#e0e0e0' }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar dataKey="total" fill="#1565C0" name="환산 점수" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>

        <div style={{ marginTop: '20px', padding: '15px', background: isComposite ? '#e3f2fd' : '#fff3e0', borderRadius: '8px', textAlign: 'center', fontSize: '0.95rem', color: isComposite ? '#1565C0' : '#F57C00', fontWeight: '600' }}>
          {isUOS ? (
              converted_score_eng > 0 
                ? "2단계: 전공영어 필기 100% 반영 (서울시립대 특성)" 
                : "2단계: 전공수학 필기 100% 반영 (서울시립대 특성)"
          ) : (
              isComposite
                ? `복합 과목 전형: 영어(${result.max_score_eng}점) + 수학(${result.max_score_math}점) | 가중치 ${result.weight_ratio}`
                : `단일 과목 전형: ${(result.max_score_eng || 0) > 0 ? '영어' : '수학'} 단독 평가`
          )}
        </div>
      </motion.div>

      {/* 전략 코멘트 & 잠금 기능 */}
      {result.strategy_comment && (
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          style={{ background: 'white', borderRadius: '16px', padding: '35px', marginBottom: '30px', boxShadow: '0 4px 20px rgba(0,0,0,0.06)', border: '2px solid #1565C0', position: 'relative' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
            <div style={{ background: '#1565C0', color: 'white', padding: '8px 16px', borderRadius: '20px', fontSize: '1rem', fontWeight: '700' }}>
              전략 제안
            </div>
          </div>

          <div style={{ filter: isUnlocked ? 'none' : 'blur(5px)', transition: 'filter 0.3s ease' }}>
            <div style={{ fontSize: '1.3rem', fontWeight: '600', lineHeight: '1.4', color: '#263238' }}>
              {result.message || "🟢 합격권입니다! 대학별 고사 실전 연습에 집중하세요."}
            </div>
          </div>

          {!isUnlocked && (
            <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }}>
              <button 
                onClick={() => {
                  alert("🎉 오픈 베타 기능! 상세 리포트가 무료로 잠금 해제되었습니다.");
                  setIsUnlocked(true);
                }}
                style={{ background: '#007bff', color: 'white', border: 'none', padding: '12px 24px', borderRadius: '25px', fontSize: '1rem', fontWeight: '600', cursor: 'pointer', boxShadow: '0 4px 12px rgba(0,123,255,0.3)' }}
              >
                🔒 상세 합격 전략 확인하기 (클릭)
              </button>
            </div>
          )}

          {isUnlocked && (
            <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
              <a 
                href="https://pf.kakao.com/_IwHgn/chat" 
                target="_blank" 
                rel="noopener noreferrer"
                style={{ display: 'inline-block', background: '#28a745', color: 'white', textDecoration: 'none', padding: '10px 20px', borderRadius: '20px', fontSize: '0.9rem', fontWeight: '600', cursor: 'pointer', border: 'none', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}
              >
                👨‍🏫 더 정확한 진단이 필요하다면? [1:1 상담 신청하기]
              </a>
            </div>
          )}
        </motion.div>
      )}

      {/* 리셋 버튼 */}
      <div style={{ textAlign: 'center' }}>
        <button 
          onClick={onReset}
          style={{ background: 'linear-gradient(135deg, #263238 0%, #37474f 100%)', color: 'white', border: 'none', padding: '18px 50px', borderRadius: '50px', fontSize: '1.2rem', fontWeight: '700', cursor: 'pointer', boxShadow: '0 6px 20px rgba(38, 50, 56, 0.3)', transition: 'transform 0.3s ease, box-shadow 0.3s ease' }}
          onMouseOver={(e) => { e.target.style.transform = 'translateY(-2px)'; e.target.style.boxShadow = '0 8px 25px rgba(38, 50, 56, 0.4)'; }}
          onMouseOut={(e) => { e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 6px 20px rgba(38, 50, 56, 0.3)'; }}
        >
          다른 학과 분석하기
        </button>
      </div>

      <div style={{ textAlign: 'center', fontSize: '0.8rem', color: '#999', marginTop: '2rem' }}>
        본 결과는 모의 진단이며 실제 합격 여부와 무관합니다.
      </div>
    </div>
  );
}

export default ResultDashboard;