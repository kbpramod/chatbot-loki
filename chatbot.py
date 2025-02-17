# -*- coding: utf-8 -*-
"""chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_FQOGmAHgJ-LwA6bjDzcNuIqGmnQ1mKB
"""

import random
import json
import pickle
import numpy as np

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("/content/intents.json").read())

words = []
classes = []
documents = []
ignore_words = ['!','.','?',',']  #ignored words

nltk.download('punkt_tab')
nltk.download('wordnet')

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)  #splitting sentence to list of words
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_words]
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words,open('/content/words.pkl','wb'))
pickle.dump(classes,open('/content/classes.pkl','wb'))

training = []
output_empty = [0]*len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)

len(training)

max_len = max(len(x[0]) for x in training)
max_len

for i in range(len(training)):
    bag_len = len(training[i][1])
    if bag_len < max_len:
        padding = [0] * (max_len - bag_len)
        training[i][1].extend(padding)

training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save(chatbot_loki.model)

model.save('chatbot_loki.h5')

model.save('chatbot_loki.keras')

from tensorflow.keras.models import load_model
model_loaded = load_model('/content/chatbot_loki.h5')

model_loaded.summary()

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model_loaded.predict(np.array([bow]))[0]
    Error_threshold =0.25
    results = [[i,r] for  i,r in enumerate(res) if r > Error_threshold]

    results.sort(key=lambda x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

while True:
    message = input("You: ")
    if message.lower() in ["stop", "exit", "quit"]:
        print("Chatbot stopped.")
        break
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("Bot:", res)