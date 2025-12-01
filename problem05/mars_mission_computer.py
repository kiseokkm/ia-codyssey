import random
import time
import json
import platform
import psutil
from datetime import datetime

# 로그 파일 경로를 상수로 정의
LOG_FILE = 'problem3/sensor_log.txt'
SETTING_FILE = 'problem5/setting.txt'

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
            short_key = key.replace('mars_base_', '')  # 접두사(중복) 제거
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
        self.settings = self.load_settings()

    def load_settings(self):
        # setting.txt 파일에서 출력 항목을 불러온다
        settings = {
            'SystemInfo': {
                'operating_system': True,
                'os_version': True,
                'cpu_type': True,
                'cpu_cores': True,
                'memory_size_gb': True
            },
            'LoadInfo': {
                'cpu_usage_percent': True,
                'memory_usage_percent': True
            }
        }
        try:
            with open(SETTING_FILE, 'r', encoding='utf-8') as f:
                section = None
                for line in f:
                    line = line.strip()
                    if line.startswith('['):
                        section = line.strip('[]')
                    elif '=' in line and section:
                        key, val = line.split('=')
                        settings[section][key.strip()] = val.strip().lower() == 'true'
        except FileNotFoundError:
            print(f'setting.txt 파일을 찾을 수 없습니다. 기본값을 사용합니다.')
        except Exception as e:
            print(f'설정 파일 읽기 오류: {e}')
        return settings

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

    def get_mission_computer_info(self):
        try:
            info = {}
            if self.settings['SystemInfo'].get('operating_system', False):
                info['operating_system'] = platform.system()
            if self.settings['SystemInfo'].get('os_version', False):
                info['os_version'] = platform.version()
            if self.settings['SystemInfo'].get('cpu_type', False):
                info['cpu_type'] = platform.processor()
            if self.settings['SystemInfo'].get('cpu_cores', False):
                info['cpu_cores'] = psutil.cpu_count(logical=False)
            if self.settings['SystemInfo'].get('memory_size_gb', False):
                info['memory_size_gb'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)

            print('[시스템 정보]')
            print(json.dumps(info, indent=2))
            return info
        except Exception as e:
            print(f'Error retrieving mission computer info: {e}')
            return {}

    def get_mission_computer_load(self):
        try:
            load = {}
            if self.settings['LoadInfo'].get('cpu_usage_percent', False):
                load['cpu_usage_percent'] = psutil.cpu_percent(interval=1)
            if self.settings['LoadInfo'].get('memory_usage_percent', False):
                load['memory_usage_percent'] = psutil.virtual_memory().percent

            print('[시스템 부하]')
            print(json.dumps(load, indent=2))
            return load
        except Exception as e:
            print(f'Error retrieving mission computer load: {e}')
            return {}

if __name__ == '__main__':
    print('[미션 컴퓨터 시작 - 5초 간격으로 센서 데이터 수집 중...]')
    print('[종료하려면 Ctrl+C 를 누르세요.]')

    RunComputer = MissionComputer()
    RunComputer.get_mission_computer_info()
    RunComputer.get_mission_computer_load()
    RunComputer.get_sensor_data()
