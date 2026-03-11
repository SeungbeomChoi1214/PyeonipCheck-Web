import pandas as pd
from sqlalchemy.orm import Session
import backend.models as models, backend.database as database

models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()

# 대학 생성
univ = db.query(models.University).filter(models.University.name == "가천대학교").first()
if not univ:
    univ = models.University(name="가천대학교")
    db.add(univ)
    db.commit()

# 더미 데이터 생성 (CSV 파일 없을 경우 대비)
dummy_data = {
    "모집단위": ["경영학전공", "컴퓨터공학전공", "화공생명공학전공"],
    "전형방법": ["영어고사\n100%", "수학고사\n100%", "수학고사\n100%"]
}
df = pd.DataFrame(dummy_data)

for _, row in df.iterrows():
    dept_name = row['모집단위']
    method = row['전형방법']
    
    # 중복 체크
    if db.query(models.Department).filter(models.Department.name == dept_name).first(): continue

    dept = models.Department(univ_id=univ.id, name=dept_name)
    db.add(dept)
    db.commit()

    # 규칙 설정 (가천대는 1단계 100%)
    eng_ratio = 1.0 if "영어" in method else 0.0
    math_ratio = 1.0 if "수학" in method else 0.0

    rule = models.ScoringRule(
        dept_id=dept.id,
        stage1_eng_ratio=eng_ratio,
        stage1_math_ratio=math_ratio,
        has_stage2=False, # 2단계 없음
        cut_off=70.0      # 임시 컷
    )
    db.add(rule)

db.commit()
print("✅ 가천대(범용 엔진용) 데이터 적재 완료!")