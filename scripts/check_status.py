import sys
import os

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.database import SessionLocal
from backend.models import University, Department, StudentScore
from sqlalchemy import func

def check_status():
    """데이터베이스 상태 검증"""
    
    print("📊 데이터베이스 상태 검증 시작...")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # 1. 각 테이블의 총 행 개수
        univ_count = db.query(University).count()
        dept_count = db.query(Department).count()
        student_count = db.query(StudentScore).count()
        
        print("📈 테이블별 데이터 개수:")
        print(f"  - University: {univ_count:,}개")
        print(f"  - Department: {dept_count:,}개")
        print(f"  - StudentScore: {student_count:,}개")
        print()
        
        # 2. 샘플 데이터 조회 (건국대 학과 하나)
        konkuk_dept = db.query(Department).join(University).filter(
            University.name.like('%건국%')
        ).first()
        
        if konkuk_dept:
            sample_students = db.query(StudentScore).filter(
                StudentScore.department_id == konkuk_dept.id
            ).limit(5).all()
            
            print(f"🎯 샘플 데이터 ({konkuk_dept.university.name} - {konkuk_dept.name}):")
            for i, student in enumerate(sample_students, 1):
                print(f"  {i}. 영어: {student.score_eng}, 수학: {student.score_math}, "
                      f"총점: {student.score_total}, 가상데이터: {student.is_virtual}")
            print()
        
        # 3. 가상 데이터 비율 통계
        virtual_count = db.query(StudentScore).filter(StudentScore.is_virtual == True).count()
        virtual_ratio = (virtual_count / student_count * 100) if student_count > 0 else 0
        
        print("📊 가상 데이터 통계:")
        print(f"  - 전체 학생: {student_count:,}명")
        print(f"  - 가상 학생: {virtual_count:,}명")
        print(f"  - 가상 데이터 비율: {virtual_ratio:.1f}%")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        db.close()
    
    print("=" * 50)
    print("✅ 검증 완료!")

if __name__ == "__main__":
    check_status()