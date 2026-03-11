import requests
import json
from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import Department

def test_api():
    """API 테스트"""
    # 먼저 학과 ID 확인
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 첫 번째 학과 가져오기
    dept = session.query(Department).first()
    if not dept:
        print("학과 데이터가 없습니다.")
        return
    
    print(f"테스트 학과: {dept.university.name} - {dept.name} ({dept.division})")
    print(f"학과 ID: {dept.id}")
    
    session.close()
    
    # API 테스트 데이터
    test_cases = [
        {
            "name": "정상 사용자 (인문계)",
            "data": {"dept_id": dept.id, "score_eng": 75, "score_math": 0}
        },
        {
            "name": "허수 사용자 (영어 99점)",
            "data": {"dept_id": dept.id, "score_eng": 99, "score_math": 70}
        },
        {
            "name": "허수 사용자 (총점 200점)",
            "data": {"dept_id": dept.id, "score_eng": 100, "score_math": 100}
        }
    ]
    
    base_url = "http://localhost:8000"
    
    for test_case in test_cases:
        print(f"\n=== {test_case['name']} ===")
        try:
            response = requests.post(f"{base_url}/predict", json=test_case['data'])
            if response.status_code == 200:
                result = response.json()
                print(f"등수: {result['rank']}")
                print(f"전체 경쟁자: {result['total_competitors']}")
                print(f"상위 백분위: {result['top_percent']}%")
                print(f"진단: {result['diagnosis']}")
            else:
                print(f"오류: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            print("API 서버가 실행되지 않았습니다. 먼저 'py main.py'로 서버를 시작하세요.")
            break
        except Exception as e:
            print(f"테스트 오류: {e}")

if __name__ == "__main__":
    test_api()