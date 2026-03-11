# 편입 합격 예측 서비스 - 프로젝트 백업 문서

## 📁 프로젝트 구조

```
TP_Vscode/
├── 📂 output/                          # 생성된 결과 파일들
│   ├── Gachon_extracted.xlsx          # 가천대 추출 데이터
│   ├── Hanyang_extracted.xlsx         # 한양대 추출 데이터  
│   ├── Hongik_extracted.xlsx          # 홍익대 추출 데이터
│   ├── Master_Data_Final.xlsx         # 최종 통합 데이터
│   ├── Master_Data_v2.xlsx            # 마스터 데이터 v2
│   └── universities_data.xlsx         # 대학 데이터 통합본
│
├── 📂 pdfs/                           # 원본 PDF 모집요강 (44개 대학)
│   ├── 가천대 모집요강.pdf
│   ├── 건국대 모집요강.pdf
│   ├── 경희대 모집요강.pdf
│   ├── 한양대 모집요강.pdf
│   └── ... (총 44개 대학 PDF)
│
├── 📂 raw_data/                       # 원시 데이터
│   └── all_tables_raw.txt            # PDF에서 추출한 텍스트 데이터
│
├── 📂 scripts/                       # 파싱 스크립트들
│   ├── parse_university_data_v2.py   # 대학 데이터 파싱 v2
│   └── parse_university_data_v3.py   # 대학 데이터 파싱 v3
│
├── 📂 static/                        # 웹 정적 파일
│   └── index.html                    # 웹 인터페이스
│
├── 🐍 백엔드 핵심 파일들
│   ├── main.py                       # FastAPI 메인 서버
│   ├── models.py                     # SQLAlchemy 데이터베이스 모델
│   ├── schemas.py                    # Pydantic 스키마
│   ├── database.py                   # 데이터베이스 연결 설정
│   └── university.db                 # SQLite 데이터베이스
│
├── 📊 데이터 처리 스크립트들
│   ├── append_data.py                # 데이터 추가/병합
│   ├── check_db.py                   # DB 상태 확인
│   ├── create_dummy_students.py      # 가상 학생 데이터 생성
│   ├── create_hanyang_dummy.py       # 한양대 더미 데이터
│   ├── dump_to_csv.py               # DB → CSV 변환
│   ├── extract_tables.py            # PDF 테이블 추출
│   ├── force_update_hongik.py       # 홍익대 데이터 강제 업데이트
│   ├── load_all_universities.py     # 모든 대학 데이터 로드
│   ├── load_data.py                 # 데이터 로딩
│   ├── make_template.py             # 템플릿 생성
│   ├── parse_university_data.py     # 대학 데이터 파싱
│   └── read_pdf.py                  # PDF 읽기
│
├── 📄 설정 및 기타 파일들
│   ├── requirements.txt             # Python 패키지 의존성
│   ├── setup_project.py            # 프로젝트 초기 설정
│   ├── all_tables_raw.txt          # 텍스트 데이터 (메인)
│   ├── Master_Data.xlsx            # 마스터 데이터
│   ├── rough_data.csv              # 임시 CSV 데이터
│   ├── ngrok.exe                   # 터널링 도구
│   └── TP_Server_Key.pem           # 서버 키
```

## 🔧 핵심 기능별 파일 분류

### 1. 백엔드 API 서버
- `main.py` - FastAPI 서버, 예측 API 엔드포인트
- `models.py` - University, Department, ScoringRule, StudentScore 모델
- `schemas.py` - API 입출력 스키마 정의
- `database.py` - SQLite 연결 설정

### 2. 데이터 수집 & 파싱
- `extract_tables.py` - PDF → 텍스트 추출
- `parse_university_data.py` - 텍스트 → 구조화된 데이터
- `all_tables_raw.txt` - 44개 대학 모집요강 텍스트

### 3. 데이터베이스 관리
- `university.db` - SQLite 데이터베이스
- `load_data.py` - 가천대 데이터 로딩
- `create_hanyang_dummy.py` - 한양대 2단계 전형 데이터
- `create_dummy_students.py` - 경쟁자 100명 가상 데이터

### 4. 데이터 검증 & 변환
- `check_db.py` - DB 상태 확인
- `dump_to_csv.py` - DB → CSV 내보내기
- `append_data.py` - 데이터 병합 (현재 파일)

## 📋 주요 데이터 구조

### ScoringRule 테이블 컬럼
```sql
- stage1_eng_ratio: 1단계 영어 비율
- stage1_math_ratio: 1단계 수학 비율  
- has_stage2: 2단계 전형 여부
- stage2_exam_ratio: 2단계 필기 비율
- stage2_doc_ratio: 2단계 서류 비율
- stage1_cutoff: 1단계 커트라인
```

### 대학별 전형 방식
- **가천대**: 영어형(1.0, 0.0) vs 수학형(0.0, 1.0)
- **한양대**: 2단계 전형 (1단계 70% + 서류 30%)
- **홍익대**: 서울(필기), 세종(공인영어+면접)

## 🚀 실행 순서

1. **환경 설정**: `pip install -r requirements.txt`
2. **DB 초기화**: `python setup_project.py`
3. **데이터 로딩**: `python load_data.py`
4. **서버 실행**: `python main.py`
5. **웹 접속**: `http://localhost:8000`

## 📊 현재 데이터 현황

- **대학 수**: 44개 대학 PDF 보유
- **파싱 완료**: 가천대, 한양대, 홍익대 등
- **가상 학생**: 100명 (경영학부 50명, 기계공학부 50명)
- **API 엔드포인트**: `/predict/gachon`, `/predict/hanyang`

## 🔄 백업 권장사항

### 중요 파일 (반드시 백업)
- `university.db` - 메인 데이터베이스
- `all_tables_raw.txt` - 원본 텍스트 데이터
- `main.py`, `models.py` - 핵심 백엔드 코드
- `pdfs/` 폴더 전체 - 원본 PDF 파일들

### 재생성 가능한 파일
- `output/` 폴더 - 스크립트로 재생성 가능
- `Master_Data*.xlsx` - 파싱 스크립트로 재생성
- `rough_data.csv` - 임시 파일

## 📝 개발 히스토리

1. **PDF 수집**: 44개 대학 모집요강 PDF 수집
2. **텍스트 추출**: tabula-py로 PDF → 텍스트 변환
3. **데이터 파싱**: 정규표현식으로 학과/모집인원 추출
4. **DB 설계**: SQLAlchemy로 대학/학과/전형규칙 모델링
5. **API 개발**: FastAPI로 예측 서비스 구현
6. **2단계 전형**: 한양대 복잡한 전형 방식 구현
7. **경쟁자 데이터**: 가상 학생 100명으로 순위 시뮬레이션

---
📅 **백업 생성일**: 2026년 1월 1일
🔧 **개발 환경**: Python 3.x, FastAPI, SQLAlchemy, pandas
📍 **프로젝트 위치**: `C:\TP_Vscode`