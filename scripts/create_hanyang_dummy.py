from sqlalchemy.orm import Session
import backend.models as models, backend.database as database

# 1. DB 테이블 생성 (필수)
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()
print("🔄 한양대 데이터 적재 시작...")

# 2. 대학 정보 생성
hanyang = db.query(models.University).filter(models.University.name == "한양대학교").first()
if not hanyang:
    hanyang = models.University(name="한양대학교")
    db.add(hanyang)
    db.commit()

# 3. 학과 데이터
data = [
    {
        "name": "경영학부", "div": "Humanities", 
        "s1_eng": 1.0, "s1_math": 0.0, "s1_cut": 80.0, 
        "s2_keep": 0.7, "s2_doc": 0.3, "final_cut": 88.0 # s2_keep으로 변경!
    },
    {
        "name": "기계공학부", "div": "Natural", 
        "s1_eng": 0.0, "s1_math": 1.0, "s1_cut": 75.0, 
        "s2_keep": 0.7, "s2_doc": 0.3, "final_cut": 85.0
    }
]

for item in data:
    # 중복 방지
    existing = db.query(models.Department).filter(models.Department.name == item["name"]).first()
    if existing: continue

    dept = models.Department(univ_id=hanyang.id, name=item["name"], division=item["div"])
    db.add(dept)
    db.commit()
    
    # 규칙 추가 (새 모델 적용)
    rule = models.ScoringRule(
        dept_id=dept.id,
        stage1_eng_ratio=item["s1_eng"],
        stage1_math_ratio=item["s1_math"],
        has_stage2=True,
        stage1_cutoff=item["s1_cut"],
        
        # 👇 [수정된 부분] 옛날 이름: stage2_exam_ratio -> 새 이름: stage2_keep_ratio
        stage2_keep_ratio=item["s2_keep"], 
        stage2_doc_ratio=item["s2_doc"],
        
        cut_off=item["final_cut"]
    )
    db.add(rule)

db.commit()
print("✅ 한양대(범용 엔진용) 데이터 적재 완료!")