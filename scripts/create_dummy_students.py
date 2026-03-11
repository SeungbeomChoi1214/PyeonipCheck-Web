import random
from sqlalchemy.orm import Session
import backend.models as models, backend.database as database

models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()

print("🔄 경쟁자(학생) 데이터 생성 중...")

# 학생 생성 함수
def create_student(univ, dept, eng_min, eng_max, math_min, math_max):
    # 점수 랜덤 생성
    eng = random.uniform(eng_min, eng_max)
    math = random.uniform(math_min, math_max)
    gpa = random.uniform(3.0, 4.5)
    
    # 총점 계산 (한양대 로직 하드코딩: 1단계*0.7 + 서류*0.3)
    # 실제로는 DB rule을 읽어와야 하지만, 더미 생성을 위해 약식으로 계산
    exam_score = eng if eng_max > 0 else math
    doc_score = (gpa / 4.5) * 100
    total = (exam_score * 0.7) + (doc_score * 0.3)

    student = models.StudentScore(
        univ_name=univ,
        dept_name=dept,
        eng_score=round(eng, 1),
        math_score=round(math, 1),
        gpa_score=round(gpa, 2),
        total_score=round(total, 2)
    )
    db.add(student)

# 1. 경영학부 (영어형) 50명
for _ in range(50):
    create_student("한양대학교", "경영학부", 60, 100, 0, 0)

# 2. 기계공학부 (수학형) 50명
for _ in range(50):
    create_student("한양대학교", "기계공학부", 0, 0, 60, 100)

db.commit()
print("🎉 경쟁자 100명 투입 완료!")