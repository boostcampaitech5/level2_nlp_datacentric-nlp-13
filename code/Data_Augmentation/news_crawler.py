#크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd


'''
연합뉴스에서 뉴스 기사 제목 크롤링
분야 : [정치, 경제, 기술과학, 사회, 문화, 스포츠, 세계]
'''

# url 만들기

def makeUrl(topic, start_pg, end_pg):
    urls = []
    for i in range(start_pg, end_pg + 1):
        if topic == 'technology-science':
            url = "https://www.yna.co.kr/industry/technology-science/"+str(i)
            results.append(url)
        else:
            url = "https://www.yna.co.kr/"+topic+"/all/"+str(i)
            results.append(url)
    return urls


# 기사 제목 크롤링하기

def news_title_crawling(urls):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
    titles=[]
    for url in tqdm(urls):
        for attempt in range(2): # connection error 2번까지 대시도
            try:
                req = requests.get(url, headers = headers, timeout=5)
                soup = BeautifulSoup(req.text, "html.parser")
                title = soup.select('strong.tit-news')
                for i in title:
                    titles.append(i.get_text())
            except:
                print("retry")
                time.sleep(5)
            else:
                break

#데이터 프레임으로 만들고 전처리하기

def preprocessing(texts)

    news_df = pd.DataFrame({'text':texts})
    #중복 행 지우기
    news_df = news_df.drop_duplicates(keep='first',ignore_index=True)

    # 특수문자 전처리
    special = re.compile(r'[^ A-Za-z0-9가-힣]')
    news_df['text'] = news_df['text'].apply(lambda x: special.sub(' ',x))

    # 띄어쓰기 보정하기 
    news_df['text'] = news_df['text'].apply(lambda x: ' '.join(x.split()))
    # None 값 없애기
    none_idx = news_df[news_df['text']=='None'].index
    news_df.drop(none_idx, inplace=True)

    return news_df


if __name__ == '__main__':
    topics = ['politics', 'economy','technology-science', 'society', 'culture', 'sports', 'international']
    start_pg, end_pg = 1, 400
    url_box = []
    for topic in topics:
        urls = makeUrl(topic, start_pg, end_pg)
        url_box += urls
    news_titles = news_title_crawling(url_box)
    news_data = preprocessing(news_titles)
    news_data.to_csv('../연합뉴스_크롤링데이터.csv')