import re
import textwrap
from pathlib import Path

import streamlit as st

from wisper_setup import process_input
from NLP_BERT import summarize_transcript
from nlp_keywords import extract_keywords

CUSTOM_CSS = """
<style>
/* Full-page university students studying background */
.stApp {
    background: url("https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?auto=format&fit=crop&w=1600&q=80")
                no-repeat center fixed;
    background-size: cover;
    font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

/* Solid light overlay behind all content for readability */
[data-testid="stAppViewContainer"] > .main {
    background-color: #F9FAFB;  /* almost white */
}

/* Dark sidebar with light text */
[data-testid="stSidebar"] {
    background-color: #020617;
}
[data-testid="stSidebar"] * {
    color: #F9FAFB !important;
    font-weight: 700 !important;
}

/* Headings: black and bold */
h1 {
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: #000000 !important;
}
h2, h3, h4, h5, h6 {
    font-weight: 800 !important;
    color: #000000 !important;
}

/* All normal text: black and bold */
p, label, span, div, textarea {
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 0.96rem;
}

/* Captions / debug text: dark gray but still clear */
small, .caption, .stCaption {
    color: #374151 !important;
    font-weight: 600 !important;
}

/* Card containers */
.card {
    padding: 1.1rem 1.35rem;
    margin-bottom: 1rem;
    background-color: #FFFFFF;
    border-radius: 0.9rem;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18);
}

/* Textareas: light background, clear border, bigger font */
textarea {
    border-radius: 0.9rem !important;
    border: 1px solid #9CA3AF !important;
    font-size: 0.98rem !important;
    line-height: 1.45 !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* High-contrast buttons: dark purple, white bold text */
.stButton > button {
    background: #312E81;
    color: #FFFFFF !important;
    border-radius: 999px;
    border: none;
    padding: 0.6rem 1.6rem;
    font-weight: 800 !important;
    font-size: 0.98rem;
    letter-spacing: 0.02em;
    box-shadow: 0 10px 22px rgba(55, 48, 163, 0.55);
    transition: all 0.15s ease-out;
}
.stButton > button:hover {
    background: #1E1B4B;
    transform: translateY(-1px);
    box-shadow: 0 14px 28px rgba(55, 48, 163, 0.70);
}
.stButton > button:active {
    transform: translateY(1px);
    box-shadow: 0 6px 16px rgba(55, 48, 163, 0.60);
}

/* Tabs: clear labels */
[data-testid="stTabs"] button {
    font-weight: 800;
    font-size: 0.95rem;
    color: #000000;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #312E81;
}

/* Content width */
.block-container {
    padding-top: 2.0rem;
    max-width: 1100px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def highlight_summary(summary: str, keywords: list[str], max_lines: int = 6) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', summary.strip())
    highlighted = []
    for sent in sentences:
        count = sum(1 for kw in keywords if kw.lower() in sent.lower())
        if count >= 2:
            highlighted.append(f"**{sent}**")
        else:
            highlighted.append(sent)
    text = " ".join(highlighted)
    return textwrap.shorten(text, width=1000, placeholder=" ...")


st.set_page_config(
    page_title="Listen & Learn AI",
    layout="wide",
    page_icon="🎧",
)

if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""
if "segments" not in st.session_state:
    st.session_state["segments"] = []
if "summary" not in st.session_state:
    st.session_state["summary"] = ""
if "file_size_mb" not in st.session_state:
    st.session_state["file_size_mb"] = None

st.sidebar.title("Settings")

input_type = st.sidebar.selectbox(
    "Input type",
    ["Audio", "Video", "Text"],
)

summary_pref_label = st.sidebar.selectbox(
    "Summary length",
    ["Auto (default)", "Short", "Medium", "Long"],
)

pref_map = {
    "Auto (default)": None,
    "Short": "short",
    "Medium": "medium",
    "Long": "long",
}
user_pref = pref_map[summary_pref_label]

st.sidebar.markdown("---")
st.sidebar.write("Max file size (approx.) is enforced in the app logic.")

st.title("🎧 Listen & Learn AI")
st.markdown(
    "Turn long lectures into **clean notes**, key concepts, and a focused study view in seconds."
)

MAX_MB = 10

uploaded_file = None
text_input = None

if input_type == "Audio":
    uploaded_file = st.file_uploader(
        "Upload audio file",
        type=["mp3", "wav", "m4a"],
    )
elif input_type == "Video":
    uploaded_file = st.file_uploader(
        "Upload video file",
        type=["mp4", "mkv", "mov"],
    )
else:
    text_input = st.text_area("Paste or type your text here", height=150)

col_left, col_right = st.columns(2)
with col_left:
    transcribe_btn = st.button("1️⃣ Transcribe / Process Input", use_container_width=True)
with col_right:
    notes_btn = st.button("2️⃣ Generate Notes", use_container_width=True)

if transcribe_btn:
    if input_type == "Text":
        if not text_input or not text_input.strip():
            st.error("Please enter some text first.")
        else:
            text, segments = process_input(text_input, is_text=True)
            st.session_state["transcript"] = text
            st.session_state["segments"] = segments
            st.session_state["file_size_mb"] = None
            st.success("Text processed successfully.")
    else:
        if uploaded_file is None:
            st.error(f"Please upload a {input_type.lower()} file first.")
        else:
            raw = uploaded_file.getvalue()
            file_size_mb = len(raw) / (1024 * 1024)
            st.session_state["file_size_mb"] = file_size_mb

            if file_size_mb > MAX_MB:
                st.error(
                    f"File too large ({file_size_mb:.1f} MB). "
                    f"Please upload a file under {MAX_MB} MB."
                )
            else:
                suffix = ".mp3" if input_type == "Audio" else ".mp4"
                temp_path = Path(f"temp_input{suffix}")
                temp_path.write_bytes(raw)

                with st.spinner("Running Whisper (tiny) on your file..."):
                    try:
                        text, segments = process_input(temp_path, is_text=False)
                        st.session_state["transcript"] = text
                        st.session_state["segments"] = segments
                        st.success("Transcription completed.")
                    except Exception as e:
                        st.error(f"Error during transcription: {e}")

st.markdown("---")

tab_notes, tab_study = st.tabs(["📝 Notes", "🎯 Study mode"])

with tab_notes:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Transcript and Notes")

    st.markdown("#### Transcript")
    st.text_area(
        "Transcript",
        value=st.session_state["transcript"],
        height=250,
    )

    st.caption(f"DEBUG transcript length: {len(st.session_state['transcript'])} chars")
    st.caption(f"DEBUG summary length: {len(st.session_state['summary'])} chars")

    if notes_btn:
        st.caption("DEBUG: notes_btn clicked")
        if not st.session_state["transcript"].strip():
            st.error("No transcript available. Please transcribe/process input first.")
        else:
            with st.spinner("Generating notes with BART..."):
                try:
                    summary = summarize_transcript(
                        st.session_state["transcript"],
                        user_pref=user_pref,
                        file_size_mb=st.session_state.get("file_size_mb"),
                    )
                    st.session_state["summary"] = summary
                    st.caption(f"DEBUG summary set, length: {len(summary)} chars")
                    st.success("Notes generated.")
                except Exception as e:
                    st.error(f"Error during summarization: {e}")

    st.markdown("#### Notes (Summary)")
    st.text_area(
        "Notes",
        value=st.session_state["summary"],
        height=250,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with tab_study:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Key Concepts")
    if st.session_state["summary"].strip():
        keywords = extract_keywords(st.session_state["summary"], top_n=8)
        if keywords:
            st.write(", ".join(f"`{kw}`" for kw in keywords))
        else:
            st.write("No key concepts detected.")
    else:
        st.write("Generate notes first to see key concepts.")

    st.subheader("Highlighted Notes")
    if st.session_state["summary"].strip():
        keywords = extract_keywords(st.session_state["summary"], top_n=8)
        highlighted_md = highlight_summary(st.session_state["summary"], keywords)
        st.markdown(highlighted_md)
    else:
        st.write("Generate notes first to see highlighted version.")

    st.subheader("Download Notes")
    if st.session_state["summary"].strip():
        st.download_button(
            label="Download notes as .txt",
            data=st.session_state["summary"],
            file_name="listen_and_learn_notes.txt",
            mime="text/plain",
        )
    else:
        st.write("Generate notes first to download.")
    st.markdown('</div>', unsafe_allow_html=True)
