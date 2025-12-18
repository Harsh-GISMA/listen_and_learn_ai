from collections import Counter
import re

STOPWORDS = {
    "the", "and", "a", "an", "to", "of", "in", "on", "for", "is", "are",
    "was", "were", "it", "this", "that", "with", "as", "by", "at", "from",
    "or", "be", "we", "you", "they", "i", "our", "their", "your",
    "so", "if", "but", "not", "no", "do", "does", "did", "can", "could",
    "should", "would", "have", "has", "had", "will", "just", "about",
    "into", "out", "up", "down", "over", "under", "than", "then", "very"
}

def extract_keywords(text: str, top_n: int = 10):
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z]+", text)
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_n)]
