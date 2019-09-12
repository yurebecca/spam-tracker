from config import config
import lib

sr_config = config['spam_rater']

def spam_severity_rating(confidence_of_spam):
    severity = 0
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

    return severity
