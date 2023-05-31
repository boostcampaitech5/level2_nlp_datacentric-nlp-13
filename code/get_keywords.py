## sudo apt install default-jdk 터미널에 실행해주세영
from konlpy.tag import Komoran
from konlpy.utils import pprint
from collections import Counter
import re
import pandas as pd

LAB2NUM = {'IT과학': 0,
         '경제': 1,
         '사회': 2,
         '생활문화': 3,
         '세계': 4,
         '스포츠': 5,
         '정치': 6,
         }

NUM2LAB = {0 : 'IT과학',
           1 : '경제',
           2 : '사회',
           3 : '생활문화',
           4 : '세계',
           5 : '스포츠',
           6 : '정치'}


# Initialize Komoran for Korean morphological analysis
komoran = Komoran()

def get_predefined_label(train_data):
    """
    설명 : url column으로 언론사에서 자체 분류한 target을 구하는 함수
    parameters : 기존 train data(pd.DataFrame)
    return : predefined 컬럼이 추가 된 데이터(pd.DataFrame)
    """
    naver = {'105' : 'IT과학',
         '104' : '세계',
         '103' : '생활문화',
         '102' : '사회',
         '101' : '경제',
         '100' : '정치'
         }

    pre_target = []
    for url in train_data['url']:
        if 'sports' in url:
            pre_target.append(LAB2NUM['스포츠'])
        else:
            p = re.compile(r'sid1=10[0-5]')
            num = p.findall(url)[0][5:8]
            pre_target.append(LAB2NUM[naver[num]])

    train_data['predefined'] = pre_target

    return train_data

# Define a function to extract keywords from text
def extract_keywords(text):
    '''
    설명 : text(str type)를 넣으면 형태소 분석을 해서 명사, 용언, 수식언만 추출하는 함수
    input : text(str type)
    return : keywords(list type)
    '''
    # Tokenize the text using Komoran
    tokens = komoran.pos(text)
    
    # Define the POS tags for nouns, verbs, and modifiers
    pos_tags = ['NNG', 'NNP', 'NNBC', 'NR', 'NP', 'VV', 'VA', 'VX', 'MM', 'MAG', 'MAJ']
    keywords = [token[0] for token in tokens if token[1] in pos_tags]
    
    return keywords

def get_keyword_of_target(target, train_data):
    '''
    설명 : 입력한 target의 keyword와 빈도수 추출
    input
    - target : 키워드를 추출할 target(str)
    - train_data : 입력 데이터 (pd.DataFrame)
    return : ['keyword','count'] column의 output(pd.DataFrame)
    '''
    target = LAB2NUM[target]
    target_data = train_data[train_data['target'] == target]
    target_keywords = []
    for text in target_data['text']:
        keywords = extract_keywords(text)
        target_keywords.extend(keywords)
    frequency = Counter(target_keywords)
    sorted_keywords = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    output = pd.DataFrame(sorted_keywords[:500], columns=['keyword','count'])
    return output


def compare_keywords(target, train_data):
    '''
    설명 : target과 predefined를 비교해서 같을 때와 다를 때의 keyword를 비교하는 함수
    input : 비교할 target(str)
    return
    - same : target과 predefined가 같은 text data의 keyword(pd.DataFrame)
    - diff : target과 predefined가 다른 text data의 keyword(pd.DataFrame)
    '''
    t = LAB2NUM[target]
    data = train_data[train_data['predefined'] == t]
    same = get_keyword_of_target(target, data)
    data = train_data[train_data['predefined'] != t]
    diff = get_keyword_of_target(target, data)
    output = pd.concat([same, diff], axis=1)
    return output


if __name__ == '__main__':
    train = pd.read_csv('../data/train_with_predefined.csv')
    target = '정치'
    #train = get_predefined_label(train)
    #output = get_keyword_of_target(target, train):
    output = compare_keywords(target, train)
    print(f'{target} 키워드 비교')
    print(output.head(10))