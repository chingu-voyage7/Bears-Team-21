import string, random

def random_string(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def sub_one(x, y):
    return max(x-y, 1)