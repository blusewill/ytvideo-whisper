語言：[English](README.md) [繁體中文](README-zh-tw.md)
# ytvideo-whisper

**ytvideo-whisper** 是一個用於下載 YouTube 影片並生成 SRT 字幕的 Python 腳本，簡單易用。


## 測試範例

- [【雀。日麻小教室1】脫離斷么染手對對仔|日麻新手看這邊](https://youtu.be/b_O-TkpYi_w)  
- [【雀。日麻小教室 2】脫離斷么染手對對仔|日麻新手看這邊](https://youtu.be/tD2fBWsZrZU)


## 功能特色

- 下載 YouTube 影片並生成 SRT 字幕檔。  
- 支援本地系統或 Google Colab 的簡易部署。  
- 支援自訂模型。  
- 針對更快的 API 使用進行最佳化。  


## 在 Google Colab 上執行

1. 確保執行環境類型設為 **GPU**：  
   Runtime -> Change Runtime Type  
2. 更新設定區塊中的設定參數。  
3. 點擊以下指令：  
   Runtime -> Run all (CTRL+F9)  
4. 連接 Google Drive。  
5. 生成的字幕 (SRT) 將出現在：  
   Google Drive -> Whisper -> result

### Colab 連結

- **全球版本 (英文版)**
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blusewill/ytvideo-whisper/blob/master/ytvideo_whisper.ipynb)

- **機器狼特別版 (繁體中文版)**  
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blusewill/ytvideo-whisper/blob/master/ytvideo_whisper_KMN_BOT_Version.ipynb)


## 安裝方式

### 需求條件

- 在您的系統上安裝 [Python](https://www.python.org/)。  

### 自動安裝（Linux）

1. 執行設定腳本以建立虛擬環境並安裝必要套件：  
   ```bash
   ./setup-requirement.sh
   ```
2. 執行主腳本：  
   ```bash
   ./run-script.sh
   ```

### 手動安裝

1. 建立 Python 虛擬環境：  
   ```bash
   python3 -m venv ./.virtualenv
   ```
2. 啟動虛擬環境：  
   - **Bash/Zsh**：  
     ```bash
     source ./.virtualenv/bin/activate
     ```
   - **Csh/Tcsh**：  
     ```bash
     source ./.virtualenv/bin/activate.csh
     ```
   - **Fish**：  
     ```bash
     source ./.virtualenv/bin/activate.fish
     ```
   - **Powershell**：  
     - 允許執行腳本：  
       ```powershell
       Set-ExecutionPolicy -ExecutionPolicy Bypass
       ```
     - 啟動虛擬環境：  
       ```powershell
       ./.virtualenv/bin/Activate.ps1
       ```


## 待辦清單

- [ ] 增加 Windows GPU 支援。  
- [x] 實作更快的 API。  
- [x] 支援自訂模型。  
- [ ] 增加安裝腳本。  


## 貢獻者名單

- [blusewill](https://blusewill.us.to) – 創作者，負責本地環境測試。  
- [機器狼](https://www.plurk.com/KMN_BOT) – Google Colab 測試者。  
- [刺蝟瑞歐的小行星](https://www.youtube.com/@RiccioReo) – 測試影片提供者。  


歡迎大家一起貢獻，讓這個專案變得更棒！🎉  