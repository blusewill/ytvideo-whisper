## ytvideo-whisper

This is a Project that Download YouTube video and Generate the SRT subtitle python script

Which is a can be used easily I guess?????


## Tested Video Example

[【雀。日麻小教室1】脫離斷么染手對對仔|日麻新手看這邊](https://youtu.be/b_O-TkpYi_w)

[【雀。日麻小教室 2】脫離斷么染手對對仔|日麻新手看這邊](https://youtu.be/tD2fBWsZrZU)


## Installation

Install [Python](https://www.python.org/) on your system

### Linux Method

You can run the following scripts to set it up.

`./setup-requirement.sh `

Will setup a Virtual Environment and install the dependency package all in one go!

And After the installation all you have to run is

`./run-script.sh`

It will mount the Virtual Environment and execute the script

### Manual Method

Create a Python Virtual Environment

`python3 -m venv ./.virtualenv`

Activate the Virtual Environment

bash/zsh : `source ./.virtualenv/bin/activate`

csh/tcsh : `source ./.virtualenv/bin/activate.csh`

fish : `source ./.virtualenv/bin/activate.fish`

Powershell :

Allow the Powershell execution 

`Set-ExecutionPolicy -ExecutionPolicy Bypass`

And Run the following Powershell Script

`./.virtualenv/bin/Activate.ps1`

## Run in Google Colab

1. Check the Runtime Type is on GPU Mode in ``Runtime -> Change Runtime Type``
1. Change the Settings at Settings Code Block
1. Click ``Runtime -> Run all`` (CTRL+F9)
1. Click on the Connect to Google Drive
1. And Wait for a moment your Generated Srt should be on ``Google Drive -> Whisper -> result``

### Global Version

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blusewill/ytvideo-whisper/blob/master/ytvideo_whisper.ipynb)

### [KMN_BOT 機器狼](https://twitter.com/V_KMN_BOT) Special Version (Chinese Traditional Version)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blusewill/ytvideo-whisper/blob/master/ytvideo_whisper_KMN_BOT_Version.ipynb)


## Todo list

- [ ] Windows GPU Support
- [x] Implment Faster API
- [x] Custom Model
- [ ] Installation Script

Contribution are also Welcome!


## Thanks to The Contributor of this Project

[blusewill](https://blusewill.us.to)
Tester of local Environment and Creator of this Project

[機器狼🤖語音辨識AI](https://www.plurk.com/KMN_BOT)
Tester of Google Colab Project

[刺蝟瑞歐的小行星](https://www.youtube.com/@RiccioReo)
The Test Video Provider
