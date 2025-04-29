# Whispa App

**Audio Transcription & Translation Tool**  
Version: 2.1.0

---

## Overview

Whispa App is a desktop GUI for:

- **Transcribing** audio files to text using OpenAI’s **Whisper** models  
- **Translating** the transcribed text into multiple target languages via **MarianMT**

Built with:
- **Python 3.10+**
- **CustomTkinter** (modern Tkinter theming)
- **PyTorch** and **faster-whisper** for transcription
- **Transformers** and **MarianMT** for translation
- **psutil** for live system stats

---

## Key Features

- **Five** Whisper model sizes: `tiny`, `base`, `small`, `medium`, `large`  
- Translate into **Spanish**, **French**, **German**, **Chinese**, **Japanese**  
- **Advanced settings**: VRAM threshold, beam sizes, VAD filter, temperature, length penalty  
- **Progress bars** and real-time status updates  
- **Local caching** for offline use after initial download  

---

## System Requirements

- **OS**: Windows 10 or later  
- **Python**: 3.10 or higher (if installing via pip)  
- **CPU** only by default; GPU supported via extra install  
- **Internet**: Required only for first-run model downloads  

---

## Installation

### 📝 Option A: Windows Installer (Recommended)

1. Download `WhispaApp-2.1.0-Setup.exe`.  
2. Run the installer and follow the prompts.  
3. A console window will show **pip** and **model** download progress.  
4. Launch **Whispa App** from the Start Menu when done.

### 🐍 Option B: pip (Requires Python Installed)

```bash
# CPU-only
pip install whispa_app[cpu]

# (Optional) GPU support
pip install torch --index-url https://download.pytorch.org/whl/cu118
pip install whispa_app[gpu]


# Download all models (first time only)
whispa-prefetch

# Launch the GUI
whispa


Quick Start
Browse for an audio file (.wav, .mp3, .m4a).

Select a Whisper model size and click Transcribe.

Choose a target Language and click Translate.

(Optional) Open Advanced to tweak VRAM, beam sizes, VAD, etc.

Save results via File → Save Transcript/Save Translation.

Advanced Settings
Setting   What it does
Min GPU VRAM (GB)   Minimum VRAM before falling back to CPU inference
Transcription Beam  Beam width for Whisper (higher = more accurate, slower)
VAD Filter     Skip silent segments during transcription
Translation Beam    Beam width for MarianMT translation
Length Penalty Penalizes shorter/longer translations (⧸1 favors longer output)
Temperature    Sampling “diversity” parameter for translation
Hover any control in the app for a tooltip with details.

First-Run Model Download
On first launch, Whispa App will automatically:

Download Whisper weights for all five sizes

Download MarianMT models for each supported language

Models are cached under %USERPROFILE%\.cache\huggingface and used offline thereafter. If a download fails, you’ll see an error dialog—just reconnect and retry.

Troubleshooting
“CMake” or “SentencePiece” errors when installing via pip?
Ensure you have a prebuilt wheel:

bash
Copy code
pip install sentencepiece
Or use the Windows installer to avoid build-from-source.

GPU not detected?
Install the CUDA-enabled PyTorch wheel:

bash
Copy code
pip install torch --index-url https://download.pytorch.org/whl/cu118
Still stuck?
Open an issue on GitHub or email below.

Support & Contribution
GitHub: github.com/damoojeje/whispa_app

Email: damilareeniolabi@gmail.com

Contributions and feedback are welcome! Feel free to submit issues or PRs.