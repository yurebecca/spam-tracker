# Code taken from https://github.com/kavgan/nlp-in-practice/blob/master/tf-idf/
import os
import re
import pickle
from . import config
from . import lib

config = config.config
ks_config = config['keyword_stuffing']

trained_data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'algorithms')

# Import the trained transformer and vectorizer
with open(os.path.join(trained_data_folder, 'keyword_model.pkl'), 'rb') as f:
    transformer = pickle.load(f)
with open(os.path.join(trained_data_folder, 'keyword_vectorizer.pkl'), 'rb') as f:
    cv = pickle.load(f)

# you only needs to do this once, this is a mapping of index to 
feature_names = cv.get_feature_names()


def keyword_stuffing_severity_rating(content_text, keyword, turn_on = None):
    severity = 0
    if turn_on is None:
        turn_on = ks_config['turn_on']

    if turn_on == False:
        return severity
    
    total_words = lib.word_count(content_text)
    keyword_count = len(re.findall(keyword, content_text))
    keyword_stuffing_percent = lib.round_half_up((keyword_count * 100) / total_words)
    if keyword_stuffing_percent >= ks_config['safe_keyword_stuffing_percent']:
        severity = ks_config['severity_start']
        # Increase severity as the percentage goes up by the rate set in the config.
        # Max severity will be 10 (set in the config file)
        severity_increase = (keyword_stuffing_percent - ks_config['safe_keyword_stuffing_percent']) / ks_config['severity_increment_per_percent']
        severity_increase = lib.round_half_up(severity_increase)

        if severity_increase > config['severity']['max'] - severity:
            severity = config['severity']['max']
        else:
            severity += severity_increase

    return severity

def find_stuffed_keywords(text):
    text = lib.pre_process(text)
    #generate tf-idf for the given text
    tf_idf_vector = transformer.transform(cv.transform([text]))

    #sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())

    #extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)

    return keywords

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

