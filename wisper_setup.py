from pathlib import Path
from typing import List, Dict, Union, Tuple

import whisper

_WHISPER_MODEL = whisper.load_model("tiny")

def transcribe_media(
    media_path: Union[str, Path]
) -> Tuple[str, List[Dict[str, Union[float, str]]]]:
    
    media_path = Path(media_path)

    if not media_path.exists():
        raise FileNotFoundError(f"File not found: {media_path}")
    
    result = _WHISPER_MODEL.transcribe(str(media_path))

    full_text = result.get("text", "").strip()

    segments = [
        {
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": seg["text"].strip(),
        }
        for seg in result.get("segments", [])
    ]

    return full_text, segments


def process_input(
    input_data: Union[str, Path],
    is_text: bool = False
) -> Tuple[str, List[Dict[str, Union[float, str]]]]:

    if is_text:
    
        text = str(input_data).strip()
        return text, []

    return transcribe_media(input_data)



if __name__ == "__main__":
    test_media_path = "sample_audio.mp3"

    print("Transcribing media file with Whisper tiny...")
    try:
        transcript, segs = transcribe_media(test_media_path)
        print("\n=== FULL TRANSCRIPT ===")
        print(transcript)

        print("\n=== FIRST 5 SEGMENTS (WITH TIMESTAMPS) ===")
        for s in segs[:5]:
            print(f"[{s['start']:.1f} - {s['end']:.1f}] {s['text']}")

    except FileNotFoundError as e:
        print(e)

    
    raw_text = "This is some example text that would normally come from a text input."
    text_out, segs_out = process_input(raw_text, is_text=True)
    print("\n=== BYPASS WHISPER (TEXT INPUT) ===")
    print("Text:", text_out)
    print("Segments:", segs_out)



