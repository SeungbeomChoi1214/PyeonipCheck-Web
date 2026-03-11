import sqlite3

# DB 파일 경로 (backend 폴더 안에 있다고 가정)
db_path = "backend/university.db" 

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. 수원대학교 ID 찾기
    cursor.execute("SELECT id FROM universities WHERE name LIKE '%수원대%'")
    univ = cursor.fetchone()
    
    if univ:
        univ_id = univ[0]
        print(f"수원대학교 ID 발견: {univ_id}")

        # 2. 자연계열(Natural) 전형을 '영어+수학'으로 수정
        # (기존에 max_score_eng가 0이었다면 100으로 변경하여 영어 반영 활성화)
        sql = """
        UPDATE admission_tracks 
        SET max_score_eng = 100, max_score_math = 100 
        WHERE university_id = ? AND track_type LIKE '%NATURAL%'
        """
        cursor.execute(sql, (univ_id,))
        
        if cursor.rowcount > 0:
            print("✅ 수원대학교 자연계열 전형 수정 완료! (영어+수학)")
            conn.commit()
        else:
            print("⚠️ 수정할 전형 데이터를 찾지 못했습니다.")
            
    else:
        print("❌ 수원대학교를 DB에서 찾을 수 없습니다.")

    conn.close()

except Exception as e:
    print(f"에러 발생: {e}")
    