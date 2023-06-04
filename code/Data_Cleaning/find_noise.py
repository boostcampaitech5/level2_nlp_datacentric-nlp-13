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

noise = []
text = []
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
        headline = special.sub('',headline)
        headline = re.sub(' +', ' ', headline)
        input_text = special.sub('',d.text)
        input_text = re.sub(' +',' ',input_text)
        print(headline, i)
        print(d.text, i)
        if input_text not in headline and headline not in input_text:
            noise.append(i)
            text.append(d.text)
        i+=1
    except:
        print("차단?")
        time.sleep(300)

    
print("찾은 noise data의 개수:", len(noise))
pd.DataFrame({'idx':noise, 'text':text}).to_csv('./noise_idx.csv', index=False)
