from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import University, Department

def test_new_endpoints():
    """새로운 API 엔드포인트 로직 테스트"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=== 대학 목록 API 테스트 ===")
    universities = session.query(University).all()
    print(f"대학 수: {len(universities)}")
    for univ in universities[:5]:
        print(f"  ID: {univ.id}, 이름: {univ.name}")
    
    print("\n=== 학과 목록 API 테스트 ===")
    if universities:
        first_univ = universities[0]
        departments = session.query(Department).filter(Department.university_id == first_univ.id).all()
        print(f"{first_univ.name} 학과 수: {len(departments)}")
        for dept in departments[:5]:
            print(f"  ID: {dept.id}, 이름: {dept.name}, 계열: {dept.division}")
    
    session.close()

if __name__ == "__main__":
    test_new_endpoints()