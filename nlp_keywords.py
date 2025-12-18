from collections import Counter
import re

import nltk
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))


def extract_keywords(text: str, top_n: int = 10):
    text = text.lower()
    # keep words only
    tokens = re.findall(r"[a-zA-Z]+", text)

    # filter stopwords and tiny words
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]

    counts = Counter(tokens)
    keywords = [w for w, _ in counts.most_common(top_n)]
    return keywords
