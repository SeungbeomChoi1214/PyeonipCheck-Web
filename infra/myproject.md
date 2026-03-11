# 폴더&파일 트리
TP_Vscode/
├── 📁 frontend/
│   ├── 📁 public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── UniversitySelector.js
│   │   │   ├── ScoreInput.js
│   │   │   ├── PredictPage.js
│   │   │   └── ResultDashboard.js
│   │   ├── 📁 data/
│   │   │   └── constants.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── package-lock.json
│
├── 📁 백엔드 핵심 파일/
│   ├── main.py              # FastAPI 메인 서버
│   ├── models.py            # DB 모델 정의
│   ├── database.py          # DB 연결 설정
│   ├── services.py          # 비즈니스 로직
│   ├── schemas.py           # API 스키마
│   └── requirements.txt     # Python 의존성
│
├── 📁 배포 설정/
│   ├── .gitignore
│   ├── deploy.sh           # 배포 스크립트
│   ├── DEPLOYMENT_GUIDE.md
│   └── README.md
│
└── 📁 초기화 스크립트/ (선택)
    ├── init_db_data.py
    └── setup_project.py
