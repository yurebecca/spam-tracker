import pytest
from api import routes
from api.tracker import lib
from api.tracker.config import config
from api.tracker.short_content_rater import short_content_severity_rating
from api.tracker.profanity_rater import profanity_severity_rating
from api.tracker.spam_rater import spam_severity_rating


# 100 word `lorem ipsum` text
lorem_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam nec libero lacus. Donec volutpat odio in risus consectetur, at posuere sapien egestas. Integer interdum libero ac arcu vestibulum tempor. Nunc molestie risus sed arcu tincidunt auctor. Nullam venenatis, nibh vel rhoncus rutrum, erat enim pellentesque quam, eget venenatis massa lorem vitae arcu. Quisque tempus tempor magna, a faucibus ligula commodo eu. Donec fermentum dui et ex ornare auctor. Morbi pellentesque erat nulla, quis cursus tellus gravida ac. Cras eu volutpat enim. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Phasellus mollis laoreet tempus. Pellentesque quis."
profane_word = "shit"

# Check settings
def test_content_length_config_settings():
    assert config['short_content']['severity_start'] <= config['severity']['max']
def test_profanity_config_settings():
    assert config['profanity_rater']['severity_start'] <= config['severity']['max']
def test_spam_config_settings():
    assert config['spam_rater']['severity_start'] <= config['severity']['max']


# Tests for short_content_rater
def test_content_length_long():
    assert short_content_severity_rating(config['short_content']['min_wordcount'] + 1, True) == 0

def test_content_length_short():
    assert short_content_severity_rating(config['short_content']['min_wordcount'], True) == config['short_content']['severity_start']

def test_content_length_shorter():
    if config['short_content']['severity_start'] < config['severity']['max']:
        assert short_content_severity_rating(
            config['short_content']['min_wordcount'] - config['short_content']['severity_increment_per_wordcount'], True
        ) == config['short_content']['severity_start'] + 1
    else:
        assert short_content_severity_rating(
            config['short_content']['min_wordcount'] - config['short_content']['severity_increment_per_wordcount'], True
        ) == config['severity']['max']

def test_content_length_off_long():
    assert short_content_severity_rating(config['short_content']['min_wordcount'] + 1, False) == 0

def test_content_length_off_short():
    assert short_content_severity_rating(config['short_content']['min_wordcount'], False) == 0

def test_content_length_off_shorter():
    assert short_content_severity_rating(
        config['short_content']['min_wordcount'] - config['short_content']['severity_increment_per_wordcount'], False
    ) == 0


# Tests for profanity_rater
def test_profanity_none():
    assert profanity_severity_rating(lorem_text, True) == 0

def test_profanity_some():
    text = " ".join([lorem_text, profane_word])
    word_count = lib.word_count(text)
    profane_percent = (1 * 100) / word_count
    safe_profanity_percent = config['profanity_rater']['safe_profanity_percent']
    if profane_percent > safe_profanity_percent:
        pytest.skip(f"Unsupported Configuration: {profane_percent} > {safe_profanity_percent} (config.json)")
    else:
        assert profanity_severity_rating(text, True) == config['profanity_rater']['severity_start']

def test_profanity_many():
    profane_wordcount = 1
    text = " ".join([lorem_text, profane_word])
    word_count = lib.word_count(text)
    profane_percent = (profane_wordcount * 100) / word_count
    too_profane_percent = config['profanity_rater']['safe_profanity_percent'] + config['profanity_rater']['severity_increment_per_percent']
    if profane_percent > too_profane_percent:
        if config['profanity_rater']['severity_start'] < config['severity']['max']:
            assert profanity_severity_rating(text, True) > config['profanity_rater']['severity_start']
        else:
            assert profanity_severity_rating(text, True) == config['severity']['max']

    while profane_percent < too_profane_percent:
        profane_wordcount += 1
        text = " ".join([text, profane_word])
        word_count = lib.word_count(text)
        profane_percent = (profane_wordcount * 100) / word_count

    if config['profanity_rater']['severity_start'] < config['severity']['max']:
        assert profanity_severity_rating(text, True) > config['profanity_rater']['severity_start']
    else:
        assert profanity_severity_rating(text, True) == config['severity']['max']

def test_profanity_off_none():
    assert profanity_severity_rating(lorem_text, False) == 0

def test_profanity_off_some():
    text = " ".join([lorem_text, profane_word])
    word_count = lib.word_count(text)
    profane_percent = (1 * 100) / word_count
    safe_profanity_percent = config['profanity_rater']['safe_profanity_percent']
    assert profanity_severity_rating(text, False) == 0

def test_profanity_off_many():
    profane_wordcount = 1
    text = " ".join([lorem_text, profane_word])
    word_count = lib.word_count(text)
    profane_percent = (profane_wordcount * 100) / word_count
    too_profane_percent = config['profanity_rater']['safe_profanity_percent'] + config['profanity_rater']['severity_increment_per_percent']
    if profane_percent > too_profane_percent:
        assert profanity_severity_rating(text, True) == 0

    while profane_percent < too_profane_percent:
        profane_wordcount += 1
        text = " ".join([text, profane_word])
        word_count = lib.word_count(text)
        profane_percent = (profane_wordcount * 100) / word_count

    assert profanity_severity_rating(text, False) == 0


# Tests for spam_rater
def test_spam_for_ham():
    assert spam_severity_rating(0, 0, True) == 0

def test_spam_for_slight_spam():
    assert spam_severity_rating(1, (config['spam_rater']['safe_spam_confidence_percent'] - 1) / 100, True) == config['spam_rater']['severity_start']

def test_spam_for_super_spam():
    too_spam_percent = config['spam_rater']['safe_spam_confidence_percent'] + config['spam_rater']['severity_increment_per_percent']
    if config['spam_rater']['severity_start'] < config['severity']['max']:
        assert spam_severity_rating(1, too_spam_percent / 100, True) == config['spam_rater']['severity_start'] + 1
    else:
        assert spam_severity_rating(1, too_spam_percent / 100, True) == config['severity']['max']

def test_spam_off_for_ham():
    assert spam_severity_rating(0, 0, False) == 0

def test_spam_off_for_slight_spam():
    assert spam_severity_rating(1, (config['spam_rater']['safe_spam_confidence_percent'] - 1) / 100, False) == 0

def test_spam_off_for_super_spam():
    too_spam_percent = config['spam_rater']['safe_spam_confidence_percent'] + config['spam_rater']['severity_increment_per_percent']
    assert spam_severity_rating(1, too_spam_percent / 100, False) == 0
