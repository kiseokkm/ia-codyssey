import socket
import threading
import sys

BUFFER_SIZE = 1024

def client_main() -> None:
    host = '127.0.0.1'
    port = 5000
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f'서버({host}:{port})에 연결되었습니다. "/종료" 입력 시 종료됩니다.')

    threading.Thread(target=_recv_loop, args=(sock,), daemon=True).start()

    try:
        while True:
            msg = input()
            if not msg:
                continue
            sock.sendall(msg.encode('utf-8'))
            if msg == '/종료':
                break
    except (KeyboardInterrupt, EOFError):
        try:
            sock.sendall("/종료".encode("utf-8"))
        except OSError:
            pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def _recv_loop(sock: socket.socket) -> None:
    try:
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            print(data.decode('utf-8'), end='')
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


if __name__ == '__main__':
    client_main()
