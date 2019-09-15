# Code taken from https://github.com/kavgan/nlp-in-practice/blob/master/tf-idf/
import os
import re
import pickle
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from . import lib
import lib

# read json into a dataframe
data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
data = pd.read_json(os.path.join(data_folder, 'stackoverflow-data-idf.txt'), lines=True)


def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

data['text'] = data['title'] + data['body']
data['text'] = data['text'].apply(lambda x:lib.pre_process(x))

#load a set of stop words
# stopwords = get_stop_words(os.path.join(data_folder, 'stopwords.txt'))
stopwords = set(stopwords.words('english'))

#get the text column 
docs = data['text'].tolist()
 
#create a vocabulary of words, 
#ignore words that appear in 85% of documents, 
#eliminate stop words
cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
word_count_vector = cv.fit_transform(docs)

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

# Save trained algorithm to a file
trained_data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'algorithms')
with open(os.path.join(trained_data_folder, 'keyword_model.pkl'), 'wb') as f:
    pickle.dump(tfidf_transformer, f)
with open(os.path.join(trained_data_folder, 'keyword_vectorizer.pkl'), 'wb') as f:
    pickle.dump(cv, f)
