from . import config
from . import lib

config = config.config
sr_config = config['spam_rater']

def spam_severity_rating(is_spam, confidence_of_spam, turn_on = None):
    severity = 0
    if turn_on is None:
        turn_on = sr_config['turn_on']

    if turn_on == False or is_spam == False:
        # Not the best way to do this, because the spam checker code still runs...
        return severity

    confidence_percent = lib.round_half_up(confidence_of_spam * 100)
    if confidence_percent >= sr_config['safe_spam_confidence_percent']:
        severity = sr_config['severity_start']
        # Increase severity as the percentage goes up by the rate set in the config.
        # Max severity will be 10 (set in the config file)
        severity_increase = (confidence_percent - sr_config['safe_spam_confidence_percent']) / sr_config['severity_increment_per_percent']
        severity_increase = lib.round_half_up(severity_increase)

        if severity_increase > config['severity']['max'] - severity:
            severity = config['severity']['max']
        else:
            severity += severity_increase
    elif is_spam:
        severity = sr_config['severity_start']
        

    return severity
