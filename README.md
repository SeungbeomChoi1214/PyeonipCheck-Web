# PyeonipCheck — 편입 합격 예측 라이브 웹 서비스

> FastAPI · React · AWS EC2 · Nginx · SQLite  
> 모집요강 데이터 기반 편입 합격 예측 서비스. 라이브 운영 중 발생한 장애를 무중단으로 방어한 경험에 집중했습니다.

---

## 📌 프로젝트 개요

44개 대학의 편입 모집요강 PDF를 파싱해 DB화하고, 사용자가 입력한 점수와 지원 학과를 기반으로 합격 가능성을 시각적 대시보드로 제공합니다.

단순 기능 구현보다 **실제 사용자가 접속 중인 라이브 환경에서 터진 버그를 어떻게 막았는가**에 초점을 맞춘 프로젝트입니다.

| 항목 | 내용 |
|------|------|
| 기간 | 2025.11 ~ 2026.02 |
| 팀 구성 | 본인 (백엔드 데이터 파이프라인 · 프론트엔드 및 인프라 담당) |
| 담당 | 프론트엔드(React) · AWS 배포 · Nginx 설정 · 장애 대응 |
| 상태 | 비용 최적화를 위해 라이브 운영 종료 후 전체 아키텍처와 트러블슈팅 내역을 GitHub에 문서화하고 AWS 리소스 Terminate |

---

## 🛠️ 기술 스택

```
Frontend     │ React.js, Recharts
Backend      │ FastAPI (Python), SQLite, SQLAlchemy, Pydantic
Infra        │ AWS EC2 (Ubuntu 22.04), Nginx (Reverse Proxy)
Data         │ tabula-py (PDF 파싱), pandas
Deployment   │ nohup + 수동 배포 (FileZilla → /var/www/html)
```

---

## 🖥️ 시스템 아키텍처

```
[사용자 브라우저]
      │  HTTP :80
      ▼
[AWS EC2 - Nginx]
  /var/www/html      ← React 빌드 산출물 서빙
      │  Reverse Proxy :8000
      ▼
[FastAPI + Uvicorn]
      │
      ▼
[SQLite DB]  ←  44개 대학 모집요강 데이터
```

---

## 📊 서비스 화면

### 1단계 — 학교 및 계열 입력
<img width="725" height="1188" alt="스크린샷 2026-02-03 093159" src="https://github.com/user-attachments/assets/f707280d-d208-46e8-9034-cf0a477a5be5" />

### 2단계 — 학과 및 점수 입력
<img width="674" height="1188" alt="스크린샷 2026-02-03 093214" src="https://github.com/user-attachments/assets/763ab80c-ce58-4e2a-95f8-bd6e760d5abe" />

### 3단계 — 분석 리포트 및 경쟁 점수 비교
<img width="410" height="1102" alt="스크린샷 2026-02-03 093227" src="https://github.com/user-attachments/assets/13dc8dc9-f938-4c68-bbc3-0708cf1df413" />

---

## 🔥 트러블슈팅 — 라이브 장애 대응 3건

서비스 오픈 이후 실사용자가 접속한 상태에서 발생한 문제들입니다. 배포 중단 없이 모두 방어했습니다.

---

### Issue 1. React 앱 전체 크래시 (Minified Error #31)

**증상**  
백엔드 응답 데이터가 간헐적으로 `null` 또는 예상 외의 `Object` 형태로 넘어올 때, React가 이를 그대로 렌더링하려다 앱 전체가 백지화되는 현상 발생.

**원인**  
백엔드 API의 응답 스키마가 불안정한 상태였고, 프론트엔드에 별도의 방어 로직이 없었음.

**해결**  
`PredictPage.js`에 `safeString()` 방어 함수를 도입. 어떤 값이 들어와도 렌더링 가능한 안전한 문자열로 변환하도록 처리해 프론트엔드 단의 Fault Tolerance를 확보했습니다.

```javascript
const safeString = (value) => {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
};
```

> 백엔드가 불안정할 때 프론트엔드가 최후 방어선이 되어야 한다는 걸 직접 경험했습니다.

---

### Issue 2. 배포 후 변경사항 미반영 (Nginx 경로 · 권한 문제)

**증상**  
`npm run build` 후 서버에 업로드했는데도, 브라우저에서 이전 버전이 계속 표출됨.

**원인 분석**  
- Nginx `root` 경로가 임시 업로드 경로(`/home/ubuntu/build`)로 잘못 지정되어 있었음  
- 파일 복사 후 디렉토리 소유권이 Nginx 프로세스 계정과 달라 읽기 권한 없음

