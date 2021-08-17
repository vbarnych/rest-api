from recognize import recognizeAudio

from tensorflow import keras
from tensorflow.keras.layers import Dense, LSTM, Input, Dropout, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

with open('train_data_true', 'r', encoding='utf-8') as f:
    texts_true = f.readlines()
    texts_true[0] = texts_true[0].replace('\ufeff', '') #убираем первый невидимый символ

with open('train_data_false', 'r', encoding='utf-8') as f:
    texts_false = f.readlines()
    texts_false[0] = texts_false[0].replace('\ufeff', '') #убираем первый невидимый символ

texts = texts_true + texts_false
count_true = len(texts_true)
count_false = len(texts_false)
total_lines = count_true + count_false
#print(count_true, count_false, total_lines)

maxWordsCount = 1000
tokenizer = Tokenizer(num_words=maxWordsCount, filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»', lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts(texts)
dist = list(tokenizer.word_counts.items())
#print(dist[:10])
#print(texts[0][:100])

max_text_len = 10
data = tokenizer.texts_to_sequences(texts)
data_pad = pad_sequences(data, maxlen=max_text_len)

X = data_pad
Y = np.array([[1, 0]]*count_true + [[0, 1]]*count_false)

indeces = np.random.choice(X.shape[0], size=X.shape[0], replace=False)
X = X[indeces]
Y = Y[indeces]


model_LSTM = keras.models.load_model("classifyModel.h5")

reverse_word_map = dict(map(reversed, tokenizer.word_index.items()))

def sequence_to_text(list_of_indices):
    words = [reverse_word_map.get(letter) for letter in list_of_indices]
    return(words)




def classifyAudio(path):

    t = recognizeAudio(path)
    
    data = tokenizer.texts_to_sequences([t])
    data_pad = pad_sequences(data, maxlen=max_text_len)


    res = model_LSTM.predict(data_pad)
    print(res, np.argmax(res), sep='\n')
    if np.argmax(res) == 0:
        return "Affirmative"
    else:
        return "Negative"

    