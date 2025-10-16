import requests
from bs4 import BeautifulSoup

def crawl_kbs_headlines():
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'
    headline_list = []

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        
        headline_elements = soup.select('div.txt-wrapper > p.title')
        
        for element in headline_elements:
            title = element.get_text(strip=True)
            if title:
                headline_list.append(title)
            
    except requests.exceptions.RequestException as e:
        print(f'오류가 발생했습니다: {e}')
        
    return headline_list

if __name__ == '__main__':
    headlines = crawl_kbs_headlines()
    
    if headlines:
        print('--- KBS 헤드라인 뉴스 ---')
        for i, title in enumerate(headlines, 1):
            print(f'{i}. {title}')
    else:
        print('뉴스를 가져오는데 실패했습니다.')
