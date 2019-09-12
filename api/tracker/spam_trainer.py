# Medium https://towardsdatascience.com/spam-or-ham-introduction-to-natural-language-processing-part-2-a0093185aebd
# Code taken from https://github.com/happilyeverafter95/Medium/blob/master/spam_or_ham.py
import os
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import confusion_matrix

data_csv = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'emails.csv')

data = pd.read_csv(data_csv, encoding = "latin-1")
data = data.rename(columns = {'spam': 'label', 'text': 'text'})
# Every mail starts with 'Subject :' will remove this from each text 
data['text'] = data['text'].map(lambda text: text[1:])

lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))

def review_messages(msg):
    # converting messages to lowercase
    msg = msg.lower()

    return msg

def alternative_review_messages(msg):
    # converting messages to lowercase
    msg = msg.lower()

    # uses a lemmatizer (wnpos is the parts of speech tag)
    # unfortunately wordnet and nltk uses a different set of terminology for pos tags
    # first, we must translate the nltk pos to wordnet
    nltk_pos = [tag[1] for tag in pos_tag(word_tokenize(msg))]
    msg = [tag[0] for tag in pos_tag(word_tokenize(msg))]
    wnpos = ['a' if tag[0] == 'J' else tag[0].lower() if tag[0] in ['N', 'R', 'V'] else 'n' for tag in nltk_pos]
    msg = " ".join([lemmatizer.lemmatize(word, wnpos[i]) for i, word in enumerate(msg)])

    # removing stopwords 
    msg = " ".join([word for word in msg.split() if word not in stopwords])

    return msg

# Processing text messages
data['text'] = data['text'].apply(review_messages)

# train test split 
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size = 0.1, random_state = 1)

# training vectorizer
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)

# training the classifier 
svm = svm.SVC(C=1000, gamma='scale')
svm.fit(X_train, y_train)

# testing against testing set 
X_test = vectorizer.transform(X_test)
y_pred = svm.predict(X_test)
print("Trained Spam Classifier results:")
print(confusion_matrix(y_test, y_pred))
