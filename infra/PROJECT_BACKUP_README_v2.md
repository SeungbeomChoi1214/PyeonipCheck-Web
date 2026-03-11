# 📋 편입 합격 예측 시스템 - 프로젝트 백업 문서 v2.0

**백업 일시:** 2026년 1월1일 현재  
**프로젝트 상태:** 런칭 가능한 완성 단계  
**주요 업데이트:** 데이터 정제 강화, 500명 시뮬레이션, 스마트 UI 구현

---

## 🏗️ 프로젝트 구조

```
TP_Vscode/
├── 📁 frontend/                    # React 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   │   ├── UniversitySelector.js    # 대학/학과 선택
│   │   │   ├── ScoreInput.js            # 점수 입력 (조건부 렌더링)
│   │   │   └── PredictPage.js           # 전문 컨설팅 대시보드
│   │   ├── App.js                       # 메인 앱
│   │   └── App.css                      # 스타일
│   └── package.json                     # 의존성 (axios, framer-motion, recharts)
│
├── 📁 scripts/                     # 데이터 처리 스크립트
│   ├── init_db_data.py             # 강력한 데이터 정제 & 룰북 적용
│   ├── generate_simulation.py      # 500명 정규분포 시뮬레이션
│   ├── check_status.py             # 데이터 상태 검증
│   └── inspect_all_departments.py  # 학과명 검사
│
├── 📁 output/                      # 처리된 데이터
│   ├── Master_Data_Final.xlsx      # 최종 마스터 데이터
│   └── all_departments_list.txt    # 학과명 검사 결과
│
├── 🗄️ 핵심 파일
│   ├── main.py                     # FastAPI 백엔드 (허수 방어 포함)
│   ├── models.py                   # DB 모델 (is_spam 컬럼 추가)
│   ├── database.py                 # DB 연결
│   ├── university.db               # SQLite 데이터베이스
│   └── TP_Simulation_Data.xlsx     # 대학별 점수 기준
│
└── 📖 문서
    ├── LAUNCH_GUIDE.md             # 런칭 가이드
    ├── FINAL_GUIDE.md              # 최종 실행 가이드
    └── PROJECT_BACKUP_README.md    # 이 문서
```

---

## 🎯 핵심 기능 및 특징

### 1. 데이터 정제 시스템 (강력한 세탁기)
- **정규식 기반 정제**: 괄호, 대괄호, 숫자, 특수문자 완전 제거
- **블랙리스트 필터링**: '단계', '선택', '모집단위' 등 불필요한 데이터 차단
- **중복 방지**: get_or_create 패턴으로 안전한 데이터 적재

### 2. 하드코딩된 시험 분류 룰북
```python
# GROUP A: 수학 100% (MATH_ONLY)
MATH_ONLY_UNIVERSITIES = [
    '한양대학교', '중앙대학교', '이화여자대학교', '숙명여자대학교',
    '가천대학교', '세종대학교', '단국대학교', '서울과학기술대학교', '경희대학교'
]

# GROUP B: 영어+수학 (ENG_MATH) - 나머지 모든 자연계
# 인문계: 무조건 ENG_ONLY
```

### 3. 500명 정규분포 시뮬레이션
- **Bell Curve**: `random.gauss(평균, 표준편차=8)` 사용
- **현실적 분포**: 30-100점 범위 제한
- **대용량 데이터**: 학과당 500명으로 통계적 신뢰성 확보

### 4. 허수 방어 시스템 (쉐도우 밴)
- **스팸 탐지**: 98점 초과, 합계 195점 초과 등 비현실적 점수 탐지
- **쉐도우 밴**: 허수는 1등으로 표시하되 실제 랭킹에서는 제외
- **데이터 분리**: `is_spam=False` 데이터만 통계 산출에 사용

### 5. 전문 컨설팅 대시보드
- **4단계 뱃지 시스템**: 🔵최초합 유력 → 🟢추가합격 가능 → 🟡소신 지원 → 🔴위험/상향
- **카운트업 애니메이션**: 등수와 백분위가 0부터 실제 값까지 증가
- **액션 가이드**: "영어 2문제 더 맞추면 안정권 진입" 같은 구체적 조언
- **AI 추천 시스템**: 확장 가능한 UI 구조

### 6. 스마트 UI (조건부 렌더링)
- **MATH_ONLY**: 수학 입력창만 표시
- **ENG_ONLY**: 영어 입력창만 표시  
- **ENG_MATH**: 둘 다 표시
- **단순화된 가이드**: "기출 최고 점수 입력" 메시지

---

## 🗄️ 데이터베이스 스키마

### University (대학)
- `id`: Primary Key
- `name`: 대학명
- `tier_group`: S, A, B, C 등급 (확장용)
- `base_score_*`: 시뮬레이션용 기준 점수

### Department (학과)
- `id`: Primary Key
- `university_id`: 대학 FK
- `name`: 학과명 (정제됨)
- `division`: Humanities/Natural
- `popularity_offset`: 인기도 가중치

### StudentScore (학생 점수)
- `id`: Primary Key
- `department_id`: 학과 FK
- `score_eng`: 영어 점수
- `score_math`: 수학 점수
- `score_total`: 총점 (랭킹 기준)
- `is_virtual`: 가상 데이터 여부
- `is_spam`: 허수 여부 (쉐도우 밴용)
- `created_at`: 생성 시간

