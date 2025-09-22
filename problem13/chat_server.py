import socket
import threading
import sys
from typing import Dict, Optional, Tuple

BUFFER_SIZE = 1024
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 5000


class ChatServer:
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
        self.host = host
        self.port = port
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.settimeout(1.0)
        self._clients: Dict[socket.socket, str] = {}
        self._nick_map: Dict[str, socket.socket] = {}
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def start(self) -> None:
        self._server_sock.bind((self.host, self.port))
        self._server_sock.listen()
        print(f'Server listening on {self.host}:{self.port}')
        try:
            while not self._stop_event.is_set():
                try:
                    client_sock, addr = self._server_sock.accept()
                except socket.timeout:
                    continue
                threading.Thread(
                    target=self._handle_client, args=(client_sock, addr), daemon=True
                ).start()
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt: shutting down server...')
        finally:
            self.shutdown()

    def _handle_client(self, client_sock: socket.socket, addr: Tuple[str, int]) -> None:
        try:
            nickname = self._recv_nickname(client_sock)
            if nickname is None:
                client_sock.close()
                return
            self._register_client(client_sock, nickname)
            self._broadcast(f'[{nickname}]님이 입장하셨습니다.')
            self._send_line(client_sock, '안내: 채팅을 시작합니다. 종료는 /종료')
            while True:
                msg = self._recv_msg(client_sock)
                if not msg:
                    break
                if msg == '/종료':
                    self._send_line(client_sock, '연결을 종료합니다.')
                    break
                sender = self._get_nickname(client_sock) or '알수없음'
                self._broadcast(f'{sender}> {msg}')
        except ConnectionResetError:
            pass
        finally:
            self._remove_client(client_sock)

    def _recv_nickname(self, client_sock: socket.socket) -> Optional[str]:
        self._send_line(client_sock, '닉네임을 입력해주세요:')
        try:
            data = client_sock.recv(BUFFER_SIZE)
        except ConnectionResetError:
            return None
        if not data:
            return None
        raw = data.decode('utf-8', errors='ignore').strip() or 'user'
        nickname = self._make_unique_nickname(raw)
        self._send_line(client_sock, f'닉네임이 [{nickname}]로 설정되었습니다.')
        return nickname

    def _make_unique_nickname(self, base: str) -> str:
        with self._lock:
            if base not in self._nick_map:
                return base
            index = 2
            while True:
                cand = f'{base}{index}'
                if cand not in self._nick_map:
                    return cand
                index += 1

    def _register_client(self, client_sock: socket.socket, nickname: str) -> None:
        with self._lock:
            self._clients[client_sock] = nickname
            self._nick_map[nickname] = client_sock
        print(f'Connected: {nickname}')

    def _remove_client(self, client_sock: socket.socket) -> None:
        nickname = None
        with self._lock:
            nickname = self._clients.pop(client_sock, None)
            if nickname:
                self._nick_map.pop(nickname, None)
        if nickname:
            print(f'Disconnected: {nickname}')
            self._broadcast(f'[{nickname}]님이 퇴장하셨습니다.')
        try:
            client_sock.close()
        except OSError:
            pass

    def _get_nickname(self, client_sock: socket.socket) -> Optional[str]:
        with self._lock:
            return self._clients.get(client_sock)

    def _broadcast(self, line: str) -> None:
        with self._lock:
            targets = list(self._clients.keys())
        for sock in targets:
            self._send_line(sock, line)

    @staticmethod
    def _send_line(sock: socket.socket, line: str) -> None:
        try:
            sock.sendall((line + '\n').encode('utf-8'))
        except OSError:
            pass

    @staticmethod
    def _recv_msg(sock: socket.socket) -> str:
        try:
            data = sock.recv(BUFFER_SIZE)
        except OSError:
            return ''
        if not data:
            return ''
        return data.decode('utf-8', errors='ignore').strip()

    def shutdown(self) -> None:
        self._stop_event.set()
        with self._lock:
            targets = list(self._clients.keys())
        for sock in targets:
            try:
                self._send_line(sock, '서버가 종료됩니다.')
                sock.close()
            except OSError:
                pass
        try:
            self._server_sock.close()
        except OSError:
            pass


def server_main() -> None:
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print('포트는 정수여야 합니다. 기본값 사용.')
    server = ChatServer(host, port)
    threading.Thread(target=_admin_console, args=(server,), daemon=True).start()
    server.start()


def _admin_console(server: ChatServer) -> None:
    while True:
        try:
            cmd = input()
        except EOFError:
            break
        if cmd.strip() == '/종료':
            print('서버 종료 명령 수신')
            server.shutdown()
            break


if __name__ == '__main__':
    server_main()
