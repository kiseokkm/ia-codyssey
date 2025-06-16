import os
import csv
import speech_recognition as sr


def get_records_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    records_path = os.path.join(base_dir, '..', 'problem10', 'records')
    return os.path.abspath(records_path)


def get_records_text_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    records_text_path = os.path.join(base_dir, 'records_text')
    if not os.path.exists(records_text_path):
        os.makedirs(records_text_path)
    return records_text_path


def transcribe_all_records():
    records_path = get_records_path()
    records_text_path = get_records_text_path()
    recognizer = sr.Recognizer()

    for file in os.listdir(records_path):
        if file.endswith('.wav'):
            wav_path = os.path.join(records_path, file)
            csv_name = file.replace('.wav', '.csv')
            csv_path = os.path.join(records_text_path, csv_name)

            print('STT 시작: ' + file)

            with sr.AudioFile(wav_path) as source:
                audio = recognizer.record(source)

            try:
                result = recognizer.recognize_google(audio, language='ko-KR', show_all=True)

                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['time', 'text'])

                    if 'alternative' in result:
                        timestamp = '00:00'
                        for alt in result['alternative']:
                            text = alt.get('transcript', '')
                            writer.writerow([timestamp, text])

                print('CSV 저장 완료: ' + csv_name)

            except sr.UnknownValueError:
                print('인식 실패: ' + file)
            except sr.RequestError:
                print('Google STT 요청 실패')


def main():
    transcribe_all_records()


if __name__ == '__main__':
    main()
