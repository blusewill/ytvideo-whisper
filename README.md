Languages Available：[English](README.md) [繁體中文](README-zh-tw.md)
# ytvideo-whisper

**ytvideo-whisper** is a Python script for downloading YouTube videos and generating SRT subtitles with ease.


## Tested Examples

- [【雀。日麻小教室1】脫離斷么染手對對仔|日麻新手看這邊](https://youtu.be/b_O-TkpYi_w)
- [【雀。日麻小教室 2】脫離斷么染手對對仔|日麻新手看這邊](https://youtu.be/tD2fBWsZrZU)


## Features

- Download YouTube videos and generate SRT subtitles.
- Easily set up and run on local systems or Google Colab.
- Support for custom models.
- Optimized for faster API usage.


## Running on Google Colab

1. Ensure the runtime type is set to **GPU**:
   Runtime -> Change Runtime Type
2. Update the settings in the settings code block.
3. Click:
   Runtime -> Run all (CTRL+F9)
4. Connect to Google Drive.
5. Generated subtitles (SRT) will appear in:  
   Google Drive -> Whisper -> result

### Colab Links

- **Global Version**  
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blusewill/ytvideo-whisper/blob/master/ytvideo_whisper.ipynb)

- **KMN_BOT Special Version (Chinese Traditional)**  
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blusewill/ytvideo-whisper/blob/master/ytvideo_whisper_KMN_BOT_Version.ipynb)


## Installation

### Prerequisites

- Install [Python](https://www.python.org/) on your system.

### Automated Installation (Linux)

1. Run the setup script to set up a virtual environment and install dependencies:
   ```bash
   ./setup-requirement.sh
   ```
2. Run the main script:
   ```bash
   ./run-script.sh
   ```

### Manual Installation

1. Create a Python virtual environment:
   ```bash
   python3 -m venv ./.virtualenv
   ```
2. Activate the virtual environment:
   - **Bash/Zsh**:  
     ```bash
     source ./.virtualenv/bin/activate
     ```
   - **Csh/Tcsh**:  
     ```bash
     source ./.virtualenv/bin/activate.csh
     ```
   - **Fish**:  
     ```bash
     source ./.virtualenv/bin/activate.fish
     ```
   - **Powershell**:  
     - Allow script execution:
       ```powershell
       Set-ExecutionPolicy -ExecutionPolicy Bypass
       ```
     - Activate the virtual environment:
       ```powershell
       ./.virtualenv/bin/Activate.ps1
       ```


## Todo List

- [ ] Add Windows GPU support.
- [x] Implement faster API.
- [x] Support custom models.
- [ ] Add an installation script.


## Contributors

- [blusewill](https://blusewill.us.to) – Creator and local environment tester.  
- [機器狼](https://www.plurk.com/KMN_BOT) – Google Colab tester.  
- [刺蝟瑞歐的小行星](https://www.youtube.com/@RiccioReo) – Test video provider.  

---

Feel free to contribute and make this project even better! 🎉