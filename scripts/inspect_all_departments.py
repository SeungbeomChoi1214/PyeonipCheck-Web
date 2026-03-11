import sys
import os
# 현재 스크립트의 부모의 부모 경로(프로젝트 루트)를 path에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from backend.database import SessionLocal
from backend.models import University, Department

def inspect_all_departments():
    """DB에 저장된 모든 학과명 검사"""
    
    print("🔍 DB 학과명 검사 시작...")
    
    db = SessionLocal()
    
    try:
        # 모든 학과 조회 (대학명과 함께)
        departments = db.query(Department).join(University).order_by(
            University.name, Department.name
        ).all()
        
        print(f"📊 총 {len(departments)}개 학과 발견")
        
        # 결과를 파일로 저장
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_file = os.path.join(output_dir, "all_departments_list.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for dept in departments:
                line = f"[{dept.university.name}] {dept.name} ({dept.division})"
                f.write(line + "\\n")
                print(line)
        
        print(f"\\n✅ 검사 완료! 결과 저장: {output_file}")
        
        # 통계 출력
        total_univs = db.query(University).count()
        natural_count = len([d for d in departments if d.division == "Natural"])
        humanities_count = len([d for d in departments if d.division == "Humanities"])
        
        print(f"\\n📈 통계:")
        print(f"  - 총 대학: {total_univs}개")
        print(f"  - 총 학과: {len(departments)}개")
        print(f"  - 자연계: {natural_count}개")
        print(f"  - 인문계: {humanities_count}개")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    inspect_all_departments()