This project turns long lectures into clean, focused study notes. It works best for students who want quick, structured revision from messy recordings or raw text.

## Overview

Listen & Learn AI lets you upload a lecture (or paste text), generates a transcript, then creates clear notes with key concepts and a “study mode” view.  
Behind the scenes, it uses a transformer-based summarization model plus lightweight NLP to surface the most important ideas.

## How it works (short workflow)

For a youtube video on how to use click(https://youtu.be/51J1aFWrUNI).

1. Input  
   - Upload an audio/video lecture file (e.g., MP3, MP4) or paste lecture text directly into the app.  
2. Transcription / text processing  
   - For audio/video, the app runs a speech-to-text model to produce a transcript.  
   - For pasted text, it skips transcription and uses your text as-is.  
3. Summarization  
   - The transcript is split into safe chunks and passed through a summarization model (BART-style).  
   - Partial summaries are combined into a clean, readable set of notes.  
4. Key concepts extraction  
   - A simple keyword extractor ranks the most frequent and relevant terms from the summary (e.g., “gradient descent”, “overfitting”).  
5. Study mode  
   - Important sentences containing multiple key concepts are highlighted.  
   - You can skim the highlighted notes, scan the key concepts, and download your notes as a text file.

## Features

- Two-step workflow  
  - Step 1: “Transcribe / Process Input” – converts audio/video or raw text into a transcript.  
  - Step 2: “Generate Notes” – creates a structured summary from the transcript.

- Notes tab  
  - Shows the full transcript for reference.  
  - Displays AI-generated notes (the main summary).

- Study mode tab  
  - Key Concepts: short list of important terms from the notes.  
  - Highlighted Notes: key sentences bolded for quick revision.  
  - Download Notes: export the notes as a `.txt` file.

## How to run locally

1. Clone the repo

```bash
git clone https://github.com/<your-username>/listen-and-learn-ai.git
cd listen-and-learn-ai
```

2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. (If using audio/video) Install ffmpeg on your system

On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg
```

5. Launch the app

```bash
streamlit run streamlit_app.py
```

Open the URL shown in the terminal 
Or 
Use this link (https://listen-and-learn-ai.streamlit.app/).

## How to use the app

1. Choose your input  
   - Go to the **Settings** sidebar.  
   - Select **Audio**, **Video**, or **Text** from “Input type”.  
   - (Optional) Choose your desired “Summary length” (Auto / Short / Medium / Long).

2. Provide content  
   - Audio: upload a lecture audio file.  
   - Video: upload a lecture video file.  
   - Text: paste the lecture text into the text area.

3. Step 1 – Transcribe / Process  
   - Click **“1️⃣ Transcribe / Process Input”**.  
   - For audio/video, wait while the model generates a transcript.  
   - For text, the app will simply clean and store your input.  
   - When finished, the transcript appears under the **Notes** tab in the “Transcript” box.

4. Step 2 – Generate Notes  
   - Click **“2️⃣ Generate Notes”**.  
   - The summarization model runs and produces concise notes.  
   - The notes appear in the “Notes (Summary)” box in the **Notes** tab.

5. Explore Study Mode  
   - Switch to the **“🎯 Study mode”** tab.  
   - Review **Key Concepts** to see the main terms extracted from your notes.  
   - Read **Highlighted Notes** to quickly scan the most important sentences.  
   - Use **Download Notes** to save the summary as a `.txt` file for later revision.

## When this app is useful

- After lectures, to turn long recordings into short, structured notes.  
- Before exams, to quickly review the key ideas and highlighted sentences.  
- For online courses, to summarize video lessons into text you can search and annotate.

You can adapt the model, UI, or keyword extraction logic to match your course, language, or study preferences.
