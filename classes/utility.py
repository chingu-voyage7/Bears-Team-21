import string, random, re

def random_string(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def sub_one(x, y):
    return max(x-y, 1)

def alphanum(text):
    return bool(re.match('^[a-zA-Z0-9]+$', text))