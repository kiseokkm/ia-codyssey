import smtplib
import ssl
import os
from email.message import EmailMessage

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path=None):
    
    try:
        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.set_content(body)

        if attachment_path:
            try:
                with open(attachment_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)
                
                message.add_attachment(
                    file_data,
                    maintype='application',
                    subtype='octet-stream',
                    filename=file_name
                )
                print(f'첨부파일이 추가되었습니다: {file_name}')
            except Exception as e:
                print(f'첨부파일 처리 중 오류 발생: {str(e)}')
                return False

        context = ssl.create_default_context()
        
        print(f'SMTP 서버에 연결 중... ({SMTP_SERVER}:{SMTP_PORT})')
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        print('TLS 보안 연결을 시작합니다...')
        server.starttls(context=context)
        print('TLS 보안 연결이 설정되었습니다.')

        print('Gmail 계정으로 로그인 중...')
        server.login(sender_email, sender_password)
        print('로그인 성공!')

        server.send_message(message)
        print(f'메일이 성공적으로 발송되었습니다: {receiver_email}')

        server.quit()
        print('SMTP 서버 연결이 종료되었습니다.')

        return True

    except smtplib.SMTPAuthenticationError:
        print('오류: 인증 실패. 이메일 주소 또는 앱 비밀번호를 확인해주세요.')
        print('Gmail의 경우 2단계 인증 및 앱 비밀번호가 필요합니다.')
        return False
    except smtplib.SMTPConnectError:
        print('오류: SMTP 서버 연결 실패. 네트워크 연결을 확인해주세요.')
        return False
    except smtplib.SMTPServerDisconnected:
        print('오류: SMTP 서버와의 연결이 끊어졌습니다.')
        return False
    except smtplib.SMTPException as e:
        print(f'오류: SMTP 오류가 발생했습니다 - {str(e)}')
        return False
    except Exception as e:
        print(f'오류: 예상치 못한 오류가 발생했습니다 - {str(e)}')
        return False


def main():
    print('=' * 50)
    print('Gmail SMTP 이메일 발송 프로그램 (STARTTLS, 587)')
    print('=' * 50)
    print()
    print('※ Gmail에서 2단계 인증을 사용하는 경우 앱 비밀번호를 생성해야 합니다.')
    print('  (Google 계정 > 보안 > 2단계 인증 > 앱 비밀번호)')
    print()

    sender_email = input('보내는 사람 Gmail 주소: ').strip()
    sender_password = input('Gmail 앱 비밀번호: ').strip()
    receiver_email = input('받는 사람 이메일 주소: ').strip()
    subject = input('메일 제목: ').strip()
    
    print('메일 본문 (입력 완료 후 빈 줄에서 Enter):')
    body_lines = []
    while True:
        line = input()
        if line == '':
            break
        body_lines.append(line)
    body = '\n'.join(body_lines)

    attachment_path = None
    attach_file = input('첨부파일을 추가하시겠습니까? (y/n): ').strip().lower()

    if attach_file == 'y':
        attachment_path_input = input('첨부파일 경로를 입력하세요: ').strip()
        
        if not os.path.exists(attachment_path_input):
            print(f'경고: 파일을 찾을 수 없습니다 - {attachment_path_input}')
            continue_anyway = input('첨부파일 없이 계속 진행하시겠습니까? (y/n): ').strip().lower()
            if continue_anyway != 'y':
                print('메일 발송이 취소되었습니다.')
                return
        else:
            attachment_path = attachment_path_input

    print()
    print('-' * 50)
    print('메일 발송을 시작합니다...')
    print('-' * 50)
    print()

    success = send_email(
        sender_email,
        sender_password,
        receiver_email,
        subject,
        body,
        attachment_path
    )

    print()
    if success:
        print('✓ 메일 발송이 완료되었습니다!')
    else:
        print('✗ 메일 발송에 실패했습니다.')


if __name__ == '__main__':
    main()