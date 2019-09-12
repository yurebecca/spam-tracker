import config
import lib
from spam_trainer import svm, vectorizer
from profanity_rater import profanity_severity_rating
from spam_rater import spam_severity_rating
from short_content_rater import short_content_severity_rating

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

    def __init__(self):
        pass

    def set_content(self, text):
        self.content = text
        self.word_count = lib.word_count(self.content)
    
    def predict(self):
        self.predict_spam()
        self.short_rating = short_content_severity_rating(self.word_count)
        self.profanity_rating = profanity_severity_rating(self.content)

    def final_rating(self):
        highest_rating = max([
            self.profanity_rating,
            self.spam_rating,
            self.short_rating,
            self.keyword_stuffing_rating
        ])
        if self.short_rating > 5:
            return self.short_rating
        else:
            return highest_rating
    
    def predict_spam(self):
        msg = vectorizer.transform([self.content])
        prediction = svm.predict(msg)
        self.spam_prediction = prediction[0]
        self.spam_prediction_confidence = svm.predict_proba(msg)
        self.spam_rating = spam_severity_rating(self.spam_prediction_confidence[1])
        return self.spam_prediction