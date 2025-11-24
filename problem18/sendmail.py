import smtplib
import ssl
import csv
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
CSV_FILENAME = 'mail_target_list.csv'


class EmailSender:
    """
    이메일 발송을 담당하는 클래스
    PEP 8: 클래스 이름은 CapWords 규칙을 따름
    """

    def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password

    def send_html_message(self, receiver_name, receiver_email):
        """
        개별 수신자에게 HTML 형식의 메일을 전송합니다.
        PEP 8: 함수 이름은 snake_case 규칙을 따름
        """
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_email
        message['To'] = receiver_email
        message['Subject'] = f'[생존 신고] {receiver_name}님, 한송희 박사입니다.'

        html_body = f'''
        <html>
            <body>
                <h2 style="color: #d9534f;">Survival Report from Mars</h2>
                <p>Dear <strong>{receiver_name}</strong>,</p>
                <p>I am sending this message to confirm my survival.</p>
                <p>We received your message from Earth. Thank you.</p>
                <hr>
                <p style="color: gray; font-size: 12px;">Sent via Python SMTP</p>
            </body>
        </html>
        '''

        part = MIMEText(html_body, 'html', 'utf-8')
        message.attach(part)

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.send_message(message)

            print(f'성공: {receiver_name} <{receiver_email}> 에게 전송 완료')
            return True

        except smtplib.SMTPAuthenticationError:
            print('오류: 인증 실패 (ID/PW 확인 필요)')
        except smtplib.SMTPException as e:
            print(f'오류: SMTP 전송 중 문제 발생 - {e}')
        except Exception as e:
            print(f'오류: 알 수 없는 예외 발생 - {e}')

        return False


def load_target_list(filename):
    """
    CSV 파일을 읽어 (이름, 이메일) 리스트를 반환합니다.
    """
    targets = []
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    email = row[1].strip()
                    targets.append((name, email))

    except FileNotFoundError:
        print(f'경고: {filename} 파일을 찾을 수 없습니다.')

    return targets


def main():
    print('=' * 50)
    print(' [화성 기지] HTML 메일 대량 발송 시스템')
    print('=' * 50)

    sender_email = input('보내는 사람 이메일 (Gmail): ').strip()
    sender_password = getpass.getpass('앱 비밀번호: ').strip()

    recipients = load_target_list(CSV_FILENAME)

    if not recipients:
        print('알림: 전송할 대상이 없습니다. 프로그램을 종료합니다.')
        return

    print(f'\n총 {len(recipients)}명의 수신자가 확인되었습니다.')
    print('메일 전송을 시작합니다...\n')

    sender = EmailSender(sender_email, sender_password)

    for name, email in recipients:
        sender.send_html_message(name, email)

    print('\n' + '=' * 50)
    print(' 모든 작업이 완료되었습니다.')
    print('=' * 50)


if __name__ == '__main__':
    main()