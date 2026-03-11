import re
import pandas as pd

# 파일 경로 (파일명 확인하세요!)
input_file = 'all_tables_raw.txt'
output_file = 'Master_Data_Final.xlsx'

def parse_safe_mode(file_path):
    data_list = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_univ = "대학명_미확인"
    
    for line in lines:
        line = line.strip()
        if not line: continue # 빈 줄 삭제

        # 1. 대학명 식별 (단순하지만 강력하게)
        # "대학교"로 끝나거나 줄에 "대학"이 있고 숫자가 없으면 대학명으로 간주
        if ("대학교" in line or "대학" in line) and not any(char.isdigit() for char in line):
            current_univ = line
            continue

        # 2. 데이터 추출 (후방 탐색 전략)
        # 줄의 맨 뒤에서부터 숫자를 찾음. 
        # 예: "경영학과 12 4" -> 4(학사), 12(일반), 나머지(경영학과)
        
        # 숫자들을 모두 찾음
        numbers = re.findall(r'\d+', line)
        
        dept_name = line # 기본값은 전체 줄 내용
        quota_gen = 0
        quota_bach = 0
        
        if len(numbers) >= 2:
            # 숫자가 2개 이상이면: 맨 뒤가 학사, 그 앞이 일반
            quota_bach = int(numbers[-1])
            quota_gen = int(numbers[-2])
            # 학과명은 숫자 앞부분까지 잘라내기
            # (단, 학과명에 숫자가 포함된 경우(예: 2차전지)가 있을 수 있어 단순 제거보다 원본 유지 추천)
            dept_match = re.search(r'^(.*?)(\d+\s+\d+)', line)
            if dept_match:
                dept_name = dept_match.group(1).strip()
            else:
                # 패턴 매칭 실패 시 그냥 숫자만 제거 시도
                dept_name = re.sub(r'\d+', '', line).strip()
                
        elif len(numbers) == 1:
            # 숫자가 1개면: 보통 일반편입 인원만 있는 경우
            quota_gen = int(numbers[0])
            dept_name = re.sub(r'\d+', '', line).strip()

        # 3. 데이터 적재 (밀림 방지를 위해 Raw Text도 같이 저장)
        data_list.append({
            'university_name': current_univ,
            'department_name': dept_name,   # 최대한 발라낸 학과명
            'recruitment_count_general': quota_gen,
            'recruitment_count_bachelor': quota_bach,
            'score_cutoff_general': '',     # 빈칸
            'score_cutoff_bachelor': '',    # 빈칸
            'category': '분류필요',          # 엑셀에서 필터 걸고 일괄 수정 추천
            'raw_text_check': line          # [핵심] 원본을 보고 수정하도록 함
        })

    return data_list

# 실행 및 엑셀 저장
try:
    print("🔄 데이터 변환 중... (밀림 방지 모드)")
    result_data = parse_safe_mode(input_file)
    
    df = pd.DataFrame(result_data)
    
    # 엑셀 저장
    df.to_excel(output_file, index=False)
    
    print(f"✅ 변환 완료! '{output_file}' 파일이 생성되었습니다.")
    print("👉 'raw_text_check' 열을 보면 원본이 있으니, 숫자가 이상한 곳은 팀원들이 그것을 보고 수정하면 됩니다.")

except Exception as e:
    print(f"❌ 오류 발생: {e}")