from datetime import datetime
import getpass
from nicegui import ui, run
import os
from faster_whisper import WhisperModel
import pysubs2
import yt_dlp
import inquirer
import shutil
import argparse
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument(
    "--cli", help="Run cli version of ytvideo-whisper", action="store_true"
)
args = parser.parse_args()

cli_ver = args.cli


# Common Element using on every single webpage.
def common_element():
    ui.page_title("ytvideo-whisper WebUI")
    ui.add_head_html(
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" rel="stylesheet" />'
    )
    dark = ui.dark_mode()
    dark.auto() 
    with ui.row().classes("w-full items-center text-2xl"):
        ui.html(
            '<a href="/"><b>ytvideo-whisper WebUI</a></b><p class="text-sm">Alpha v1</p>'
        )
        ui.label().classes("mr-auto")
        ui.button(
            icon="fa-brands fa-github-alt",
            color="#5e81ac",
            on_click=lambda: ui.navigate.to(
                "https://github.com/blusewill/ytvideo-whisper", new_tab=True
            ),
        )
        with ui.button(icon="fa-solid fa-language", color="#5e81ac"):
            with ui.menu():
                ui.menu_item("English", lambda: ui.navigate.to("/"))
                ui.menu_item("繁體中文", lambda: ui.navigate.to("/zh-tw"))
                ui.separator()


@ui.page("/")
async def index():
    global youtube_url
    global file_name
    global task
    global model_user
    global Custom_Model
    global cookies_file
    global switch_cookies
    global upload_local_files
    global local_files
    global language
    global Generate_Plain_Document
    common_element()
    with ui.row().classes("w-full text-4xl"):
        ui.space()
        ui.markdown(f"{greet_by_time()} **{getpass.getuser()}**")
        ui.space()

    with ui.row().classes("w-full"):
        with ui.column():
            ui.markdown("**General Settings**").classes("text-3xl")
            local_files = ui.switch("Enable Local Files", on_change=lambda e: (str(e.value)))
            upload_local_files = ui.upload(max_files=1).bind_visibility_from(local_files, "value")
            youtube_url = (
                ui.input("YouTube URL", value="https://youtu.be/GeCP-0nuziE")
                .classes("w-96")
            )
            file_name = (
                ui.input("File Name", value="The TRUTH About How LTT Makes Money")
                .classes("w-96")
                .props("clearable")
            )
            with ui.input(label="Language", value="Auto").classes("w-96") as language:
                ui.button(on_click=lambda: language.set_value("Auto"), icon="refresh").props('flat dense')
            task = ui.select(
                ["transcribe", "translate"], value="transcribe", label="task"
            ).classes("w-96")
            Generate_Plain_Document = ui.switch("Generate Plain Document", value=True)

            ui.markdown("**Other Options**").classes("text-3xl")
            model_user = ui.select(
                [
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
                value="medium",
                label="Model",
            ).classes("w-96")
            Custom_Model = ui.input(
                "Custom Model", value="XA9/faster-whisper-large-v2-cantonese-1"
            ).classes("w-96")
            switch_cookies = ui.switch("Enable Cookies")
            cookies_file = ui.upload(max_files=1).bind_visibility_from(switch_cookies, "value")
            ui.button('Start', on_click=whisper_run)
def greet_by_time():
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 15:
        return "Good Afternoon!"
    elif 15 <= hour < 24 or 0 <= hour < 5:
        return "Good Evening!"
    else:
        return "ERROR!"


async def whisper_on_click():
    await whisper_run()

async def whisper_run():
    globals()
    with ui.dialog() as dialog, ui.card():
                ui.label(f"The Following Execution will display on the Terminal. \n Due to NiceGUI's limitation. \n It's not possible for not letting the process to be execute at the same time. \n This will change in the future update.").classes("text-xl")
                confirmation = ui.button('Got it.', on_click=dialog.close)
    dialog.open()
    await confirmation.clicked()
    dialog.close()
    await asyncio.sleep(1)
    if switch_cookies.value == True:
        download_with_cookies = 1
    else:
        download_with_cookies = 0
    PWD = os.getcwd()
    path = f"{PWD}/temp"

    if not os.path.exists(path):
        os.mkdir(path)
 
    new_filename = os.path.splitext(file_name.value)[0] + ".srt"
    new_filename2 = os.path.splitext(file_name.value)[0] + " Transcript.txt"

    if local_files.value == False:
       output_location = f"{PWD}/temp/audio"
       if download_with_cookies == 1:
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
               "cookiefile": cookies_file,
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
           ydl.download([youtube_url.value])
    elif local_files.value == False:
       shutil.copyfile(f"{upload_local_files}", f"{PWD}/temp/audio.mp3")

    if model_user.value == "Custom":
        model = WhisperModel(Custom_Model.value)
    else:
        model = WhisperModel(model_user.value)
    filename = "audio.mp3"

    input_directory = f"{PWD}/temp"

    input_file = f"{input_directory}/{filename}"

    if task.value == "translate":
        segments, info = model.transcribe(
        input_file, task="translate", language=language
    )

    else:
        if language.value == "Auto":
            segments, info = model.transcribe(input_file)
            print(
                "Detected language '%s' with probability %f"
                % (info.language, info.language_probability)
            )
        else:
            segments, info = model.transcribe(input_file, language=language.value)
    results = []

    print("Starting transcription with verbose output...")
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        segment_dict = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
        }
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
    if Generate_Plain_Document.value == True:
        txt_path = transcription_root + new_filename2
        with open(txt_path, "w") as txt_file:
            for segment in results:
                txt_file.write(f"{segment['text']}\n")
        print("Generated both SRT and TXT files.")

    else:
        print("Generated only SRT file.")

    print("Transcription complete!")

    directory_path = os.path.join(os.getcwd(), f"{PWD}/temp")

    os.path.exists(directory_path)
    shutil.rmtree(directory_path)


