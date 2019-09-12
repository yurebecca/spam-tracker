import re
from profanity_filter import ProfanityFilter
from config import config
import lib


pr_config = config['profanity_rater']

pf = ProfanityFilter(analyses=pr_config['languages'], languages=pr_config['languages'])
pf.censor_char = '*'
pf.extra_profane_word_dictionaries = pr_config['extra_profane_word_dictionary']


def profanity_severity_rating(content_text):
    cencored_text = pf.censor(content_text)
    profane_words = re.findall(f"\{pf.censor_char}+", cencored_text)
    total_words = lib.word_count(content_text)
    percent_profane = (len(profane_words) / total_words) * 100

    severity = 0
    if percent_profane > pr_config['safe_profanity_percent']:
        severity = pr_config['severity_start']
        # Increase severity as the percentage goes up by the rate set in the config.
        # Max severity will be 10 (set in the config file)
        severity_increase = (percent_profane - pr_config['safe_profanity_percent']) / pr_config['severity_increment_per_percent']
        severity_increase = lib.round_half_up(severity_increase)

        if severity_increase > config['severity']['max'] - severity:
            severity = config['severity']['max']
        else:
            severity += severity_increase
    elif len(profane_words) > 0:
        severity = pr_config['severity_start']

    return severity


# print(profanity_severity_rating("Hello world! Why are you so bright and beautiful? That's bullshit."))