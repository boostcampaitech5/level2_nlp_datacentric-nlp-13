import random
import pandas as pd
from hanspell import spell_checker
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random

def delete_random_word(sentence):
    """
    문장 내 임의 단어 삭제한 문장 반환하는 함수

    Args:
        sentence (str): 임의 단어 삭제할 문장

    Returns:
        str: 임의 단어 삭제된 문장
    """
    words = sentence.split()
    num_words = len(words)
    words_to_delete = random.sample(range(num_words), 1)
    augmented_words = [word for i, word in enumerate(words) if i not in words_to_delete]
    augmented_sentence = ' '.join(augmented_words)
    return str(augmented_sentence)

def random_deletion(dataset):
    """
    임의 단어 삭제 함수

    Args:
        dataset (pd.DataFrame): 원본 data

    Returns:
        pd.DataFrame
    """
    sens = []
    for i in list(dataset.index):
        a = dataset['text'][i]
        sen = delete_random_word(a)
        sens.append(sen)
    dataset['text'] = sens
    dataset = dataset.dropna()
    return dataset

def get_word(label):
    """
    주어진 label에 있는 단어 중 랜덤 단어 반환

    Args:
        label (int): target 숫자

    Returns:
        str: 선택된 랜덤 단어
    """
    data = pd.read_csv('./data/no_noise.csv')
    words = []
    sentences = data[data['target'] == label]['text'].tolist()
    for sentence in sentences:
        words += sentence.split()
    word = random.choice(words)
    return word

def random_insertion(dataset):
    """
    문장에 랜덤 단어 삽입

    Args:
        dataset (pd.DataFrame): 원본 data

    Returns:
        pd.DataFrame
    """
    sens = []
    for i in list(dataset.index):
        word = get_word(dataset['target'][i])
        sentence = dataset['text'][i]
        sen = sentence.split(' ')
        length = len(sen)
        id = random.randrange(length)
        sen.insert(id, word)
        sens.append(' '.join(sen))
    dataset['text'] = sens
    return dataset
        
def han_spell(dataset):
    """
    띄어쓰기 교정해주는 함수

    Args:
        dataset (pd.DataFrame): 원본 data

    Returns:
        pd.DataFrame
    """
    sens = []
    for i in list(dataset.index):
        a = dataset['text'][i]
        spelled_sent = spell_checker.check(a)
        checked_sent = spelled_sent.checked
        sens.append(checked_sent)
    dataset['text'] = sens
    dataset = dataset.dropna()
    return dataset

def translate(dataset):
    """
    T5모델 이용해 역번역해주는 함수

    Args:
        dataset (pd.DataFrame): 원본 data

    Returns:
        pd.DataFrame
    """
    tokenizer = AutoTokenizer.from_pretrained("KETI-AIR-Downstream/long-ke-t5-base-translation-aihub-ko2en")
    model = AutoModelForSeq2SeqLM.from_pretrained("KETI-AIR-Downstream/long-ke-t5-base-translation-aihub-ko2en")
    tokenizer2 = AutoTokenizer.from_pretrained("KETI-AIR-Downstream/long-ke-t5-base-translation-aihub-en2ko")
    model2 = AutoModelForSeq2SeqLM.from_pretrained("KETI-AIR-Downstream/long-ke-t5-base-translation-aihub-en2ko")
    sens = []
    for i in list(dataset.index):
        a = dataset['text'][i]
        input = tokenizer(a, return_tensors = "pt")
        input_id = input.input_ids
        output = model.generate(input_id)
        trans = tokenizer.decode(output[0], skip_special_tokens = True)
        input2 = tokenizer2(trans, return_tensors = "pt")
        input_id2 = inpu2.input_ids
        output2 = model2.gerenate(input_id2)
        btrans = tokenizer2.decode(output2[0], skip_special_tokens = True)
        sens.append(btrans)
    dataset['text'] = sens
    return dataset

if __name__ == '__main__':
    train_data = pd.read_csv('../data/no_noise_data.csv')
    train_data2 = translate(train_data)
    train = pd.concat([train_data, train_data2])
    train.to_csv('../data/backtrans.csv')