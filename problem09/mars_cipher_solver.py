import os
import zipfile
from typing import Optional


def load_caesar_target_from_zip() -> Optional[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, '..', 'problem8')

    zip_path = os.path.join(base_path, 'emergency_storage_key.zip')
    pw_path = os.path.join(base_path, 'password.txt')
    internal_filename = 'password.txt'

    try:
        with open(pw_path, 'r', encoding='utf-8') as f:
            password = f.read().strip()
    except Exception:
        return None

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            if internal_filename not in zf.namelist():
                return None
            data = zf.read(internal_filename, pwd=password.encode('utf-8'))
            return data.decode('utf-8')
    except Exception:
        return None

def caesar_cipher_decode(target_text: str, key: int) -> str:
    result = []
    for char in target_text:
        if 'a' <= char <= 'z':
            shifted = (ord(char) - ord('a') - key) % 26
            result.append(chr(shifted + ord('a')))
        elif 'A' <= char <= 'Z':
            shifted = (ord(char) - ord('A') - key) % 26
            result.append(chr(shifted + ord('A')))
        else:
            result.append(char)
    return ''.join(result)


def main():
    ciphertext = load_caesar_target_from_zip()
    if ciphertext is None:
        return

    candidates = {}
    for key in range(26):
        plain = caesar_cipher_decode(ciphertext, key)
        candidates[key] = plain
        print(f'[{key:02}] {plain}')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    result_path = os.path.join(script_dir, 'result.txt')

    while True:
        try:
            user_input = input('정답으로 보이는 key 번호를 입력하세요 (0~25): ')
            selected = int(user_input)
            if 0 <= selected < 26:
                with open(result_path, 'w', encoding='utf-8') as f:
                    f.write(candidates[selected])
                print(f'선택된 평문이 {result_path} 에 저장되었습니다.')
                break
            else:
                print('0~25 사이 숫자를 입력하세요.')
        except ValueError:
            print('숫자를 입력하세요.')
        except Exception as e:
            print(f'오류 발생: {e}')

if __name__ == '__main__':
    main()
