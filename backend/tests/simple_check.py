from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import Department, StudentScore, University

def check_database():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        univ_count = session.query(University).count()
        print(f"대학 수: {univ_count}개")
        
        dept_count = session.query(Department).count()
        print(f"학과 수: {dept_count}개")
        
        total_scores = session.query(StudentScore).count()
        virtual_scores = session.query(StudentScore).filter(StudentScore.is_virtual == True).count()
        real_scores = total_scores - virtual_scores
        
        print(f"총 학생 점수 레코드: {total_scores:,}개")
        print(f"가상 데이터: {virtual_scores:,}개")
        print(f"실제 데이터: {real_scores:,}개")
        
        print("\n대학별 학과 수:")
        universities = session.query(University).all()
        for univ in universities[:5]:
            dept_count = session.query(Department).filter(Department.university_id == univ.id).count()
            print(f"  {univ.name}: {dept_count}개 학과")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_database()