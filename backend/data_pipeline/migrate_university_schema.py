"""
University 스키마 업데이트: tier 및 waitlist_ratio 컬럼 추가
"""
import sqlite3
import os

def migrate_university_schema():
    """University 테이블에 tier와 waitlist_ratio 컬럼 추가"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'university.db')
    
    if not os.path.exists(db_path):
        print("❌ university.db 파일이 존재하지 않습니다.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 기존 컬럼 확인
        cursor.execute("PRAGMA table_info(universities)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # tier 컬럼 추가
        if 'tier' not in columns:
            cursor.execute("ALTER TABLE universities ADD COLUMN tier TEXT DEFAULT 'B'")
            print("✅ tier 컬럼 추가 완료")
        else:
            print("ℹ️ tier 컬럼이 이미 존재합니다")
        
        # waitlist_ratio 컬럼 추가
        if 'waitlist_ratio' not in columns:
            cursor.execute("ALTER TABLE universities ADD COLUMN waitlist_ratio REAL DEFAULT 1.5")
            print("✅ waitlist_ratio 컬럼 추가 완료")
        else:
            print("ℹ️ waitlist_ratio 컬럼이 이미 존재합니다")
        
        # is_real_data 컬럼 추가
        if 'is_real_data' not in columns:
            cursor.execute("ALTER TABLE universities ADD COLUMN is_real_data INTEGER DEFAULT 0")
            print("✅ is_real_data 컬럼 추가 완료")
        else:
            print("ℹ️ is_real_data 컬럼이 이미 존재합니다")
        
        # 티어별 waitlist_ratio 초기값 설정
        cursor.execute("""
            UPDATE universities 
            SET waitlist_ratio = CASE 
                WHEN tier_group IN ('S', 'A') THEN 2.5
                WHEN tier_group = 'B' THEN 1.5
                ELSE 1.0
            END
            WHERE waitlist_ratio = 1.5
        """)
        
        # tier 초기값 설정 (tier_group 기반)
        cursor.execute("""
            UPDATE universities 
            SET tier = tier_group
            WHERE tier = 'B'
        """)
        
        conn.commit()
        print("🎉 스키마 마이그레이션 완료")
        
        # 결과 확인
        cursor.execute("SELECT name, tier, waitlist_ratio FROM universities LIMIT 5")
        results = cursor.fetchall()
        print("\n📊 샘플 데이터:")
        for row in results:
            print(f"  {row[0]}: tier={row[1]}, waitlist_ratio={row[2]}")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ 마이그레이션 실패: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_university_schema()