import pandas as pd
import os
from backend.database import SessionLocal, engine
from backend.models import University, Base

# 1. 기존 DB 파일이 꼬이는 것을 방지하기 위해 테이블을 새로 만듭니다.
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def load_data():
    db = SessionLocal()
    filename = "universities_data.xlsx"
    
    if not os.path.exists(filename):
        print(f"❌ '{filename}' 파일이 없습니다! make_template.py를 먼저 실행하세요.")
        return

    try:
        df = pd.read_excel(filename)
        df = df.fillna(0) # 빈값 처리
    except Exception as e:
        print(f"❌ 엑셀 파일 읽기 실패: {e}")
        return

    print(f"🚀 '{filename}'에서 {len(df)}개 데이터를 읽어와 'university.db'에 적재합니다...")

    count = 0
    for index, row in df.iterrows():
        try:
            # 📌 변수명 일치 작업 (공백 제거 포함)
            uni = University(
                university=str(row['university']).strip(),
                department=str(row['department']).strip(),
                division=str(row['division']).strip(),
                
                stage1_eng=float(row['stage1_eng']),
                stage1_math=float(row['stage1_math']),
                stage1_cut=float(row['stage1_cut']),
                
                has_stage2=bool(row['has_stage2']),
                stage2_keep=float(row['stage2_keep']),
                stage2_doc=float(row['stage2_doc']),
                stage2_int=float(row['stage2_int']),
                
                final_cut=float(row['final_cut'])
            )
            db.add(uni)
            count += 1
        except Exception as e:
            print(f"⚠️ 에러 발생 (행 {index}): {e}")

    db.commit()
    db.close()
    print(f"🎉 성공! 총 {count}개 데이터가 'university.db'에 저장되었습니다.")

if __name__ == "__main__":
    load_data()