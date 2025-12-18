from typing import Literal, Optional, Dict

from transformers import pipeline

_SUMMARIZER = pipeline("summarization", model="facebook/bart-large-cnn")

def _count_words(text: str) -> int:
    return len(text.split())


def _get_length_config(
    text: str,
    user_pref: Optional[Literal["short", "medium", "long"]] = None,
    file_size_mb: Optional[float] = None,
) -> Dict[str, int]:

    word_count = _count_words(text)

    cfg_short = {"min_w": 80, "max_w": 200}    
    cfg_med   = {"min_w": 250, "max_w": 700}     
    cfg_long  = {"min_w": 500, "max_w": 1200}    

    if user_pref not in {"short", "medium", "long"}:
        base_type = "medium"
    else:
        base_type = user_pref

    if word_count < 200:
        base_type = "short"
    elif word_count < 600 and base_type == "long":
        base_type = "medium"

    if file_size_mb is not None and file_size_mb < 2:
        if base_type == "long":
            base_type = "medium"
        if word_count < 200:
            base_type = "short"

    if base_type == "short":
        return cfg_short
    if base_type == "long":
        return cfg_long
    return cfg_med


def _words_to_tokens(word_len: int) -> int:

    return int(word_len * 1.3)

def _chunk_text(text: str, max_chars: int = 3000):
    """
    Split text into chunks no longer than max_chars, cutting on sentence boundaries.
    """
    sentences = text.split(". ")
    chunks = []
    current = []
    current_len = 0

    for sent in sentences:
        sent_len = len(sent) + 2  # account for ". "
        if current_len + sent_len > max_chars and current:
            chunks.append(". ".join(current))
            current = [sent]
            current_len = sent_len
        else:
            current.append(sent)
            current_len += sent_len

    if current:
        chunks.append(". ".join(current))
    return chunks


def _summarize_chunk(chunk: str, user_pref, file_size_mb):
    cfg = _get_length_config(
        chunk,
        user_pref=user_pref,
        file_size_mb=file_size_mb,
    )

    min_tokens = _words_to_tokens(cfg["min_w"])
    max_tokens = _words_to_tokens(cfg["max_w"])
    max_tokens = min(max_tokens, 1024)

    result = _SUMMARIZER(
        chunk,
        min_length=min_tokens,
        max_length=max_tokens,
        do_sample=False,
    )[0]["summary_text"]

    return result.strip()

def summarize_transcript(
    transcript: str,
    user_pref: Optional[Literal["short", "medium", "long"]] = None,
    file_size_mb: Optional[float] = None,
) -> str:
    transcript = transcript.strip()
    if not transcript:
        return ""

    # 1) Split long transcript into safe chunks
    chunks = _chunk_text(transcript, max_chars=3000)

    # 2) Summarize each chunk
    partial_summaries = []
    for chunk in chunks:
        summary_piece = _summarize_chunk(chunk, user_pref, file_size_mb)
        partial_summaries.append(summary_piece)

    # 3) Optionally, summarize the combined summaries once more
    combined = " ".join(partial_summaries)

    if len(combined.split()) < 400:
        # Already short enough
        return combined.strip()

    # Final “summary of summaries”
    final_cfg = _get_length_config(
        combined,
        user_pref=user_pref,
        file_size_mb=file_size_mb,
    )
    final_min = _words_to_tokens(final_cfg["min_w"])
    final_max = _words_to_tokens(final_cfg["max_w"])
    final_max = min(final_max, 1024)

    final = _SUMMARIZER(
        combined,
        min_length=final_min,
        max_length=final_max,
        do_sample=False,
    )[0]["summary_text"]

    return final.strip()


if __name__ == "__main__":
    sample_text = (
        "In today's lecture, we discussed linear regression and its applications in "
        "predictive analytics. First, we introduced the idea of modeling the relationship "
        "between a dependent variable and one or more independent variables. "
        "Then, we explored the least squares method and how to estimate parameters..."
    )

    print("=== SHORT SUMMARY ===")
    print(summarize_transcript(sample_text, user_pref="short", file_size_mb=1.0))
    print("\n=== MEDIUM SUMMARY (DEFAULT) ===")
    print(summarize_transcript(sample_text, user_pref=None, file_size_mb=1.0))
    print("\n=== LONG SUMMARY (WILL BE DOWNGRADED IF TEXT TOO SHORT) ===")
    print(summarize_transcript(sample_text, user_pref="long", file_size_mb=1.0))

