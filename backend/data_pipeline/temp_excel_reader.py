import pandas as pd
import sys

# Excel 파일 읽기
try:
    df = pd.read_excel('편입모집요강.xlsx')
    print("Excel 파일 읽기 성공!")
    print(f"데이터 형태: {df.shape}")
    print("\n컬럼명:")
    print(df.columns.tolist())
    print("\n첫 5행:")
    print(df.head())
    print("\n데이터 타입:")
    print(df.dtypes)
    
    # CSV로 저장
    df.to_csv('temp_data.csv', index=False, encoding='utf-8-sig')
    print("\nCSV 파일로 저장 완료: temp_data.csv")
    
except Exception as e:
    print(f"오류 발생: {e}")