import sys
import os
import re

# TXT 파일에서 대학별 학과 데이터 추출 테스트
def test_txt_parsing():
    """TXT 파일 파싱 테스트"""
    
    txt_file_path = 'all_tables_raw.txt'
    if not os.path.exists(txt_file_path):
        txt_file_path = os.path.join('raw_data', 'all_tables_raw.txt')
    
    if not os.path.exists(txt_file_path):
        print("❌ TXT 파일을 찾을 수 없습니다.")
        return
    
    print(f"📁 TXT 파일 분석: {txt_file_path}")
    
    # 보유 대학 리스트
    target_universities = [
        '가천대', '가톨릭대', '강원대', '건국대', '경기대', '경희대',
        '광운대', '국민대', '단국대', '동국대', '명지대', '부산대',
        '상명대', '서강대', '서울시립대', '성균관대', '세종대', '수원대',
        '숙명여대', '숭실대', '용인대', '이화여대', '인천대', '인하대',
        '전남대', '전북대', '중앙대', '충남대', '충북대', '한국공학대',
        '한국외대', '한양대', '홍익대'
    ]
    
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📊 파일 크기: {len(content):,} 문자")
        
        # 대학별 데이터 찾기
        found_universities = {}
        lines = content.split('\\n')
        
        for line in lines[:100]:  # 처음 100줄만 샘플 확인
            line = line.strip()
            if not line:
                continue
                
            for univ in target_universities:
                if univ in line:
                    if univ not in found_universities:
                        found_universities[univ] = []
                    found_universities[univ].append(line[:100])  # 처음 100자만
        
        print(f"\\n🏫 발견된 대학: {len(found_universities)}개")
        for univ, samples in found_universities.items():
            print(f"  - {univ}: {len(samples)}개 라인 발견")
            if samples:
                print(f"    예시: {samples[0]}")
        
        # 학과명으로 보이는 패턴 찾기
        dept_patterns = []
        for line in lines[:200]:
            line = line.strip()
            if (len(line) > 2 and len(line) < 50 and 
                any(keyword in line for keyword in ['학과', '학부', '전공']) and
                not any(skip in line for skip in ['모집요강', 'pdf', '페이지'])):
                dept_patterns.append(line)
        
        print(f"\\n📚 학과명 패턴 샘플 ({len(dept_patterns)}개):")
        for pattern in dept_patterns[:10]:
            print(f"  - {pattern}")
            
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")

if __name__ == "__main__":
    test_txt_parsing()