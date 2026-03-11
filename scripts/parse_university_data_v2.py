import pandas as pd
import re
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def classify_category(dept_name):
    """학과명을 기반으로 계열 자동 분류"""
    
    # 인문계열 키워드
    humanities_keywords = ['국어', '영어', '철학', '사학', '경영', '경제', '사회', '법', 
                          '문학', '어문', '정치', '행정', '외교', '상담', '무역', '글로벌']
    
    # 자연계열 키워드  
    natural_keywords = ['수학', '물리', '화학', '생명', '공학', '컴퓨터', '전자', '기계',
                       '건축', '토목', '환경', '재료', '융합', '반도체', '소프트웨어', 
                       '데이터', '사이언스', '시스템', '과학', '바이오']
    
    # 예체능계열 키워드
    arts_keywords = ['미술', '디자인', '체육', '음악', '무용', '연극', '영화', '도예',
                    '예술', '공연', '뮤지컬', '피아노', '성악', '국악']
    
    dept_lower = dept_name.lower()
    
    # 예체능 먼저 체크
    for keyword in arts_keywords:
        if keyword in dept_name:
            return '예체능'
    
    # 자연계열 체크
    for keyword in natural_keywords:
        if keyword in dept_name:
            return '자연'
    
    # 인문계열 체크
    for keyword in humanities_keywords:
        if keyword in dept_name:
            return '인문'
    
    return '기타'

def extract_numbers(text):
    """텍스트에서 숫자 추출"""
    numbers = re.findall(r'\d+', text)
    return [int(n) for n in numbers if int(n) > 0 and int(n) < 1000]  # 합리적인 범위의 숫자만

def is_university_line(line):
    """대학명 라인인지 판단"""
    line_clean = line.strip()
    
    # 대학교로 끝나거나 대학이 포함되고 숫자가 없는 경우
    if (line_clean.endswith('대학교') or '대학' in line_clean) and not re.search(r'\d', line_clean):
        # 불필요한 단어들 제외
        exclude_words = ['모집단위', '계열', '정원', '합계', '총계', '전형', '선발']
        if not any(word in line_clean for word in exclude_words):
            return True
    
    return False

def is_department_line(line):
    """학과 데이터 라인인지 판단"""
    line_clean = line.strip()
    
    # 숫자가 포함되어 있고, 학과명으로 보이는 패턴
    if re.search(r'\d', line_clean):
        # 학과/학부 관련 키워드가 있거나 일반적인 학과명 패턴
        dept_indicators = ['학과', '학부', '전공', '과', '부']
        if any(indicator in line_clean for indicator in dept_indicators):
            return True
        
        # 또는 파이프(|)로 구분된 테이블 형태
        if '|' in line_clean and len(line_clean.split('|')) >= 3:
            return True
    
    return False

def parse_department_line(line, current_university):
    """학과 라인에서 데이터 추출"""
    try:
        line_clean = line.strip()
        
        # 파이프로 구분된 경우
        if '|' in line_clean:
            parts = [part.strip() for part in line_clean.split('|')]
            
            # 학과명 찾기 (첫 번째 의미있는 부분)
            dept_name = None
            for part in parts:
                if part and not part.isdigit() and len(part) > 1:
                    # 불필요한 단어 제외
                    if part not in ['계열', '대학', '모집단위', '정원내', '정원외', '일반편입', '학사편입']:
                        dept_name = part
                        break
        else:
            # 파이프가 없는 경우, 첫 번째 단어들을 학과명으로 추정
            words = line_clean.split()
            dept_name = ' '.join(words[:2]) if len(words) >= 2 else words[0] if words else None
        
        if not dept_name:
            return None
        
        # 숫자 추출
        numbers = extract_numbers(line_clean)
        
        # 계열 분류
        category = classify_category(dept_name)
        
        return {
            'university_name': current_university or '미상',
            'department_name': dept_name,
            'category': category,
            'recruitment_count_general': numbers[0] if len(numbers) > 0 else 0,
            'recruitment_count_bachelor': numbers[1] if len(numbers) > 1 else 0,
            'score_cutoff_general': '',
            'score_cutoff_bachelor': '',
            'note': '',
            'raw_text_check': line_clean
        }
        
    except Exception as e:
        logging.warning(f"라인 파싱 실패: {line[:50]}... - {e}")
        return None

