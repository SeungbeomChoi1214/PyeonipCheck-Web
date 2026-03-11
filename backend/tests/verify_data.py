from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import University, Department, StudentScore

def verify_data():
    """데이터베이스 데이터 검증"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("데이터베이스 검증 시작...")
        
        # 대학 수 확인
        univ_count = session.query(University).count()
        print(f"대학 수: {univ_count}개")
        
        # 학과 수 확인
        dept_count = session.query(Department).count()
        print(f"학과 수: {dept_count}개")
        
        # 학생 점수 데이터 확인
        total_scores = session.query(StudentScore).count()
        virtual_scores = session.query(StudentScore).filter(StudentScore.is_virtual == True).count()
        real_scores = total_scores - virtual_scores
        
        print(f"총 학생 점수 레코드: {total_scores:,}개")
        print(f"가상 데이터: {virtual_scores:,}개")
        print(f"실제 데이터: {real_scores:,}개")
        
        # 대학별 학과 수 확인 (상위 10개)
        print("\n대학별 학과 수 (상위 10개):")
        universities = session.query(University).limit(10).all()
        for univ in universities:
            dept_count = session.query(Department).filter(Department.university_id == univ.id).count()
            print(f"  {univ.name}: {dept_count}개 학과")
        
        # 계열별 학과 수
        humanities_count = session.query(Department).filter(Department.division == 'Humanities').count()
        natural_count = session.query(Department).filter(Department.division == 'Natural').count()
        
        print(f"\n계열별 학과 수:")
        print(f"  인문계열: {humanities_count}개")
        print(f"  자연계열: {natural_count}개")
        
        print("\n데이터베이스 검증 완료!")
        
    except Exception as e:
        print(f"검증 중 오류 발생: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    verify_data()