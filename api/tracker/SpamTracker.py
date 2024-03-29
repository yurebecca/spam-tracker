import os
import pickle
import operator
from . import config
from . import lib
from .profanity_rater import profanity_severity_rating
from .spam_rater import spam_severity_rating
from .short_content_rater import short_content_severity_rating
from .keyword_stuffing_rater import keyword_stuffing_severity_rating, find_stuffed_keywords

# Import the trained svm and vectorizer
trained_data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'algorithms')
with open(os.path.join(trained_data_folder, 'spam_model.pkl'), 'rb') as f:
    svm = pickle.load(f)
with open(os.path.join(trained_data_folder, 'spam_model_vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

class SpamTracker:
    """Spam Tracker Class"""

    content = ""
    word_count = 0

    # Ratings
    profanity_rating = 0
    spam_rating = 0
    short_rating = 0
    keyword_stuffing_rating = 0

    spam_prediction = 0 # Default to ham (0 - ham; 1 - spam;)
    spam_prediction_confidence = 0
    severity_type = None

    keywords = []

    def __init__(self):
        pass

    def set_content(self, text):
        self.content = text
        self.word_count = lib.word_count(self.content)
    
    def reset(self):
        content = ""
        word_count = 0
        profanity_rating = 0
        spam_rating = 0
        short_rating = 0
        keyword_stuffing_rating = 0
        spam_prediction = 0
        spam_prediction_confidence = 0
        severity_type = None
        keywords = []
    
    def predict(self):
        self.predict_spam()
        self.short_rating = short_content_severity_rating(self.word_count)
        self.profanity_rating = profanity_severity_rating(self.content)

        self.keywords = find_stuffed_keywords(self.content)
        stuffed_keyword = None
        for k in self.keywords:
            if stuffed_keyword is None:
                stuffed_keyword = k
            self.keywords[k] = float(self.keywords[k])
        self.keyword_stuffing_rating = keyword_stuffing_severity_rating(self.content, stuffed_keyword)

    def final_rating(self):
        ratings = {
            "profanity": self.profanity_rating,
            "spam": self.spam_rating,
            "short_content": self.short_rating,
            "keyword_stuffing": self.keyword_stuffing_rating
        }
        self.severity_type = max(ratings.items(), key=operator.itemgetter(1))[0]
        highest_rating = ratings[self.severity_type]
        if self.short_rating > 5:
            self.severity_type = "short_content"
            highest_rating = ratings[self.severity_type]
        if highest_rating == 0:
            self.severity_type = None
        return highest_rating
    
    def predict_spam(self):
        msg = vectorizer.transform([self.content])
        prediction = svm.predict(msg)
        self.spam_prediction = prediction[0]
        self.spam_prediction_confidence = svm.predict_proba(msg)[0]
        self.spam_rating = spam_severity_rating(self.spam_prediction, self.spam_prediction_confidence[1])
        return self.spam_prediction
    
    def get_ratings(self):
        return {
            "profanity_rating": self.profanity_rating,
            "spam_rating": self.spam_rating,
            "short_rating": self.short_rating,
            "keyword_stuffing_rating": self.keyword_stuffing_rating,

            "spam": {
                "spam_prediction": int(self.spam_prediction),
                "spam_prediction_confidence": [float(self.spam_prediction_confidence[0]), float(self.spam_prediction_confidence[1])],
            },
            "keywords": self.keywords
        }