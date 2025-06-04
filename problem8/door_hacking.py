import zipfile
import string
import itertools
import multiprocessing
import time
import os

def crack_worker(zip_path, first_chars, charset, pwd_len, stop_signal, result, counter, start_time):
    def gen_pw():
        if pwd_len == 1:
            for fc in first_chars:
                yield fc
        else:
            for fc in first_chars:
                for tail in itertools.product(charset, repeat=pwd_len - 1):
                    yield fc + ''.join(tail)

    for pw in gen_pw():
        if stop_signal.is_set():
            break
        with counter.get_lock():
            counter.value += 1
            if counter.value % 10000 == 0:
                print(f'시도 {counter.value}회 / {pw} / 경과 {time.time() - start_time:.1f}초')
        try:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(pwd=pw.encode('utf-8'))
            if not stop_signal.is_set():
                result.put(pw)
                stop_signal.set()
            break
        except Exception:
            continue

def unlock_zip(zip_path='emergency_storage_key.zip', out_file='problem/8password.txt'):
    print('비밀번호 크래킹을 시작합니다...')
    charset = string.ascii_lowercase + string.digits
    length = 6
    total = len(charset) ** length

    if not os.path.exists(zip_path):
        print(f'파일 {zip_path}을 찾을 수 없습니다.')
        return

    start = time.time()
    print(f'시작시간: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))}')
    print(f'총 경우의 수: {total:,}개')

    proc = multiprocessing.cpu_count()
    print(f'병렬 프로세스: {proc}')

    stop_signal = multiprocessing.Event()
    result = multiprocessing.Queue()
    counter = multiprocessing.Value('i', 0)

    char_splits = [[] for _ in range(proc)]
    for i, ch in enumerate(charset):
        char_splits[i % proc].append(ch)

    workers = []
    for first_set in char_splits:
        if not first_set:
            continue
        p = multiprocessing.Process(
            target=crack_worker,
            args=(zip_path, first_set, charset, length, stop_signal, result, counter, start)
        )
        workers.append(p)
        p.start()

    password = None
    while any(p.is_alive() for p in workers) and not stop_signal.is_set():
        try:
            password = result.get(timeout=1)
            if password:
                stop_signal.set()
                break
        except:
            pass

    for p in workers:
        p.terminate()
        p.join()

    elapsed = time.time() - start
    if password:
        print(f'암호 발견: {password}')
        print(f'총 시도: {counter.value}회')
        print(f'걸린 시간: {elapsed:.2f}초')
        try:
            with open(out_file, 'w') as f:
                f.write(password)
            print(f'비밀번호를 {out_file}에 저장했습니다.')
        except Exception:
            print(f'파일 저장 실패')
        return password
    else:
        print(f'실패. 총 시도: {counter.value}회, 경과 {elapsed:.2f}초')

if __name__ == '__main__':
    unlock_zip('problem8/emergency_storage_key.zip', 'problem8/password.txt')
