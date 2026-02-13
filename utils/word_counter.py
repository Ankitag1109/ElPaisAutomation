from collections import Counter
import re

def count_words(titles):
    words = []
    for title in titles:
        clean = re.findall(r'\b[a-zA-Z]+\b', title.lower())
        words.extend(clean)

    counter = Counter(words)

    print("\nWord Frequency:")
    for word, count in counter.most_common(10):
        print(word, ":", count)

    return counter
