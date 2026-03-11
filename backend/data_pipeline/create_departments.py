from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import Department, University

def create_sample_departments():
    """36개 대학에 기본 학과 데이터 생성"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 기본 학과 목록 (인문/자연 계열)
    humanities_depts = [
        "국어국문학과", "영어영문학과", "사학과", "철학과", "경영학과", 
        "경제학과", "법학과", "행정학과", "사회학과", "심리학과",
        "교육학과", "언론정보학과", "정치외교학과", "문화콘텐츠학과"
    ]
    
    natural_depts = [
        "컴퓨터공학과", "전자공학과", "기계공학과", "화학공학과", "건축학과",
        "수학과", "물리학과", "화학과", "생물학과", "의학과",
        "간호학과", "약학과", "건설환경공학과", "신소재공학과"
    ]
    
    try:
        universities = session.query(University).all()
        print(f"대학 수: {len(universities)}개")
        
        total_depts = 0
        
        for univ in universities:
            print(f"처리 중: {univ.name}")
            
            # 각 대학에 인문계열 학과 5-8개 추가
            import random
            selected_hum = random.sample(humanities_depts, random.randint(5, 8))
            for dept_name in selected_hum:
                dept = Department(
                    university_id=univ.id,
                    name=dept_name,
                    division="Humanities",
                    recruit_type="General",
                    popularity_offset=0.0,
                    stage1_eng_ratio=100.0,
                    stage1_math_ratio=0.0,
                    has_stage2=False
                )
                session.add(dept)
                total_depts += 1
            
            # 각 대학에 자연계열 학과 5-8개 추가
            selected_nat = random.sample(natural_depts, random.randint(5, 8))
            for dept_name in selected_nat:
                dept = Department(
                    university_id=univ.id,
                    name=dept_name,
                    division="Natural",
                    recruit_type="General",
                    popularity_offset=0.0,
                    stage1_eng_ratio=50.0,
                    stage1_math_ratio=50.0,
                    has_stage2=False
                )
                session.add(dept)
                total_depts += 1
        
        session.commit()
        print(f"총 {total_depts}개 학과 생성 완료!")
        
        # 확인
        final_count = session.query(Department).count()
        print(f"최종 학과 수: {final_count}개")
        
    except Exception as e:
        session.rollback()
        print(f"오류 발생: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    create_sample_departments()