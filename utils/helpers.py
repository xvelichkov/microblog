import re


MENTION_REGEX=r"@(\w+)"
HASHTAG_REGEX=r"#(\w+)"

def get_mentions(text):
    mentions = re.findall(MENTION_REGEX, text)
    return mentions

def get_hashtags(text):
    hashtags = re.findall(HASHTAG_REGEX, text)
    return hashtags

def wrap_mentions(match):
    return f'AAAA {match.group()} AAAA'