---

## 🚀 실행 환경 및 의존성

### 백엔드 (Python)
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pandas==2.1.3
python-multipart==0.0.6
```

### 프론트엔드 (React)
```
react==18.3.1
axios==1.7.9
framer-motion==11.15.0
recharts==2.13.3
```

### 데이터베이스
- **SQLite**: 개발/테스트용 (university.db)
- **확장 가능**: PostgreSQL, MySQL 등으로 마이그레이션 가능

---

## 📊 데이터 현황 (백업 시점 기준)

### 대학 데이터
- **총 대학 수**: 약 50개 대학
- **총 학과 수**: 약 500개 학과
- **자연계/인문계**: 자동 분류 완료

### 시뮬레이션 데이터
- **학과당 가상 학생**: 500명
- **총 시뮬레이션 데이터**: 약 250,000개 레코드
- **분포**: 정규분포 (평균 75점, 표준편차 8점)

### 데이터 품질
- **정제율**: 99% (블랙리스트 필터링 적용)
- **중복 제거**: 완료
- **허수 방어**: 활성화

---

## 🔧 주요 API 엔드포인트

### 1. 대학 목록 조회
```
GET /universities
Response: [{"id": 1, "name": "건국대학교"}, ...]
```

### 2. 학과 목록 조회
```
GET /universities/{univ_id}/departments
Response: [{"id": 1, "name": "컴퓨터공학부", "division": "Natural", "exam_type": "ENG_MATH"}, ...]
```

### 3. 합격 예측 (핵심 기능)
```
POST /predict
Request: {"dept_id": 1, "my_score_eng": 85.0, "my_score_math": 80.0}
Response: {
  "rank": 15,
  "total_competitors": 500,
  "top_percent": 3.0,
  "diagnosis": "안정",
  "is_flagged": false
}
```

---

## 🎨 UI/UX 특징

### 디자인 컨셉
- **전문 컨설팅 느낌**: 카드 기반 레이아웃
- **편입생 심리 반영**: 직관적 신호등 시스템
- **데이터 기반 안심**: 구체적 수치와 액션 가이드

### 색상 시스템
- **안정**: #2196F3 (파란색)
- **적정**: #4CAF50 (초록색)  
- **소신**: #FF9800 (주황색)
- **위험**: #F44336 (빨간색)

### 애니메이션
- **Framer Motion**: 부드러운 전환 효과
- **카운트업**: 숫자가 0부터 실제 값까지 증가
- **Progress Bar**: 내 위치를 시각적으로 표시

---

## 🔒 보안 및 안정성

### 허수 방어
- **자동 탐지**: 비현실적 점수 자동 감지
- **쉐도우 밴**: 허수에게는 정상 결과 표시, 실제 통계에서는 제외
- **데이터 무결성**: 정상 데이터만으로 랭킹 계산

### CORS 설정
- **허용 도메인**: localhost:3000, 127.0.0.1:3000
- **확장 가능**: 실제 도메인으로 변경 가능

### 에러 처리
- **백엔드**: HTTPException으로 명확한 에러 메시지
- **프론트엔드**: try-catch로 사용자 친화적 에러 처리

---

## 📈 확장 가능성

### 단기 확장 (1-2개월)
- **실제 합격 데이터 연동**: 각 대학 공식 데이터 수집
- **더 많은 대학 추가**: 전국 모든 편입 가능 대학
- **모바일 앱**: React Native로 포팅

### 중기 확장 (3-6개월)
- **AI 추천 시스템**: 실제 구현 (현재는 UI만)
- **사용자 계정 시스템**: 로그인, 즐겨찾기, 히스토리
- **실시간 경쟁률**: WebSocket으로 실시간 업데이트

### 장기 확장 (6개월+)
- **프리미엄 서비스**: 상세 분석, 개인 맞춤 컨설팅
- **커뮤니티 기능**: 편입 준비생 소통 공간
- **데이터 분석 대시보드**: 관리자용 통계 시스템

---

## 🚨 백업 및 복구 가이드

### 중요 파일 백업 리스트
1. **데이터베이스**: `university.db`
2. **설정 파일**: `main.py`, `models.py`, `database.py`
3. **프론트엔드**: `frontend/src/` 전체
4. **스크립트**: `scripts/` 전체
5. **원본 데이터**: `TP_Simulation_Data.xlsx`, `Master_Data.xlsx`

### 복구 절차
1. 위 파일들을 새 환경에 복사
2. Python 가상환경 생성 및 의존성 설치
3. `LAUNCH_GUIDE.md` 따라 순차 실행
4. 데이터 검증: `python scripts/check_status.py`

---

## 📞 기술 지원 및 문의

### 개발 환경
- **Python**: 3.8+
- **Node.js**: 16+
- **OS**: Windows 10/11 (개발 기준)

### 주요 이슈 해결
- **대학 목록 안 보임**: 백엔드 서버 실행 확인
- **점수 입력창 이상**: exam_type 전달 확인
- **결과 화면 오류**: 시뮬레이션 데이터 재생성

---

**🎉 프로젝트 상태: 런칭 준비 완료**  
**마지막 업데이트**: 2026월 1월 1일  
**다음 마일스톤**: 실제 서비스 배포 및 사용자 피드백 수집