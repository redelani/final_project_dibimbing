import joblib
import json
import nltk
import numpy as np
import pandas as pd
import pickle

nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# Text pre-processing
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping


try:
    with open('models/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
        
    model = joblib.load("models/modelDense_tuned.sav")
except FileNotFoundError:
    raise RuntimeError("Model file not found!")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

def preprocessing(data):
    data = data.str.lower()
    data = data.str.replace(r'[^a-zA-Z\s]', '', regex=True)
    data = data.apply(word_tokenize)
    with open('data/combined_slang_words.txt', 'r', encoding='utf-8') as file:
        kamus_normalisasi = json.load(file)
    data = data.apply(lambda x: [kamus_normalisasi.get(kata, kata) for kata in x])
    with open('data/combined_stop_words.txt', 'r', encoding='utf-8') as file:
        stop_words = set(file.read().splitlines())
        stop_words.update(['sih', 'siih', 'si', 'sii', 'siii', 'iya', 'ya', 'yaa', 'nya', 'ku', 'yg', 'tp', 'gtu', 'deh', 'tuh', 'tuhh', 'tuuhh', 'ituuuuuu', 'iniii', 'hehe', 'he', 'e', 'eh', 'ehh', 'jg', 'ku', 'lah', 'laah', 'an', 'nge', 'kak', 'wkwk', 'wkwkwk', 'haha', 'hahaha', 'hahahaha', 'hhi', 'hihi', 'hihihi', 'hihihihi', 'hehe', 'hehehe', 'hehehehe', 'an', 'we', 'weh', 'yuk', 'yuuk', 'aaaaa', 'aaaaaaaaa', 'aaaaakkkkk', 'aaah', 'ahhh', 'aaaa', 'aaaaaa', 'aaaaaakkkkk'])
    data = data.apply(lambda x: [word for word in x if word not in stop_words])
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data = data.apply(lambda x: [stemmer.stem(word) for word in x])
    data = data.apply(lambda x: ' '.join(x))
    return data

def predict_sentiment(text):
    # Defining pre-processing parameters
    
    max_len = 50
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = '<OOV>'
    vocab_size = 500
    
    predict_msg = preprocessing(pd.Series([text]))
    print(predict_msg)  
    new_seq = tokenizer.texts_to_sequences(predict_msg)
    print(new_seq)
    padded = pad_sequences(new_seq,
                         maxlen = max_len,
                         padding = padding_type,
                         truncating = trunc_type)
    print("done padded")
    prediction = model.predict(padded)
    predicted_classes = ['1' if prob > 0.5 else '0' for prob in prediction]
    print(predicted_classes)
    return predicted_classes