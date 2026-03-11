from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import Department, StudentScore

def test_logic():
    """API 로직 직접 테스트"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 첫 번째 학과 가져오기
    dept = session.query(Department).first()
    print(f"테스트 학과: {dept.university.name} - {dept.name} ({dept.division})")
    
    # 테스트 케이스 1: 정상 사용자
    print("\n=== 정상 사용자 테스트 ===")
    score_eng = 75
    score_math = 70
    
    if dept.division == "Humanities":
        total_score = score_eng
    else:
        total_score = score_eng + score_math
    
    print(f"입력: 영어={score_eng}, 수학={score_math}")
    print(f"총점: {total_score} (계열: {dept.division})")
    
    # 허수 체크
    is_spam = (score_eng > 98 or score_math > 98 or total_score > 195)
    print(f"허수 여부: {is_spam}")
    
    if not is_spam:
        # 랭킹 계산
        higher_scores = session.query(StudentScore).filter(
            StudentScore.department_id == dept.id,
            StudentScore.score_total > total_score,
            StudentScore.is_spam == False
        ).count()
        
        rank = higher_scores + 1
        
        total_competitors = session.query(StudentScore).filter(
            StudentScore.department_id == dept.id,
            StudentScore.is_spam == False
        ).count()
        
        top_percent = (rank / total_competitors) * 100
        
        print(f"등수: {rank}")
        print(f"전체 경쟁자: {total_competitors}")
        print(f"상위 백분위: {top_percent:.1f}%")
        
        # 진단
        if top_percent <= 5:
            diagnosis = "최초합 유력"
        elif top_percent <= 15:
            diagnosis = "추가합격 가능"
        elif top_percent <= 30:
            diagnosis = "소신 지원"
        else:
            diagnosis = "위험/상향"
        
        print(f"진단: {diagnosis}")
    
    # 테스트 케이스 2: 허수 사용자
    print("\n=== 허수 사용자 테스트 ===")
    score_eng = 99
    score_math = 95
    total_score = score_eng + score_math
    
    is_spam = (score_eng > 98 or score_math > 98 or total_score > 195)
    print(f"입력: 영어={score_eng}, 수학={score_math}")
    print(f"총점: {total_score}")
    print(f"허수 여부: {is_spam}")
    
    if is_spam:
        print("결과: 1등, 최초합 유력 (가짜 결과)")
    
    session.close()

if __name__ == "__main__":
    test_logic()