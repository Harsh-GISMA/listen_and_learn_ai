from transformers import pipeline

# 1. Load the BART summarization pipeline
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# 2. Some long text (later this will be your Whisper transcript)
text = """
Investment is an art that every person should learn. As the Indian economy continue to grow the retail investors count is also growing. 
A article in The Indian Express say, According to the Economic Survey 2023-24, the number of retail investors at NSE nearly tripled from March 2020 to March 2024,
with direct ownership in listed companies reaching approximately Rs 36 lakh crore (Vyas, 2023). 
A recent survey has highlighted the ongoing shift in investment trends among young Indians. The revelations in latest Investor Behavior Index (IBI, 2025), 
released by StockGro in collaboration with 1Lattice, show the growing preference for stock market investments, the rising demand for financial education, and the increasing role of digital platforms in shaping investor behavior (Mishra, 2025). 
So, people have started to understand importance of investment. Now the question that arrives is where and how should you invest? That is the reason companies like my client have started offering schemes for retail investors so that they do not have to play the hard part of studying the entire market. 
In other words, we can say that people need guidance for anyone who is new in stocks investment. 
"""

# 3. Run summarization
summary = summarizer(
    text,
    max_length=180,   # adjust as needed
    min_length=60,
    do_sample=False
)[0]["summary_text"]

print("SUMMARY:\n", summary)