**해결**  
```bash
# 1. Nginx root 경로를 정석 위치로 수정
root /var/www/html;

# 2. 빌드 파일 복사 후 권한 부여
sudo cp -r build/* /var/www/html/
sudo chmod 755 /var/www/html -R

# 3. Nginx 재기동
sudo systemctl reload nginx
```

---

### Issue 3. 서울시립대 점수 계산 오류 — 프론트엔드 긴급 Hotfix

**증상**  
사용자가 70점을 입력했을 때 서울시립대(UOS) 결과만 35점(또는 0점)으로 반환되는 데이터 오염 발생.

**원인**  
백엔드의 UOS 전용 점수 계산 로직에 결함이 있었으나, 즉각적인 서버 재배포가 불가능한 상황.

**해결**  
프론트엔드에서 `isUOS` 플래그를 생성하고, 서울시립대에 한해 백엔드 응답을 무시한 채 사용자 입력값을 직접 매핑하는 예외 처리를 적용했습니다.

```javascript
const isUOS = university?.name?.includes('서울시립대');

const displayScore = isUOS
  ? userInputScores   // 백엔드 응답 무시, 입력값 직접 사용
  : result.score;     // 정상 케이스
```

> 이 방식은 임시 Hotfix이며, 향후 백엔드 로직 수정 및 예외 케이스를 Config 파일로 분리하는 리팩토링이 예정되어 있습니다.

---

## 📂 프로젝트 구조

```
pyeonipcheck-frontend/          # 로컬 React 작업 환경
├── src/
│   ├── pages/
│   │   └── PredictPage.js      # 핵심 — 합격 예측 결과 화면 + 장애 대응 로직
│   ├── utils/
│   │   └── safeString.js       # 데이터 방어 함수
│   ├── App.js
│   └── index.js
├── public/
├── build/                      # npm run build 산출물 (서버 배포 대상)
└── package.json

TP_Vscode/                      # 백엔드 및 데이터 파이프라인
├── main.py                     # FastAPI 서버 + 예측 API 엔드포인트
├── models.py                   # SQLAlchemy 모델 (University, Department, ScoringRule)
├── schemas.py                  # Pydantic 스키마
├── database.py                 # SQLite 연결 설정
├── university.db               # 대학 데이터 DB
├── scripts/                    # PDF 파싱 스크립트
│   ├── extract_tables.py
│   ├── parse_university_data_v3.py
│   └── load_all_universities.py
└── pdfs/                       # 44개 대학 원본 모집요강 PDF
```

**AWS EC2 배포 경로**
```
/var/www/html/          ← React 빌드 산출물 (Nginx 서빙)
/etc/nginx/sites-available/default  ← Nginx 설정 (포트 80, 리버스 프록시 :8000)
```

---

## 🗄️ 데이터 파이프라인

```
[44개 대학 모집요강 PDF]
        │ tabula-py
        ▼
[all_tables_raw.txt]  ← 원본 텍스트 추출
        │ parse_university_data_v3.py
        ▼
[university.db (SQLite)]
  ├── University (대학 기본 정보)
  ├── Department (학과별 모집 정원)
  └── ScoringRule (전형 방식 · 비율 · 커트라인)
        │
        ▼
[FastAPI /predict 엔드포인트]
```

**대학별 전형 방식 예시**

| 대학 | 전형 구조 |
|------|-----------|
| 가천대 | 영어형(영어 100%) / 수학형(수학 100%) 택1 |
| 한양대 | 1단계 70% + 서류 30% (2단계 전형) |
| 홍익대 | 서울(필기), 세종(공인영어 + 면접) 별도 |

---

## ⚙️ 로컬 실행

```bash
# 백엔드
pip install -r requirements.txt
python setup_project.py   # DB 초기화
python load_data.py        # 데이터 로딩
uvicorn main:app --reload  # http://localhost:8000

# 프론트엔드
cd pyeonipcheck-frontend
npm install
npm start                  # http://localhost:3000
```

---

## 💡 회고 및 향후 개선 계획

이 프로젝트에서 가장 많이 배운 건 **"라이브 서비스는 이상적인 환경을 가정하면 안 된다"** 는 점입니다. 백엔드가 잘못된 데이터를 줘도 프론트엔드가 버텨야 하고, 배포 스크립트 하나가 틀려도 사용자에게 바로 영향이 갑니다.

현재 기술 부채로 남아있는 부분과 개선 방향은 다음과 같습니다.

| 현재 상태 | 개선 방향 |
|-----------|-----------|
| FileZilla 수동 배포 | GitHub Actions 기반 CI/CD 자동화 |
| 프론트엔드 Hotfix 하드코딩 | 백엔드 로직 수정 + 예외 Config 파일 분리 |
| SQLite 단일 파일 DB | AWS RDS (PostgreSQL) 마이그레이션 |
| 단일 EC2 인스턴스 | 백엔드 컨테이너화 (Docker) |