def parse_university_data(file_path):
    """텍스트 파일을 한 줄씩 읽어서 파싱"""
    
    data = []
    current_university = None
    line_count = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line_count += 1
                line = line.strip()
                
                # 빈 줄이나 구분선 건너뛰기
                if not line or '----' in line or '====' in line or line.startswith('---'):
                    continue
                
                try:
                    # 대학명 식별
                    if is_university_line(line):
                        # 대학명 추출
                        if '대학교' in line:
                            current_university = line.split('대학교')[0].strip() + '대학교'
                        elif '대학' in line:
                            current_university = line.split('대학')[0].strip() + '대학'
                        
                        logging.info(f"대학명 발견: {current_university}")
                        continue
                    
                    # 학과 데이터 식별 및 파싱
                    if is_department_line(line):
                        dept_data = parse_department_line(line, current_university)
                        if dept_data:
                            # 유효한 데이터만 추가 (모집인원이 있는 경우)
                            if dept_data['recruitment_count_general'] > 0 or dept_data['recruitment_count_bachelor'] > 0:
                                data.append(dept_data)
                                logging.debug(f"데이터 추가: {dept_data['department_name']}")
                
                except Exception as e:
                    logging.warning(f"라인 {line_count} 처리 실패: {line[:50]}... - {e}")
                    continue
    
    except Exception as e:
        logging.error(f"파일 읽기 실패: {e}")
        return []
    
    logging.info(f"총 {len(data)}개의 데이터 추출 완료 (총 {line_count}줄 처리)")
    return data

def create_excel_file(data, output_file):
    """데이터를 엑셀 파일로 저장"""
    
    if not data:
        logging.error("저장할 데이터가 없습니다.")
        return
    
    try:
        # DataFrame 생성
        df = pd.DataFrame(data)
        
        # 중복 제거 (같은 대학, 같은 학과)
        df = df.drop_duplicates(subset=['university_name', 'department_name'])
        
        # 정렬
        df = df.sort_values(['university_name', 'department_name'])
        
        # 엑셀 파일로 저장
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Master_Data', index=False)
            
            # 워크시트 가져오기
            worksheet = writer.sheets['Master_Data']
            
            # 컬럼 너비 조정
            worksheet.column_dimensions['A'].width = 15  # university_name
            worksheet.column_dimensions['B'].width = 25  # department_name
            worksheet.column_dimensions['C'].width = 10  # category
            worksheet.column_dimensions['D'].width = 15  # recruitment_count_general
            worksheet.column_dimensions['E'].width = 15  # recruitment_count_bachelor
            worksheet.column_dimensions['I'].width = 50  # raw_text_check
        
        logging.info(f"엑셀 파일 생성 완료: {output_file}")
        logging.info(f"총 {len(df)}개 행, {len(df.columns)}개 열")
        
        # 통계 출력
        print("\n=== 파싱 결과 통계 ===")
        print(f"총 데이터 수: {len(df)}개")
        print(f"대학 수: {df['university_name'].nunique()}개")
        
        # 대학별 통계
        university_stats = df.groupby('university_name').agg({
            'department_name': 'count',
            'recruitment_count_general': 'sum',
            'recruitment_count_bachelor': 'sum'
        }).round(0)
        university_stats.columns = ['학과수', '일반편입', '학사편입']
        print("\n=== 대학별 통계 ===")
        print(university_stats)
        
        # 계열별 통계
        category_stats = df.groupby('category').size()
        print("\n=== 계열별 통계 ===")
        print(category_stats)
        
    except Exception as e:
        logging.error(f"엑셀 파일 생성 실패: {e}")

def main():
    """메인 함수"""
    
    input_file = 'all_tables_raw.txt'
    output_file = 'Master_Data_v2.xlsx'
    
    print("📊 대학 모집요강 데이터 변환 시작...")
    print(f"입력 파일: {input_file}")
    print(f"출력 파일: {output_file}")
    
    # 데이터 파싱
    data = parse_university_data(input_file)
    
    if data:
        # 엑셀 파일 생성
        create_excel_file(data, output_file)
        print(f"✅ 변환 완료: {output_file}")
        print("📋 원본 텍스트는 'raw_text_check' 컬럼에서 확인 가능합니다.")
    else:
        print("❌ 추출된 데이터가 없습니다.")

if __name__ == "__main__":
    main()