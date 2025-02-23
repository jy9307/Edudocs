
import requests
from bs4 import BeautifulSoup
import re

class UrlExtractor() :

    def __init__(self,url) :
        self.response = requests.get(url)
        self.response.raise_for_status()


        return

    def law_url_extract(self) :

        soup = BeautifulSoup(self.response.text, 'html.parser')
        print(soup)

        span = soup.find('span', string=re.compile('시행'))

        iframe = soup.find("iframe", {"id": "lawService"})

        if iframe:
            # iframe의 src 속성값 추출
            iframe_src = iframe["src"]
            
            # 절대 URL 생성
            iframe_url = f"https://www.law.go.kr{iframe_src}"

            iframe_response = requests.get(iframe_url)
            iframe_response.raise_for_status()

            # iframe 내부 HTML 파싱
            iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')

            print(iframe_soup)

        # if span:
        #     # 텍스트 추출
        #     text = span.get_text(strip=True)
            
        #     # 정규식을 사용하여 날짜와 법률 번호 추출
        #     matches = re.findall(r'\d{4}\. \d{1,2}\. \d{1,2}\.|\d{5,}', text)
            
        #     if len(matches) == 3:
        #         시행일 = matches[0].replace('. ', '')
        #         법률번호 = matches[1]
        #         공포일 = matches[2].replace('. ', '')
                
        #         # 원하는 형식으로 출력
        #         result = f"({시행일},{법률번호},{공포일})"
        #         return result

       


extractor = UrlExtractor('https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%90%EC%9C%A1%EA%B3%B5%EB%AC%B4%EC%9B%90%EB%B2%95')
print(extractor.law_url_extract())



