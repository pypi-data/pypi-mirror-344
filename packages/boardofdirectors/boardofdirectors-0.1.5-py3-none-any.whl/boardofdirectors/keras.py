class Libraries:
    text = '''
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib import style
# import seaborn as sns

# %matplotlib inline 
# style.use('fivethirtyeight')
# sns.set(style='whitegrid', color_codes=True)

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk import word_tokenize, sent_tokenize

from tensorflow.keras.preprocessing.text import one_hot, Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Embedding, Input
from tensorflow.keras.models import Model
'''

    def __str__(self):
        return self.text

class Code:
    text = '''
text_1 = "bitty bought a bit of butter"
text_2 = "but the bit of butter was a bit bitter"
text_3 = "so she bought some better butter to make the bitter butter better"

crop = [text_1, text_2, text_3]
no_docs = len(crop)

print(crop)
print(no_docs)

vocabulary_size = 50
encoded_crop = []

for i, doc in enumerate(crop):
    encoded = one_hot(doc, vocabulary_size)
    encoded_crop.append(encoded)
    print("The encoding for document", i+1, "is:", encoded)

print("\\n", encoded_crop)

maxlen = -1

for doc in crop:
    tokens = nltk.word_tokenize(doc)
    if maxlen < len(tokens):
        maxlen = len(tokens)
print("The maximum number of words in any document is:", maxlen)

padded_crop = pad_sequences(encoded_crop, maxlen=maxlen, padding='post', value=0.0)
print("Number of padded documents:", len(padded_crop))

for i, doc in enumerate(padded_crop):
    print("The padded encoding for document", i+1, "is:", doc)

input = Input(shape=(maxlen,))
embedding = Embedding(input_dim=vocabulary_size, output_dim=8, input_length=maxlen)(input)
flatten = Flatten()(embedding)
output = Dense(1, activation='sigmoid')(flatten)

model = Model(inputs=[input], outputs=[output])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()
'''

    def __str__(self):
        return self.text