@ui.page("/zh-tw")
async def zh_tw():
    global youtube_url
    global file_name
    global task
    global model_user
    global Custom_Model
    global cookies_file
    global switch_cookies
    global upload_local_files
    global local_files
    global language
    global Generate_Plain_Document
    common_element()
    with ui.row().classes("w-full text-6xl"):
        ui.space()
        ui.markdown(f"{greet_by_time_zh_tw()}**{getpass.getuser()}**")
        ui.space()

    with ui.row().classes("w-full"):
        with ui.column():
            ui.markdown("**一般設定**").classes("text-3xl")
            local_files = ui.switch("啟用本地上傳音檔", on_change=lambda e: (str(e.value)))
            upload_local_files = ui.upload(max_files=1).bind_visibility_from(local_files, "value")
            youtube_url = (
                ui.input("YouTube 連接", value="https://youtu.be/GeCP-0nuziE")
                .classes("w-96")
            )
            file_name = (
                ui.input("檔案名稱", value="The TRUTH About How LTT Makes Money")
                .classes("w-96")
                .props("clearable")
            )
            with ui.input(label="語言", value="Auto").classes("w-96") as language:
                ui.button(on_click=lambda: language.set_value("Auto"), icon="refresh").props('flat dense')
            task = ui.select(
                ["transcribe", "translate"], value="transcribe", label="操作"
            ).classes("w-96")
            Generate_Plain_Document = ui.switch("生成純文字檔", value=True)

            ui.markdown("**其他選項**").classes("text-3xl")
            model_user = ui.select(
                [
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
                value="medium",
                label="模型",
            ).classes("w-96")
            Custom_Model = ui.input(
                "自訂模型", value="XA9/faster-whisper-large-v2-cantonese-1"
            ).classes("w-96")
            switch_cookies = ui.switch("啟用 Cookies 登入階段")
            cookies_file = ui.upload(max_files=1).bind_visibility_from(switch_cookies, "value")
            ui.button('開始', on_click=whisper_run)


def greet_by_time_zh_tw():
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "早安！"
    elif 12 <= hour < 18:
        return "午安！"
    else:
        return "晚安！"


# Cli Version Code
def run_cli():
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

                language = input(
                    "Please type the language you are going to transcribe : "
                )

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
                "continue",
                message="Is these Options all Correct?",
                choices=["yes", "no"],
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
        segments, info = model.transcribe(
            input_file, task="translate", language=language
        )
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
        segment_dict = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
        }
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


if cli_ver == True:
    run_cli()
else:
    ui.run()
