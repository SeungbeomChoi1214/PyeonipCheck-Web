import pandas as pd
import re
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def parse_university_data(file_path):
    """텍스트 파일을 파싱하여 대학 데이터를 추출"""
    
    data = []
    current_university = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        logging.error(f"파일 읽기 실패: {e}")
        return []
    
    # 대학명 추출 패턴
    university_pattern = r'\[\[\s*대학명:\s*([^]]+)\s*모집요강\.pdf\s*\]\]'
    
    # 모집단위 테이블 패턴들
    dept_patterns = [
        # 동국대 스타일: 대학 | 모집단위 | | 계열 | 일반편입 | 학사편입
        r'([^|]+)\s*\|\s*([^|]+)\s*\|\s*[^|]*\s*\|\s*(인문|자연|예체능)\s*\|\s*([0-9]*)\s*\|\s*([0-9]*)',
        # 건국대 스타일: 모집단위 | 계열 | 일반편입 | 우선선발 | 학사편입
        r'([^|]+)\s*\|\s*(인문|자연|예체능)\s*\|\s*([0-9]+)\s*\|\s*[^|]*\s*\|\s*([0-9]*)',
        # 한양대 스타일: 모집단위(학과) | 일반편입학 | 학사편입학
        r'([^|]+)\s*\|\s*([0-9]+)\s*\|\s*([0-9]+)',
        # 홍익대 스타일: 모집단위 | | 일반 | 학사
        r'([^|]+)\s*\|\s*[^|]*\s*\|\s*([0-9]+)\s*\|\s*([0-9]*)'
    ]
    
    sections = re.split(university_pattern, content)
    
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            university_name = sections[i].strip()
            university_content = sections[i + 1]
            
            logging.info(f"처리 중: {university_name}")
            
            # 각 라인별로 처리
            lines = university_content.split('\n')
            
            for line_num, line in enumerate(lines):
                line = line.strip()
                if not line or '----' in line or '===' in line:
                    continue
                
                # 각 패턴으로 시도
                matched = False
                
                for pattern in dept_patterns:
                    matches = re.findall(pattern, line)
                    
                    for match in matches:
                        try:
                            if len(match) >= 3:
                                # 기본 정보 추출
                                dept_name = match[0].strip()
                                
                                # 숫자가 아닌 문자가 포함된 학과명 필터링
                                if not dept_name or dept_name in ['대학', '모집단위', '계열', '합계', '총계']:
                                    continue
                                
                                # 계열 정보 추출
                                category = None
                                general_count = 0
                                bachelor_count = 0
                                
                                if len(match) == 5:  # 동국대 스타일
                                    category = match[2] if match[2] in ['인문', '자연', '예체능'] else '인문'
                                    general_count = int(match[3]) if match[3].isdigit() else 0
                                    bachelor_count = int(match[4]) if match[4].isdigit() else 0
                                elif len(match) == 4:  # 건국대 스타일
                                    if match[1] in ['인문', '자연', '예체능']:
                                        category = match[1]
                                        general_count = int(match[2]) if match[2].isdigit() else 0
                                        bachelor_count = int(match[3]) if match[3].isdigit() else 0
                                    else:
                                        # 한양대 스타일 (계열 정보 추론)
                                        category = infer_category(dept_name)
                                        general_count = int(match[1]) if match[1].isdigit() else 0
                                        bachelor_count = int(match[2]) if match[2].isdigit() else 0
                                elif len(match) == 3:  # 기타 스타일
                                    category = infer_category(dept_name)
                                    general_count = int(match[1]) if match[1].isdigit() else 0
                                    bachelor_count = int(match[2]) if match[2].isdigit() else 0
                                
                                # 유효한 데이터만 추가
                                if dept_name and (general_count > 0 or bachelor_count > 0):
                                    data.append({
                                        'university_name': university_name,
                                        'department_name': dept_name,
                                        'recruitment_count_general': general_count,
                                        'recruitment_count_bachelor': bachelor_count,
                                        'score_cutoff_general': '',  # 빈칸
                                        'score_cutoff_bachelor': '',  # 빈칸
                                        'category': category or '인문'
                                    })
                                    matched = True
                        
                        except (ValueError, IndexError) as e:
                            logging.warning(f"라인 파싱 실패 (라인 {line_num}): {line[:50]}... - {e}")
                            continue
                
                if not matched and any(keyword in line for keyword in ['학과', '학부', '전공']):
                    logging.debug(f"매칭되지 않은 라인: {line[:100]}...")
    
    logging.info(f"총 {len(data)}개의 데이터 추출 완료")
    return data

def infer_category(dept_name):
    """학과명을 기반으로 계열 추론"""
    
    # 자연계열 키워드
    natural_keywords = [
        '공학', '과학', '수학', '물리', '화학', '생명', '의학', '간호', '컴퓨터', 
        '전자', '전기', '기계', '건축', '토목', '환경', '재료', '화공', '바이오',
        '정보', '소프트웨어', 'AI', '데이터', '시스템', '에너지', '반도체'
    ]
    
    # 예체능계열 키워드
    arts_keywords = [
        '미술', '음악', '체육', '예술', '디자인', '영상', '연극', '영화', '무용',
        '애니메이션', '게임', '방송', '미디어'
    ]
    
    dept_name_lower = dept_name.lower()
    
    # 예체능 먼저 체크
    for keyword in arts_keywords:
        if keyword in dept_name:
            return '예체능'
    
    # 자연계열 체크
    for keyword in natural_keywords:
        if keyword in dept_name:
            return '자연'
    
    # 기본값은 인문계열
    return '인문'

def create_excel_file(data, output_file):
    """데이터를 엑셀 파일로 저장"""
    
    if not data:
        logging.error("저장할 데이터가 없습니다.")
        return
    
    try:
        df = pd.DataFrame(data)
        
        # 중복 제거 (같은 대학, 같은 학과)
        df = df.drop_duplicates(subset=['university_name', 'department_name'])
        
        # 정렬
        df = df.sort_values(['university_name', 'department_name'])
        
        # 엑셀 파일로 저장
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Master_Data', index=False)
        
        logging.info(f"엑셀 파일 생성 완료: {output_file}")
        logging.info(f"총 {len(df)}개 행, {len(df.columns)}개 열")
        
        # 대학별 통계
        university_stats = df.groupby('university_name').agg({
            'department_name': 'count',
            'recruitment_count_general': 'sum',
            'recruitment_count_bachelor': 'sum'
        }).round(0)
        
        print("\n=== 대학별 통계 ===")
        print(university_stats)
        
    except Exception as e:
        logging.error(f"엑셀 파일 생성 실패: {e}")

def main():
    """메인 함수"""
    
    input_file = 'all_tables_raw.txt'
    output_file = 'Master_Data.xlsx'
    
    print("📊 대학 모집요강 데이터 변환 시작...")
    
    # 데이터 파싱
    data = parse_university_data(input_file)
    
    if data:
        # 엑셀 파일 생성
        create_excel_file(data, output_file)
        print(f"✅ 변환 완료: {output_file}")
    else:
        print("❌ 추출된 데이터가 없습니다.")

if __name__ == "__main__":
    main()