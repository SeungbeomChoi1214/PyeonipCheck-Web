import random
from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import Department, StudentScore, University

# 대학 Tier 정의
TIER_S_UNIVERSITIES = [
    "서강대", "성균관대", "한양대", "중앙대", "이화여대", "경희대", 
    "서울시립대", "건국대", "동국대", "홍익대", "한국외대"
]

TIER_A_UNIVERSITIES = [
    "국민대", "숭실대", "세종대", "단국대", "아주대", "인하대", 
    "항공대", "서울과기대", "숙명여대", "성신여대", "광운대"
]

def get_university_tier_score(univ_name):
    """대학 Tier에 따른 평균 점수 반환"""
    if univ_name in TIER_S_UNIVERSITIES:
        return 85
    elif univ_name in TIER_A_UNIVERSITIES:
        return 75
    else:
        return 65

def generate_score(mu=75, sigma=8, min_score=30, max_score=100):
    """정규분포 기반 점수 생성 (30-100 범위 제한)"""
    score = random.gauss(mu, sigma)
    return max(min_score, min(max_score, score))

def generate_simulation():
    """각 학과당 500명의 가상 데이터 생성"""
    print("가상 학생 데이터 생성 시작...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # DB에서 모든 학과 조회
        departments = session.query(Department).join(University).all()
        print(f"총 학과 수: {len(departments)}개")
        
        total_students = 0
        batch_data = []
        
        for dept in departments:
            univ_name = dept.university.name
            dept_name = dept.name
            division = dept.division
            exam_type = dept.exam_type
            
            # 대학 Tier에 따른 평균 점수 설정
            tier_mu = get_university_tier_score(univ_name)
            
            print(f"  처리 중: {univ_name} - {dept_name} ({division}, {exam_type}, Tier 평균: {tier_mu})")
            
            # 학과당 500명 생성
            for _ in range(500):
                # 전형별 점수 생성 로직
                if exam_type == "MATH_ONLY":
                    score_eng = 0
                    score_math = generate_score(mu=tier_mu)
                    score_total = score_math
                elif exam_type == "ENG_ONLY":
                    score_eng = generate_score(mu=tier_mu)
                    score_math = 0
                    score_total = score_eng
                else:  # ENG_MATH
                    score_eng = generate_score(mu=tier_mu)
                    score_math = generate_score(mu=tier_mu)
                    score_total = (score_eng + score_math) / 2
                
                # 배치 데이터에 추가
                batch_data.append({
                    'department_id': dept.id,
                    'score_eng': round(score_eng, 1),
                    'score_math': round(score_math, 1),
                    'score_total': round(score_total, 1),
                    'is_virtual': True
                })
            
            total_students += 500
            
            # 10,000명마다 배치 인서트
            if len(batch_data) >= 10000:
                session.bulk_insert_mappings(StudentScore, batch_data)
                session.commit()
                batch_data = []
                print(f"    진행률: {total_students:,}명 완료")
        
        # 남은 데이터 인서트
        if batch_data:
            session.bulk_insert_mappings(StudentScore, batch_data)
            session.commit()
        
        print(f"총 {total_students:,}명의 가상 학생 데이터 생성 완료!")
        
        # 최종 확인
        total_records = session.query(StudentScore).count()
        virtual_records = session.query(StudentScore).filter(StudentScore.is_virtual == True).count()
        
        print(f"최종 통계:")
        print(f"  - 전체 StudentScore 레코드: {total_records:,}개")
        print(f"  - 가상 데이터 레코드: {virtual_records:,}개")
        print(f"  - 실제 데이터 레코드: {total_records - virtual_records:,}개")
        
    except Exception as e:
        session.rollback()
        print(f"오류 발생: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    generate_simulation()