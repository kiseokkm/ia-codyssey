# 파일 경로
LOG_FILE_PATH = '1주차/data/mission_computer_main.log'
ERROR_LOG_FILE_PATH = '1주차/data/ERROR_log.log'

# 오류 키워드 (문제가 되는 부분 키워드만 넣어놨음, 추가 하면 그에 맞게 저장됨)
ERROR_KEYWORDS = ["unstable", "explosion", "powered down"]

# 로그 파일을 읽어오는 함수
def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except Exception as e:
        print(f'오류: {e}')
    return []

# 오류 로그를 저장하는 함수
def save_error_logs(error_lines):
    if error_lines:
        with open(ERROR_LOG_FILE_PATH, 'w', encoding='utf-8') as error_file:
            error_file.writelines(error_lines)
        print(f'문제 로그가 "{ERROR_LOG_FILE_PATH}"에 저장되었습니다.')

def main():
    print('Hello Mars\n')

    # 로그 파일 읽기
    logs = read_log_file(LOG_FILE_PATH)

    if logs:
        print('\n[ 로그 파일 내용 출력 (최신순) ]\n')

        # logs 리스트를 역순으로 정렬
        logs.reverse() 

        # 출력
        for line in logs:
            print(line.strip())

        # 문제가 되는 부분 필터링
        error_lines = [line for line in logs if any(keyword in line for keyword in ERROR_KEYWORDS)]

        # 오류 로그 파일로 저장
        save_error_logs(error_lines)

if __name__ == '__main__':
    main()
