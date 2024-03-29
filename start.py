import os
import yt_dlp
import whisper
from whisper.utils import get_writer
from transfersh_client.app import send_to_transfersh, create_zip, remove_file
import inquirer
import shutil
import requests

# Create temporary directory

path = './temp'

if not os.path.exists(path):
  os.mkdir(path)

while True:

    os.system('cls' if os.name=='nt' else 'clear')


# Asking Question

# Video Download
    links = input("Please type your YouTube Video Link Here and Press Enter : ")
# Rename the Generated SRT File
    file_rename = input("Please input your filename here : ")
    new_filename = os.path.splitext(file_rename)[0] + ".srt"
    new_filename2 = os.path.splitext(new_filename)[0] + " Transcript.txt"


# Clear the Screen

    os.system('cls' if os.name=='nt' else 'clear')


# Asking the Whisper Model

    questions = [
        inquirer.List('model', message='Please Choose your Whisper Model', choices=['tiny.en','tiny','base.en','base','small.en','small','medium.en','medium','large-v1','large-v2','large']),
    ]
# Set Model's Answer

    answers = inquirer.prompt(questions)

    model_user = answers['model']

# Clear the Screen
    os.system('cls' if os.name=='nt' else 'clear')

# Task Settings

    questions2 = [
        inquirer.List('task', message='Please Choose the task you are going to perform', choices=['transcribe', 'translate']),
    ]

    answers2 = inquirer.prompt(questions2)

    task = answers2['task']

    os.system('cls' if os.name=='nt' else 'clear')

# Specify language
    if task.lower() == 'transcribe':
        
        questions3 = [
            inquirer.List('language', message='Do you want to Specify language?', choices=['yes', 'no']),
        ]

        answers3 = inquirer.prompt(questions3)

        language_choices = answers3['language']

        os.system('cls' if os.name=='nt' else 'clear')

        if language_choices.lower() == 'yes':
            
            language = input("Please type the language you are going to transcribe : ")

        else:
            
            language = "auto"

    elif task.lower() == 'translate':
        language = input("Please type the language you are going to translate : ")
        os.system('cls' if os.name=='nt' else 'clear')

# Asking for Plain Document
    
    questions4 = [
            inquirer.List('transcript', message='Do you want to Generate transcript file?', choices=['yes', 'no']),
            
            ]

    answers4 = inquirer.prompt(questions4)

    Generate_Plain_Document = answers4['transcript']

    os.system('cls' if os.name=='nt' else 'clear')

# Cookies for Downloading Video
      
    print("Your cookies might get leaked, and I will not take any responsibility if your account gets stolen.")
    print("The recommended approach is to use another Google Account's cookies to run this tool.")
    print("If it is a private video, you can share the video with that Google Account to grant access to it.")
    print("")
    
    questions5 = [
            inquirer.List('cookies', message='Do you want to enable Cookies login file to Download?', choices=['yes', 'no']),
            ]
    
    answers5 = inquirer.prompt(questions5)

    enable_cookies = answers5['cookies']
    
    if enable_cookies.lower() == 'yes':
        print("Please Paste your Cookies file location at here")
        cookies_location = input("")
    else:
        cookies_location = "Disabled"

    os.system('cls' if os.name=='nt' else 'clear')

# If User Choose Yes in Translate

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
                inquirer.List('continue', message='Is these Options all Correct?', choices=['yes', 'no']),
            ]

    answers3 = inquirer.prompt(questions3)

    loopbreaker = answers3['continue']

    if loopbreaker.lower() == "yes":
        break

# Download the Video

import yt_dlp

if enable_cookies.lower() == "yes":

  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }],
          'outtmpl': './temp/audio',
          'cookiefile': cookies_location
  }

else:

    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }],
          'outtmpl': './temp/audio',
  }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([links])

# Import Model and Generating Srt File

model = whisper.load_model(model_user)

print("Whisper model loaded.")

filename = "audio.mp3"

input_directory = "./temp"

input_file = f"{input_directory}/{filename}"

if language.lower() == 'auto':
  result = model.transcribe(input_file, verbose=True, task=task)
else:
  result = model.transcribe(input_file, verbose=True, task=task, language=language)
if not os.path.exists("Generated"):
    os.mkdir("Generated")

transcription_root = "./Generated"

# Setup Options for SRT/TXT file
options = {
    'max_line_width': None,
    'max_line_count': None,
    'highlight_words': False
}

# Save as an SRT file
srt_writer = get_writer("srt", transcription_root,)
srt_writer(result, new_filename, options)

if Generate_Plain_Document.lower() == "yes":

  # Save as TXT file
  srt_writer = get_writer("txt", transcription_root,)
  srt_writer(result, new_filename2,options)
  print("Generated srt and txt file in the Generated Folder.")

else:

  print("Generated srt file in the Generated Folder.")


# Delete the Temp file

directory_path = os.path.join(os.getcwd(), './temp')

os.path.exists(directory_path)
shutil.rmtree(directory_path)


# Asking for Upload to anonfile
questions6 = [
            inquirer.List('upload', message='Do you want to Upload the Generated file to cloud service?', choices=['yes', 'no']),
            ]

answers6 = inquirer.prompt(questions6)

upload_file_cloud = answers6['upload']

# Asking for upload service

if upload_file_cloud.lower() == "yes":
   
   archived = shutil.make_archive(file_rename, 'zip', './temparchive')

   questions7 = [
            inquirer.List('service', message='Please choose your cloud services?', choices=['anonfiles', 'transfer.sh']),
            ]

   answers7 = inquirer.prompt(questions7)

   cloud_service = answers7['service']


# Anonfile

if cloud_service.lower() == "anonfiles":
# Output to Another directory (./temparchive)
    if not os.path.exists("temparchive"):
        os.mkdir("temparchive")
    
    srt_writer = get_writer("srt", "./temparchive",)
    srt_writer(result, new_filename)
    
    if Generate_Plain_Document.lower() == "yes":
        srt_writer = get_writer("txt", "./temparchive",)
        srt_writer(result, new_filename2)
        print("Generated srt and txt file in the Generated Folder.")

# Creating the ZIP file
    
    if os.path.exists(archived):
        print(archived)

    anonfile_api = 'https://api.anonfiles.com/upload'
    zip_path = os.path.abspath(archived)

    with open(zip_path, 'rb') as f:
        # Send a POST request to the Anonfile API with the archive file as the payload
        response = requests.post(anonfile_api, files={'file': f})

    # Check if the upload was successful
    if response.status_code == 200:
        # Print the download URL of the uploaded file
        print(response.json()['data']['file']['url']['full'])
        os.remove(zip_path)
        shutil.rmtree("temparchive")
    else:
        # Print an error message
        print('Error the Following Status Code is : ', response.status_code, "Maybe the anonfile API is currently offline, if not please send a message in issues on github")
        os.remove(zip_path)
        shutil.rmtree("temparchive")
else:
     
     def send_files_from_dir():
         directory = '/content'
         send_to_transfersh(archived, clipboard=False)  # sends archive to transfer.sh


     if __name__ == '__main__':
        send_files_from_dir()
