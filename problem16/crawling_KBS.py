import time
import pyperclip
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_naver_mail_count(user_id, user_pw):
    mail_info = []
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option('detach', True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://nid.naver.com/nidlogin.login')

        pyperclip.copy(user_id)
        driver.find_element(By.ID, 'id').click()
        time.sleep(1)
        driver.find_element(By.ID, 'id').send_keys('\ue009', 'v')
        time.sleep(1)

        pyperclip.copy(user_pw)
        driver.find_element(By.ID, 'pw').click()
        time.sleep(1)
        driver.find_element(By.ID, 'pw').send_keys('\ue009', 'v')
        time.sleep(1)

        driver.find_element(By.ID, 'log.login').click()

        wait = WebDriverWait(driver, 20)
        mail_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.nav.mail > span.an_icon > em.an_cur'))
        )
        
        unread_mail_count = mail_element.text
        mail_info.append(f'읽지 않은 메일: {unread_mail_count}개')

    except Exception as e:
        mail_info.append(f'크롤링 중 오류가 발생했습니다: {e}')
    finally:
        driver.quit()
        
    return mail_info

if __name__ == '__main__':
    my_id = input('네이버 아이디를 입력하세요: ')
    my_pw = getpass.getpass('네이버 비밀번호를 입력하세요: ')

    results = get_naver_mail_count(my_id, my_pw)
    
    if results:
        print("\n--- 크롤링 결과 ---")
        for item in results:
            print(item)
    else:
        print("결과를 가져오지 못했습니다.")

