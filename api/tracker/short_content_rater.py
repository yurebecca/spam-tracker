from config import config
import lib

sc_config = config['short_content']

def short_content_severity_rating(wordcount):
    severity = 0
    if wordcount <= sc_config['min_wordcount']:
        severity = sc_config['severity_start']
        # Increase severity as the percentage goes up by the rate set in the config.
        # Max severity will be 10 (set in the config file)
        severity_increase = (sc_config['min_wordcount'] - wordcount)  / sc_config['severity_increment_per_wordcount']
        severity_increase = lib.round_half_up(severity_increase)

        if severity_increase > config['severity']['max'] - severity:
            severity = config['severity']['max']
        else:
            severity += severity_increase

    return severity
