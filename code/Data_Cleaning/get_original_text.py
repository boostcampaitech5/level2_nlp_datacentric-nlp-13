import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import html
import time

BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, './data')

data = pd.read_csv(DATA_DIR+'/train.csv')

texts = []
special = re.compile(r'[^ A-Za-z0-9가-힣]')

i=0
while i<45677:
    d=data.iloc[i]
    try:  
        url = d.url
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})
        article_html = r.content
        soup = BeautifulSoup(article_html, 'html.parser')
        if 'sports' not in url:
            headline = soup.select('#title_area')
            headline = str(headline[0])
        else:
            headline = soup.find("h4")
            headline = str(headline)
        headline = BeautifulSoup(headline, "lxml").text
        print(headline)
        texts.append(headline)
        i+=1
    except:
        print("차단?")
        time.sleep(300)

pd.DataFrame({'ID': data.ID,'text': texts, 'target': data.target, 'url': data.url, 'date': data.date}).to_csv('./original_text.csv', index=False)