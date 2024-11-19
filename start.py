import os
from faster_whisper import WhisperModel
import pysubs2
import yt_dlp
import inquirer
import shutil
from datetime import datetime

# Execuction Time Start

start_time = datetime.now()

# Create temporary directory


PWD = os.getcwd()

path = f"{PWD}/temp"

if not os.path.exists(path):
    os.mkdir(path)

while True:
    # Asking the user to use the audio file already in the computer or fetch from YouTube
    os.system("cls" if os.name == "nt" else "clear")

    questions_audio = [
        inquirer.List(
            "audio",
            message="Are you going to use your local file or fetch the audio from YouTube.",
            choices=["local", "youtube"],
        ),
    ]
    # Set audio's Answer

    answers = inquirer.prompt(questions_audio)

    audio_fetch = answers["audio"]

    # Clear the Screen
    os.system("cls" if os.name == "nt" else "clear")

    if audio_fetch == "local":
        local = input("Where is the file located (mp3 file format only) : ")
    else:
        # Video Download
        links = input("Please type your YouTube Video Link Here and Press Enter : ")
    # Rename the Generated SRT File
    file_rename = input("Please input your filename here : ")
    new_filename = os.path.splitext(file_rename)[0] + ".srt"
    new_filename2 = os.path.splitext(new_filename)[0] + " Transcript.txt"

    # Clear the Screen

    os.system("cls" if os.name == "nt" else "clear")

    # Asking the Whisper Model

    questions = [
        inquirer.List(
            "model",
            message="Please Choose your Whisper Model",
            choices=[
                "tiny.en",
                "tiny",
                "base.en",
                "base",
                "small.en",
                "small",
                "medium.en",
                "medium",
                "large",
                "large-v1",
                "large-v2",
                "large-v3",
                "Custom",
            ],
        ),
    ]
    # Set Model's Answer

    answers = inquirer.prompt(questions)

    model_user = answers["model"]

    # Clear the Screen
    os.system("cls" if os.name == "nt" else "clear")

    if model_user == "Custom":
        model_user = input(
            "Please Enter the Custom Faster-Whisper Model you're going to use."
        )

    # Task Settings

    questions2 = [
        inquirer.List(
            "task",
            message="Please Choose the task you are going to perform",
            choices=["transcribe", "translate"],
        ),
    ]

    answers2 = inquirer.prompt(questions2)

    task = answers2["task"]

    os.system("cls" if os.name == "nt" else "clear")

    # Specify language
    if task.lower() == "transcribe":

        questions3 = [
            inquirer.List(
                "language",
                message="Do you want to Specify language?",
                choices=["yes", "no"],
            ),
        ]

        answers3 = inquirer.prompt(questions3)

        language_choices = answers3["language"]

        os.system("cls" if os.name == "nt" else "clear")

        if language_choices.lower() == "yes":

            language = input("Please type the language you are going to transcribe : ")

            os.system("cls" if os.name == "nt" else "clear")
        else:

            language = "auto"

    elif task.lower() == "translate":

        language = input("Please type the language you are going to translate : ")

        os.system("cls" if os.name == "nt" else "clear")

    # Asking for Plain Document

    questions4 = [
        inquirer.List(
            "transcript",
            message="Do you want to Generate transcript file?",
            choices=["yes", "no"],
        ),
    ]

    answers4 = inquirer.prompt(questions4)

    Generate_Plain_Document = answers4["transcript"]

    os.system("cls" if os.name == "nt" else "clear")

    # Cookies for Downloading Video
    if audio_fetch.lower() == "youtube":
        print(
            "Your cookies might get leaked, and I will not take any responsibility if your account gets stolen."
        )
        print(
            "The recommended approach is to use another Google Account's cookies to run this tool."
        )
        print(
            "If it is a private video, you can share the video with that Google Account to grant access to it."
        )
        print("")

        questions5 = [
            inquirer.List(
                "cookies",
                message="Do you want to enable Cookies login file to Download?",
                choices=["yes", "no"],
            ),
        ]

        answers5 = inquirer.prompt(questions5)

        enable_cookies = answers5["cookies"]

        if enable_cookies.lower() == "yes":
            print("Please Paste your Cookies file location at here")
            cookies_location = input("")
            os.system("cls" if os.name == "nt" else "clear")
        else:
            cookies_location = "Disabled"
            os.system("cls" if os.name == "nt" else "clear")

    # If User Choose Yes in Translate
    if audio_fetch.lower() == "local":
        print("Please Check the Following Settings is Correct or not")
        print("File Path : ", local)
        print("File Name : ", file_rename)
        print("You Are going to : ", task)
        print("Model : ", model_user)
        print("Language : ", language)
        print("Generate Transcript? : ", Generate_Plain_Document)
        print("")
    else:
        print("Please Check the Following Settings is Correct or not")
        print("Video Link : ", links)
        print("File Name : ", file_rename)
        print("You Are going to : ", task)
        print("Model : ", model_user)
        print("Language : ", language)
        print("Enable Cookies? : ", enable_cookies)
        print("Cookies location : ", cookies_location)
        print("Generate Transcript? : ", Generate_Plain_Document)
        print("")

    questions3 = [
        inquirer.List(
            "continue", message="Is these Options all Correct?", choices=["yes", "no"]
        ),
    ]

    answers3 = inquirer.prompt(questions3)

    loopbreaker = answers3["continue"]

    if loopbreaker.lower() == "yes":
        break

# Download the Video
if audio_fetch.lower() == "youtube":
    output_location = f"{PWD}/temp/audio"
    if enable_cookies.lower() == "yes":
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": output_location,
            "cookiefile": cookies_location,
        }
    else:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": output_location,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([links])
elif audio_fetch.lower() == "local":
    shutil.copyfile(f"{local}", f"{PWD}/temp/audio.mp3")


# Import Model and Generating Srt File

model = WhisperModel(model_user)
print("Whisper model loaded.")

filename = "audio.mp3"

input_directory = f"{PWD}/temp"

input_file = f"{input_directory}/{filename}"

# Transcribe with or without specific language setting
if task == "translate":
    segments, info = model.transcribe(input_file, task="translate", language=language)
else:
    if language.strip() == "auto":
        segments, info = model.transcribe(input_file)
        print(
            "Detected language '%s' with probability %f"
            % (info.language, info.language_probability)
        )
    else:
        segments, info = model.transcribe(input_file, language=language)

results = []
print("Starting transcription with verbose output...")
for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    segment_dict = {"start": segment.start, "end": segment.end, "text": segment.text}
    results.append(segment_dict)

if not os.path.exists("Generated"):
    os.mkdir("Generated")

transcription_root = f"{PWD}/Generated/"

# Setup Options for SRT/TXT file
options = {"max_line_width": None, "max_line_count": None, "highlight_words": False}

# Save as SRT
subs = pysubs2.load_from_whisper(results)
srt_path = transcription_root + new_filename
subs.save(srt_path)
print(f"SRT file saved at: {srt_path}")

# Optionally generate plain text file
if Generate_Plain_Document.lower() == "yes":
    txt_path = transcription_root + new_filename2
    with open(txt_path, "w") as txt_file:
        for segment in results:
            txt_file.write(f"{segment['text']}\n")
    print("Generated both SRT and TXT files.")

else:
    print("Generated only SRT file.")

print("Transcription complete!")


# Delete the Temp file

directory_path = os.path.join(os.getcwd(), f"{PWD}/temp")

os.path.exists(directory_path)
shutil.rmtree(directory_path)

end_time = datetime.now()
print("Execution Time: {}".format(end_time - start_time))
