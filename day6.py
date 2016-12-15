from collections import Counter

def day6(messages):
    return ''.join(list(map(lambda x:Counter(x).most_common(1)[0][0],zip(*messages.split('\n')))))

def day6b(messages):
    return ''.join(list(map(lambda x:Counter(x).most_common()[-1][0],zip(*messages.split('\n')))))