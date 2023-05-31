#pip install koeda
from koeda import SR, RI, RS, RD
from tqdm.auto import tqdm
import pandas as pd

def sr(df, num):
    """
    문장 내 단어를 유의어로 바꿔주는 함수입니다.

    필요 라이브러리 :
    pip install koeda

    Args:
        df (pd.DataFrame): 원본 data
        num (float) : 변형의 정도

    Returns:
        pd.DataFrame    
    """
    sr_df = df.copy()
    text = df['text'].to_list()

    func = SR("Okt")

    for i in tqdm(range(len(text))):
        text[i] = func(text[i], num)

    sr_df['text'] = text  

    return sr_df

def ri(df, num):
    """
    문장 내에 유의어를 무작위로 삽입하는 함수입니다.

    필요 라이브러리 :
    pip install koeda

    Args:
        df (pd.DataFrame): 원본 data
        num (float) : 변형의 정도

    Returns:
        pd.DataFrame    
    """
    ri_df = df.copy()
    text = df['text'].to_list()

    func = RI("Okt")
    for i in tqdm(range(len(text))):
        text[i] = func(text[i], num)

    ri_df['text'] = text  

    return ri_df

def rs(df, num):
    """
    문장 내 단어들의 위치를 바꾸는 함수입니다.
    필요 라이브러리 :
    pip install koeda

    Args:
        df (pd.DataFrame): 원본 data
        num (float) : 변형의 정도

    Returns:
        pd.DataFrame    
    """
    rs_df = df.copy()
    text = df['text'].to_list()

    func = RS("Okt")
    for i in tqdm(range(len(text))):
        text[i] = func(text[i], num)

    rs_df['text'] = text     

    return rs_df

def rd(df, num):
    """
    문장 내 단어를 무작위로 삭제하는 함수입니다.

    필요 라이브러리 :
    pip install koeda

    Args:
        df (pd.DataFrame): 원본 data
        num (float) : 변형의 정도

    Returns:
        pd.DataFrame    
    """
    rd_df = df.copy()
    text = df['text'].to_list()

    func = RD("Okt")
    for i in tqdm(range(len(text))):
        text[i] = func(text[i], num)

    rd_df['text'] = text  

    return rd_df

if __name__ == '__main__':
    num = 0.3 # 변형 정도
    data = pd.read_csv("data/no_noise_del_keyword.csv")
    random_swap = rs(data, num)
    # 아래로 쭉쭉 추가해서 concat list에 aug 할 거 추가해주세여
    print(random_swap.head(5))
    output = pd.concat([data, random_swap])
    print(f'기존 데이터 길이 : {len(data)}')
    print(f'증강 후 데이터 길이 : {len(output)}')
    output.to_csv('data/aug_data_rs.csv')
    print("SUCCESSFULLY SAVED!")