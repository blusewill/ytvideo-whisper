import whisper
import yt_dlp
import os
from whisper.utils import get_writer

# Load Whisper's Model "Default Model : Medium" (tiny,base,small,medium,large)

model = whisper.load_model("medium")

print("Whisper model loaded.")

model.device

# Download Audio Files

links = input("Please type your YouTube Video Link Here and Press Enter : ")
name = input("Please type your SRT file name Here and Press Enter : ")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
        'outtmpl': './.tmp/audio',
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([links])

# Start Generating the SRT File

filename = "audio.mp3"
input_directory = ".tmp"
input_file = f"{input_directory}/{filename}"

result = model.transcribe(input_file)
transcription_root = "./result/"

# Save as an SRT file
srt_writer = get_writer("srt", transcription_root,)
srt_writer(result, name,)

# Removing The Temp Audio Files

os.remove(./.tmp/audio.mp3)
