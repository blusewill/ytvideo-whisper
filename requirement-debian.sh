if command -v pipx >/dev/null 2>&1 ; then
  echo "pipx is installed run the following command."
  pipx install openai-whisper --include-deps
  pipx install yt-dlp --include-deps
  pipx install ffmpeg-python --include-deps
  pipx install inquirer --include-deps
  sudo apt install python3-requests
  echo "Dependency has already installed"
else
    echo "pipx is not installed. Installing pipx."
    sudo apt install pipx -y
    if command -v pipx > /dev/null 2>&1 ; then
      pipx install openai-whisper
      pipx install yt-dlp
      pipx install ffmpeg-python
      pipx install inquirer
      sudo apt install python3-requests
      echo "Dependency has already installed"
    else
      echo "Can't install pipx. Please install it by typing the following command"
      echo "sudo apt install pipx"
    fi
fi
