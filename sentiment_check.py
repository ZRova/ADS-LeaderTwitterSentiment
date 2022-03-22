from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
#from bs4 import BeautifulSoup
import re

################# MODEL
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

tokens = tokenizer.encode('It was good but couldve been better. Great', return_tensors='pt')
result = model(tokens)
result.logits
int(torch.argmax(result.logits))+1


import numpy as np
import pandas as pd

df = pd.read_csv("borisjohnsonscrape_20220321")
# df = pd.DataFrame(np.array(reviews), columns=['review'])
df['review'].iloc[0]
def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits))+1
sentiment_score(df['review'].iloc[1])
df['sentiment'] = df['review'].apply(lambda x: sentiment_score(x[:512]))
df
df['review'].iloc[3]