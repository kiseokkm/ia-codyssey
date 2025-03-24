import csv

# Mars_Base_Inventory_List.csv 의 내용을 list 객체로 변환
# 배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬
# 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력
# 인화성 지수가 0.7 이상되는 목록을 CSV 포멧으로 저장


# 파일 경로 상수
INPUT_FILE = 'problem2/Mars_Base_Inventory_List.csv'
OUTPUT_FILE = 'problem2/Mars_Base_Inventory_danger.csv'

# CSV 파일 읽어 list로 변환
def read_inventory(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file) # 파일을 한 줄씩 리스트 형태로 읽어줌
            header = next(reader)  # 헤더는 따로 저장
            data = [row for row in reader]
        return header, data
    except Exception as e:
        print(f'파일 읽기 오류: {e}')
        return [], []

# 인화성 높은 순으로 정렬 & 0.7 이상되는 목록 필터링
def get_dangerous_items(data, threshold=0.7):
    filtered = []
    for row in data:
        try:
            flammability = float(row[-1])  # csv에서 마지막 열이 인화성 지수! csv 읽을때 문자열임, 실수로 변환!
            if flammability >= threshold:
                filtered.append(row)
        except ValueError:
            # 'Various' 등 숫자가 아닌 경우 무시
            continue
    # 인화성 지수 기준 내림차순 정렬
    filtered.sort(key=lambda x: float(x[-1]), reverse=True)
    return filtered

# CSV 파일로 저장
def save_to_csv(file_path, header, data):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
        print(f' 위험 물질 목록 저장 완료: {file_path}')
    except Exception as e:
        print(f'파일 저장 오류: {e}')

# 메인 함수
def main():
    header, data = read_inventory(INPUT_FILE)
    if not data:
        return

    print('[ 전체 물질 리스트 출력 ]')
    for row in data:
        print(row)

    print('\n[ 인화성 0.7 이상 위험 물질 목록 ]')
    danger_items = get_dangerous_items(data)
    for item in danger_items:
        print(item)

    save_to_csv(OUTPUT_FILE, header, danger_items)

# 실행
if __name__ == '__main__':
    main()
