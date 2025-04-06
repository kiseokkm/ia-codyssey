import random
import time
import json
from datetime import datetime

# 로그 파일 경로를 상수로 정의
LOG_FILE = 'problem3/sensor_log.txt'

class DummySensor:
    def __init__(self):
        # 센서 값들을 저장할 사전 객체
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        # 각 센서 항목의 값을 지정된 범위 내에서 랜덤으로 설정
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        # 현재 시간 기록
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 로그 문자열 구성
        log_lines = [now]
        for key, value in self.env_values.items():
            short_key = key.replace('mars_base_', '') # 접두사(중복) 제거
            log_lines.append(f'{short_key}: {value}')
        
        log_text = '\n'.join(log_lines) + '\n'

        # 로그 파일에 저장
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as file:
                file.write(log_text)
        except Exception as e:
            print(f'로그 파일 저장 중 오류 발생: {e}')

        # 콘솔 출력
        print(log_text)
        return self.env_values
    
class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.ds = DummySensor()
        self.history = {key: [] for key in self.env_values.keys()}
        self.last_avg_time = time.time()

    def get_sensor_data(self):
        try:
            while True:
                self.ds.set_env()
                self.env_values = self.ds.get_env()

                # JSON 형태로 출력
                print('[실시간 센서 데이터]')
                print(json.dumps(self.env_values, indent=2))
                print('-' * 40)

                # 평균 계산을 위한 값 저장
                for key in self.env_values:
                    self.history[key].append(self.env_values[key])

                # 5분 평균 출력 
                current_time = time.time()
                if current_time - self.last_avg_time >= 300:
                    print('[최근 5분간 평균 값 출력]')
                    avg_values = {}
                    for key in self.history:
                        values = self.history[key]
                        avg_values[key] = round(sum(values) / len(values), 2) if values else 0.0
                    print(json.dumps(avg_values, indent=2))
                    print('=' * 40)

                    # 초기화
                    self.history = {key: [] for key in self.env_values.keys()}
                    self.last_avg_time = current_time

                time.sleep(5)
        
        except KeyboardInterrupt:
            print('\nSystem stopped...')
            
if __name__ == '__main__':
    print('[미션 컴퓨터 시작 - 5초 간격으로 센서 데이터 수집 중...]')
    print('[종료하려면 Ctrl+C 를 누르세요.]')

    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()