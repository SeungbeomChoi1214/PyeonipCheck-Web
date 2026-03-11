# 중장기 개선: 데이터 마이그레이션 스크립트 (migrate_to_v2.py)

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.database import SessionLocal
from backend.models import University as OldUniversity, Department as OldDepartment
from models_v2 import University as NewUniversity, Department as NewDepartment, Base

def generate_university_code(name: str, existing_codes: set) -> str:
    """대학 코드 자동 생성"""
    # 한글 대학명을 영문 약어로 변환
    code_map = {
        '건국대학교': 'KU', '한양대학교': 'HY', '중앙대학교': 'CAU',
        '이화여자대학교': 'EW', '서강대학교': 'SG', '성균관대학교': 'SKK',
        # ... 더 많은 매핑 추가
    }
    
    base_code = code_map.get(name, name[:2].upper())
    
    # 중복 방지
    counter = 1
    code = f"{base_code}{counter:03d}"
    while code in existing_codes:
        counter += 1
        code = f"{base_code}{counter:03d}"
    
    return code

def generate_department_code(name: str, division: str) -> str:
    """학과 코드 자동 생성"""
    # 학과명 기반 코드 생성
    code_map = {
        '컴퓨터공학': 'CSE', '경영학': 'BUS', '기계공학': 'ME',
        '전자공학': 'EE', '화학공학': 'CHE', '건축학': 'ARCH',
        # ... 더 많은 매핑 추가
    }
    
    for key, code in code_map.items():
        if key in name:
            return code
    
    # 기본 코드 생성 (첫 글자들 조합)
    words = name.replace('과', '').replace('부', '').replace('학', '').split()
    if len(words) >= 2:
        return ''.join(word[0].upper() for word in words[:3])
    else:
        return name[:3].upper()

def migrate_data():
    """기존 데이터를 새 스키마로 마이그레이션"""
    
    print("🔄 데이터 마이그레이션 시작...")
    
    # 기존 DB 연결
    old_db = SessionLocal()
    
    # 새 DB 생성
    new_engine = create_engine("sqlite:///./university_v2.db")
    Base.metadata.create_all(bind=new_engine)
    NewSession = sessionmaker(bind=new_engine)
    new_db = NewSession()
    
    try:
        # 1. 대학 데이터 마이그레이션
        print("📚 대학 데이터 마이그레이션...")
        old_universities = old_db.query(OldUniversity).all()
        existing_codes = set()
        
        for old_univ in old_universities:
            code = generate_university_code(old_univ.name, existing_codes)
            existing_codes.add(code)
            
            new_univ = NewUniversity(
                code=code,
                name=old_univ.name,
                official_name=old_univ.name,
                tier_group=getattr(old_univ, 'tier_group', None)
            )
            new_db.add(new_univ)
        
        new_db.commit()
        print(f"✅ {len(old_universities)}개 대학 마이그레이션 완료")
        
        # 2. 학과 데이터 마이그레이션
        print("🏫 학과 데이터 마이그레이션...")
        old_departments = old_db.query(OldDepartment).join(OldUniversity).all()
        
        # 새 대학 ID 매핑 생성
        univ_mapping = {}
        new_universities = new_db.query(NewUniversity).all()
        for new_univ in new_universities:
            old_univ = old_db.query(OldUniversity).filter(OldUniversity.name == new_univ.name).first()
            if old_univ:
                univ_mapping[old_univ.id] = new_univ.id
        
        migrated_count = 0
        skipped_count = 0
        
        for old_dept in old_departments:
            if old_dept.university_id not in univ_mapping:
                print(f"⚠️ 스킵: {old_dept.name} (대학 매핑 없음)")
                skipped_count += 1
                continue
            
            # 중복 검사
            existing = new_db.query(NewDepartment).filter(
                NewDepartment.university_id == univ_mapping[old_dept.university_id],
                NewDepartment.name == old_dept.name
            ).first()
            
            if existing:
                print(f"⚠️ 스킵: {old_dept.name} (중복)")
                skipped_count += 1
                continue
            
            code = generate_department_code(old_dept.name, old_dept.division)
            
            new_dept = NewDepartment(
                university_id=univ_mapping[old_dept.university_id],
                code=code,
                name=old_dept.name,
                official_name=old_dept.name,
                division=old_dept.division,
                is_active=True
            )
            new_db.add(new_dept)
            migrated_count += 1
        
        new_db.commit()
        print(f"✅ {migrated_count}개 학과 마이그레이션 완료, {skipped_count}개 스킵")
        
        # 3. 데이터 검증
        print("🔍 데이터 검증...")
        total_univs = new_db.query(NewUniversity).count()
        total_depts = new_db.query(NewDepartment).count()
        
        # 중복 검사
        duplicate_check = new_db.execute(text("""
            SELECT university_id, name, COUNT(*) as cnt 
            FROM departments 
            GROUP BY university_id, name 
            HAVING COUNT(*) > 1
        """)).fetchall()
        
        print(f"📊 마이그레이션 결과:")
        print(f"  - 총 대학: {total_univs}개")
        print(f"  - 총 학과: {total_depts}개")
        print(f"  - 중복 학과: {len(duplicate_check)}개")
        
        if duplicate_check:
            print("⚠️ 중복 학과 발견:")
            for dup in duplicate_check:
                print(f"    - 대학ID {dup[0]}: {dup[1]} ({dup[2]}개)")
        
    except Exception as e:
        new_db.rollback()
        print(f"❌ 마이그레이션 실패: {e}")
        import traceback
        traceback.print_exc()
    finally:
        old_db.close()
        new_db.close()

def create_integrity_constraints():
    """데이터 무결성 제약 조건 추가"""
    engine = create_engine("sqlite:///./university_v2.db")
    
    with engine.connect() as conn:
        # 추가 제약 조건들
        constraints = [
            "CREATE INDEX IF NOT EXISTS idx_dept_full_code ON departments(university_id, code);",
            "CREATE INDEX IF NOT EXISTS idx_dept_active ON departments(is_active);",
            "CREATE INDEX IF NOT EXISTS idx_score_dept_virtual ON student_scores(department_id, is_virtual);",
        ]
        
        for constraint in constraints:
            try:
                conn.execute(text(constraint))
                print(f"✅ 제약 조건 추가: {constraint[:50]}...")
            except Exception as e:
                print(f"⚠️ 제약 조건 실패: {e}")

if __name__ == "__main__":
    migrate_data()
    create_integrity_constraints()
    print("🎉 마이그레이션 완료!")