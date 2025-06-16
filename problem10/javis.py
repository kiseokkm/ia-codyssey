import os
import wave
import datetime
import pyaudio


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def create_records_directory(base_dir):
    records_path = os.path.join(base_dir, 'records')
    if not os.path.exists(records_path):
        os.mkdir(records_path)
    return records_path


def generate_filename(records_path):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M%S')
    filename = os.path.join(records_path, timestamp + '.wav')
    return filename


def record_voice(duration_seconds=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print('녹음을 시작합니다.')

    frames = []

    for _ in range(0, int(rate / chunk * duration_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print('녹음이 완료되었습니다.')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    base_dir = get_base_dir()
    records_path = create_records_directory(base_dir)
    filename = generate_filename(records_path)

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print('파일이 저장되었습니다: ' + filename)


def main():
    base_dir = get_base_dir()
    create_records_directory(base_dir)
    record_voice()


if __name__ == '__main__':
    main()
