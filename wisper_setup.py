import whisper
from pathlib import Path
from pprint import pprint
from timeit import timeit


model = whisper.load_model("base")  # or "base"
path = Path.cwd() / "Test audio 2.mp3"


def convert_audio_to_text(audio_path: str):
    result =  model.transcribe(audio_path, word_timestamps=True)
    return result

result = convert_audio_to_text(path.absolute().as_posix())


# result = model.transcribe("Test audio 2.mp3", word_timestamps=True)
print(result["text"])
pprint(result)
print(timeit("func()", number=1000, globals=globals()))


