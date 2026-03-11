import React, { useState } from 'react';
import axios from 'axios';
import UniversitySelector from './components/UniversitySelector';
import ScoreInput from './components/ScoreInput';
import PredictPage from './components/PredictPage';
import './App.css';

// 20240523_FINAL_DEPLOY_TEST

const API_BASE = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8000';

function App() {
  const [step, setStep] = useState(1);
  const [selectedUniv, setSelectedUniv] = useState(null);
  const [selectedDivision, setSelectedDivision] = useState(null);
  const [deptName, setDeptName] = useState('');
  const [scores, setScores] = useState({ eng: '', math: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async (requestData) => {
    setLoading(true); // 1. 로딩 스피너 시작

    try {
      // 2. [추가된 부분] 1500ms(1.5초) 동안 강제로 기다림 (분석하는 느낌 연출)
      await new Promise(resolve => setTimeout(resolve, 1500));

      // 3. 그 다음에 진짜 API 호출
      const response = await axios.post(`${API_BASE}/predict`, requestData);
      setResult(response.data);
      setStep(3);
    } catch (error) {
      if (error.response?.status === 400) {
        alert(error.response.data.detail);
      } else {
        alert('예측 중 오류가 발생했습니다.');
      }
    } finally {
      setLoading(false); // 4. 로딩 끝
    }
  };

  const resetApp = () => {
    setStep(1);
    setSelectedUniv(null);
    setSelectedDivision(null);
    setDeptName('');
    setScores({ eng: '', math: '' });
    setResult(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎯 편입 합격 예측 시스템</h1>
        <p>데이터 기반 합격 가능성 진단</p>
      </header>

      <main className="app-main">
        {step === 1 && (
          <UniversitySelector
            selectedUniv={selectedUniv}
            selectedDivision={selectedDivision}
            onUnivSelect={setSelectedUniv}
            onDivisionSelect={setSelectedDivision}
            onNext={() => setStep(2)}
          />
        )}

        {step === 2 && (
          <ScoreInput
            selectedUniv={selectedUniv}
            selectedDivision={selectedDivision}
            deptName={deptName}
            scores={scores}
            onDeptNameChange={setDeptName}
            onScoreChange={setScores}
            onBack={() => setStep(1)}
            onPredict={handlePredict}
            loading={loading}
          />
        )}

        {step === 3 && result && (
          <PredictPage
            result={result}
            selectedUniv={selectedUniv}
            selectedDivision={selectedDivision}
            deptName={deptName}
            scores={scores}
            onReset={resetApp}
          />
        )}
      </main>
    </div>
  );
}

export default App;