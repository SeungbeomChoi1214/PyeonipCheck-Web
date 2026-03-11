대학 편입 합격 예측 시스템 (University Transfer Admission Prediction System)
📋 프로젝트 개요
실시간 편입 합격 가능성 분석 및 전략 제안 플랫폼

사용자의 영어/수학 점수를 입력받아 36개 주요 대학의 편입 합격 가능성을 정규분포 기반 시뮬레이션으로 분석하고, 개인 맞춤형 지원 전략을 제공하는 웹 애플리케이션입니다.

🏗️ 시스템 아키텍처
Backend (FastAPI + SQLAlchemy)
API 서버: FastAPI 기반 RESTful API

데이터베이스: SQLite (university.db)

ORM: SQLAlchemy

핵심 모델: University, AdmissionTrack, StudentScore

Frontend (React + Recharts)
UI 프레임워크: React.js

차트 라이브러리: Recharts (동적 스택 바 차트)

애니메이션: Framer Motion

스타일링: Inline CSS

🎯 핵심 기능
1. 지능형 점수 환산 시스템
공식: (영어점수/영어만점 × 영어가중치) + (수학점수/수학만점 × 수학가중치)
스케일링: 환산점수 × (총만점 / 총가중치)

Copy
2. 트랙별 맞춤 분석
자연계열: Natural Major/General (영어+수학 복합)

인문계열: Humanities Major/General (영어 단일)

동적 전형 구분: DB 기반 max_score_math 판별

3. 티어 기반 경쟁 분석
S티어 (연세대, 고려대 등): 평균 85%, 표준편차 8

A티어 (인하대, 국민대 등): 평균 78%, 표준편차 12

B티어 (가천대, 경기대 등): 평균 70%, 표준편차 15

C티어 (기타): 평균 60%, 표준편차 18

4. 실시간 시각화
스택 바 차트: 영어/수학 점수 분리 표시

동적 Y축: 대학별 총만점에 따른 자동 조절

비교 분석: 사용자 vs 안정권 vs 평균 점수

📊 데이터 구조
University 테이블
- id, name, tier, waitlist_ratio
- exam_type_natural, exam_type_humanities
- real_applicant_count

Copy
sql
AdmissionTrack 테이블
- university_id, track_type (NATURAL_GENERAL/MAJOR, HUMAN_GENERAL/MAJOR)
- max_score_eng, max_score_math, total_max_score
- weight_ratio (예: "40:60"), mu, sigma

Copy
sql
StudentScore 테이블
- track_id, score_eng, score_math, score_total
- is_virtual, is_spam (허수 방어)

Copy
sql
🔄 워크플로우
사용자 입력: 대학명, 학과명, 계열, 영어/수학 점수

트랙 매핑: 학과 키워드 기반 Major/General 분류

점수 환산: DB의 weight_ratio 적용한 가중 점수 계산

순위 산출: 정규분포 기반 백분위 계산

전략 제안: 대안 트랙 분석 및 합격 확률 개선안

시각화: 동적 차트로 결과 표시

🛠️ 주요 스크립트
reset_and_init_db.py: DB 초기화 및 대학 데이터 생성

generate_simulation.py: 15,000명 가상 지원자 데이터 생성

update_admission_rules.py: CSV 기반 입시 정보 업데이트

verify_data.py: 데이터 무결성 검증

📈 분석 알고리즘
합격 예측 모델
percentile = stats.norm.cdf(user_score, track_mu, tier_sigma)
rank = (1 - percentile) × total_applicants

Copy
python
충원 인사이트
대학별 충원 배수 데이터 기반 추가 합격 가능성 분석

실제 데이터 vs 추정 데이터 구분 표시

🎨 UI/UX 특징
반응형 디자인: 모바일/데스크톱 최적화

실시간 애니메이션: 순위 카운팅 효과

색상 코딩: 합격 가능성별 시각적 구분

상세 툴팁: 점수 분해 정보 제공

🔧 기술 스택 요약
Backend: FastAPI, SQLAlchemy, SQLite, NumPy, SciPy
Frontend: React, Recharts, Framer Motion
Data: Pandas (전처리), 정규분포 시뮬레이션
API: RESTful, CORS 지원

이 시스템은 실제 편입 시장의 복잡성을 단순화하여 직관적인 인사이트를 제공하는 것이 핵심 목표입니다.