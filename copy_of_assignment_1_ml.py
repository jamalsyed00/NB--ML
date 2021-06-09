# -*- coding: utf-8 -*-
"""Copy of Assignment_1_ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18tljbzMzK4wJMhJcmdPNDMf6lKaYfR79
"""

import nltk
import string
import random

f = open("dataset_NB.txt", "r")
f = f.read().split("\n")
data_global = []
val_global = []
for sent in f:
  l = len(sent)
  data_global.append(sent[:l-1].strip())
  val_global.append(int(sent[l-1]))

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.remove("no")
stop_words.remove("not")

from nltk import word_tokenize

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def text_preprocess(sentence):
  # Lowercase
  sentence = sentence.lower()
  # Puntuation removal
  sentence = "".join([char for char in sentence if char not in string.punctuation])
  # Tokenization
  words = word_tokenize(sentence)
  # StopWord removal
  words = [word for word in words if word not in stop_words]
  # Lemmetizer
  words = [lemmatizer.lemmatize(word) for word in words]

  return words

def preprocess(data,val):
  pos = {}
  neg = {}
  pos_size = 0
  neg_size = 0
  vocab_size = 0
  pos_val_frequency = 0
  neg_val_frequency = 0
  for j in range(0,len(val)):
    sentence = data[j]
    vocab_size = 0
    words = text_preprocess(sentence)
    if val[j] == 1:
      pos_val_frequency += 1
      for word in words:
        if word in pos:
          pos[word] = pos[word]+1
        else:
          pos[word] = 1
          if word not in neg:
            vocab_size += 1

    else:
      neg_val_frequency += 1
      for word in words:
        if word in neg:
          neg[word] = neg[word]+1
        else:
          neg[word] = 1
          if word not in pos:
            vocab_size += 1

  for key in pos:
    pos_size = pos_size + pos[key]

  for key in neg:
    neg_size = neg_size + neg[key]

  pos_val_frequency /= len(train_data)
  neg_val_frequency /= len(train_data)

  return pos,neg,pos_size,neg_size,vocab_size,pos_val_frequency,neg_val_frequency

def classify_nb(test_data,train_data,train_val,alpha):
  pos,neg,pos_size,neg_size,vocab_size,pos_freq,neg_freq = preprocess(train_data,train_val)

  predicted_val = []

  for j in range(0,len(test_data)):
    words = text_preprocess(test_data[j])
    pos_prob = 1
    neg_prob = 1

    for word in words:
      if word in pos:
        pos_prob = pos_prob*(pos[word]+alpha)/(pos_size+vocab_size)
      else:
        pos_prob = pos_prob*alpha/(pos_size+vocab_size)

      if word in neg:
        neg_prob = neg_prob*(neg[word]+alpha)/(neg_size+vocab_size)
      else:
        neg_prob = neg_prob*alpha/(neg_size+vocab_size)

    pos_prob *= pos_freq
    neg_prob *= neg_freq

    if neg_prob > pos_prob:
      predicted_val.append(0)
    else:
      predicted_val.append(1)

  return predicted_val

if __name__ == '__main__':
  temp = list(zip(data_global, val_global))
  random.shuffle(temp)
  data_global, val_global  = zip(*temp)

  alpha = 1

  k_len = int(len(val_global)/7)

  avg_accuracy: float = 0.0

  for i in range (0,7):
    test_data = data_global[0:k_len]
    train_data = data_global[k_len:]
    test_val = val_global[0:k_len]
    train_val = val_global[k_len:]

    data_global = train_data + test_data
    val_global = train_val + test_data

    local_accuracy = 0

    predicted_val = classify_nb(test_data,train_data,train_val,alpha)

    for j in range (0,len(predicted_val)):
      if predicted_val[j] == test_val[j]:
        local_accuracy = local_accuracy + 1

    local_accuracy = local_accuracy/(len(predicted_val))

    print("Accuracy for " +str(i+1)+ "th iteration is "+str(local_accuracy))
    avg_accuracy = avg_accuracy+local_accuracy

  avg_accuracy = avg_accuracy/7
  print("Average Accuracy is "+str(avg_accuracy))