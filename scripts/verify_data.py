import sqlite3
import pandas as pd
import os

# 1. DB 파일 경로를 프로젝트 루트 기준으로 확실하게 잡기
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # scripts 폴더
PROJECT_ROOT = os.path.dirname(BASE_DIR)              # 상위 폴더 (TP_Vscode)
DB_PATH = os.path.join(PROJECT_ROOT, 'university.db')

print(f"📡 DB 연결 시도 경로: {DB_PATH}")

if not os.path.exists(DB_PATH):
    print("❌ 오류: university.db 파일을 찾을 수 없습니다. init_db_data.py를 먼저 실행하세요.")
    exit()

conn = sqlite3.connect(DB_PATH)

try:
    print("\n=== [1. 데이터 요약 체크] ===")
    # AdmissionTrack 테이블과 StudentScore 테이블 조회
    summary = pd.read_sql('''
        SELECT 
            (SELECT COUNT(*) FROM University) as univ_count,
            (SELECT COUNT(*) FROM AdmissionTrack) as track_count,
            (SELECT COUNT(*) FROM StudentScore) as score_count
    ''', conn)
    print(summary)
    
    univ_cnt = summary.iloc[0]['univ_count']
    track_cnt = summary.iloc[0]['track_count']
    score_cnt = summary.iloc[0]['score_count']

    print("\n=== [2. 정밀 진단] ===")
    if univ_cnt == 36 and track_cnt == 144:
        print("✅ 뼈대(대학/트랙) 생성 완료: 정상")
    else:
        print(f"❌ 뼈대 생성 이상: 대학 36개, 트랙 144개가 되어야 합니다. (현재: {univ_cnt}, {track_cnt})")

    if score_cnt >= 72000:
        print(f"✅ 시뮬레이션 데이터(점수) 생성 완료: {score_cnt}명 (정상)")
    elif score_cnt == 0:
        print("❌ 경고: 트랙은 있지만 '학생 점수'가 0명입니다! (껍데기만 있는 상태)")
        print("💡 해결책: generate_simulation.py를 실행하거나 init 로직을 보강해야 합니다.")
    else:
        print(f"⚠️ 주의: 학생 수가 예상(72,000명)보다 적습니다: {score_cnt}명")

except Exception as e:
    print(f"❌ 데이터 조회 중 오류 발생: {e}")
    print("팁: DB 스키마가 변경되었습니다. 기존 DB를 삭제하고 init_db_data.py를 다시 실행했는지 확인하세요.")

finally:
    conn.close()