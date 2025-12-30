<div align="center">
  <div>&nbsp;</div>
  <img src="logo.png" width="300"/> <br>
  <a href="https://trendshift.io/repositories/8133" target="_blank"><img src="https://trendshift.io/api/badge/repositories/8133" alt="myshell-ai%2FMeloTTS | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
  
  <h2>🎵 High-Quality Multi-Lingual Text-to-Speech</h2>
  <p><strong>Fast, Open-Source, and Production-Ready</strong></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
</div>

---

## 🌟 Why MeloTTS?

MeloTTS is a **high-quality multi-lingual** text-to-speech library by [MIT](https://www.mit.edu/) and [MyShell.ai](https://myshell.ai), designed for production use with cutting-edge features:

✨ **10 Language Variants** - English (5 accents), Spanish, French, Chinese, Japanese, Korean  
⚡ **Real-Time on CPU** - Fast enough for production without GPU  
🎯 **OpenAI API Compatible** - Drop-in replacement for OpenAI TTS API  
🚀 **Optional Audio Upsampling** - Ultra-fast 24kHz→48kHz with FlashSR (200-400x realtime)  
🌐 **Interactive Web UI** - Test and demo instantly  
🔧 **Smart Text Processing** - Auto-normalize URLs, numbers, symbols, and more  
📦 **Multiple Formats** - Opus, MP3, and WAV output

## 🗣️ Supported Languages

| Language | Accents/Variants | Example Audio |
| --- | --- | --- |
| **English** | American, British, Indian, Australian, Default | [🔊 Listen](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-US/speed_1.0/sent_000.wav) |
| **Spanish** | ES | [🔊 Listen](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/es/ES/speed_1.0/sent_000.wav) |
| **French** | FR | [🔊 Listen](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/fr/FR/speed_1.0/sent_000.wav) |
| **Chinese** | ZH (Mixed Chinese & English) | [🔊 Listen](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/zh/ZH/speed_1.0/sent_008.wav) |
| **Japanese** | JP | [🔊 Listen](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/jp/JP/speed_1.0/sent_000.wav) |
| **Korean** | KR | [🔊 Listen](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/kr/KR/speed_1.0/sent_000.wav) |

> 💡 **Note:** Spanish model uses [myshell-ai/MeloTTS-Spanish](https://huggingface.co/myshell-ai/MeloTTS-Spanish) from HuggingFace

---

## ⚡ Quick Start

### 🚀 Get Started in 3 Steps

1. **Clone and Install**:
   ```bash
   git clone https://github.com/groxaxo/MeloTTS.git
   cd MeloTTS
   pip install -r requirements.txt
   python -m unidic download  # Required for Japanese support
   ```

2. **Start the Server**:
   ```bash
   python -m melo.fastapi_server
   # Server starts at http://0.0.0.0:8000
   ```

3. **Try It Out**:
   - **Web UI**: Open `http://127.0.0.1:8000` in your browser
   - **API Docs**: Visit `http://127.0.0.1:8000/docs` for interactive API documentation

### ⚙️ Configuration Options

Control server behavior with command-line flags or environment variables:

```bash
# Start with custom settings
python start_server.py --port 8000 --device cuda --disable-flashsr

# Or use environment variables
export MODEL_DEVICE=cuda              # Device: auto, cpu, cuda, mps
export ENABLE_FLASHSR=true           # Enable/disable audio upsampling globally
python -m melo.fastapi_server
```

> **💡 Tip:** FlashSR upsampling can also be controlled per-request via the API (see below)

---

## 📖 API Documentation

### OpenAI-Compatible TTS Endpoint

**Endpoint**: `POST /v1/audio/speech`

Generates audio from text with optional FlashSR upsampling (24kHz → 48kHz).

**Example with Spanish**:
```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hola, bienvenido a MeloTTS. Esta es una prueba de voz en español.",
    "voice": "ES",
    "response_format": "mp3",
    "enable_upsampling": true
  }' \
  --output speech_es.mp3
```

**Example with Upsampling Control**:
```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello, this is MeloTTS!",
    "voice": "EN-Default",
    "response_format": "opus",
    "enable_upsampling": false
  }' \
  --output speech.opus
```

**Example using Python**:
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/v1/audio/speech",
    json={
        "model": "tts-1",
        "input": "The field of text-to-speech has seen rapid development recently.",
        "voice": "EN-US",
        "response_format": "mp3",
        "speed": 1.0,
        "enable_upsampling": True  # Optional: control upsampling per request
    }
)

with open("output.mp3", "wb") as f:
    f.write(response.content)
```

**Request Parameters**:

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `model` | `string` | Model identifier (e.g., `tts-1`). Required for compatibility. |
| `input` | `string` | The text to generate audio for (automatically normalized). |
| `voice` | `string` | Voice/speaker ID (see available voices below). |
| `response_format` | `string` | Output format: `opus` (default), `mp3`, or `wav`. |
| `speed` | `float` | Speech speed (0.5 to 2.0). Default: 1.0 |
| `enable_upsampling` | `boolean` | **Optional**: Enable/disable FlashSR upsampling for this request. If not specified, uses server default. |

### List Available Voices

**Endpoint**: `GET /v1/audio/voices`

Returns a list of all available voices across all languages.

**Example**:
```bash
curl http://127.0.0.1:8000/v1/audio/voices
```

**Response**:
```json
{
  "voices": [
    {
      "id": "EN-Default",
      "name": "EN-Default",
      "object": "voice",
      "category": "melo_en",
      "language": "EN"
    },
    {
      "id": "EN-US",
      "name": "EN-US",
      "object": "voice",
      "category": "melo_en",
      "language": "EN"
    },
    ...
  ]
}
```

### Available Voices

**English (EN)**:
- EN-Default
- EN-US (American)
- EN-BR (British)
- EN_INDIA (Indian)
- EN-AU (Australian)

**Other Languages**:
- ES (Spanish) - [Model on HuggingFace](https://huggingface.co/myshell-ai/MeloTTS-Spanish)
- FR (French)
- ZH (Chinese - supports mixed Chinese and English)
- JP (Japanese)
- KR (Korean)

---

## 🎯 Key Features

### 🎚️ Optional Audio Upsampling (FlashSR)

FlashSR upsampling is **flexible and configurable**:

**Control Options**:
1. **Global Setting** (via environment variable):
   ```bash
   export ENABLE_FLASHSR=true  # Default
   python -m melo.fastapi_server
   ```

2. **Per-Request Control** (via API parameter):
   ```json
   {
     "input": "Your text here",
     "voice": "EN-US",
     "enable_upsampling": true  // Override global setting
   }
   ```

3. **Web UI Toggle**: Enable/disable with checkbox in the web interface

**Benefits**:
- ✅ Higher quality 48kHz audio output
- ✅ Minimal performance impact (200-400x realtime)
- ✅ Better compatibility with modern audio formats (especially Opus)
- ✅ Optional - use when you need it!

### 🔤 Smart Text Processing

Text is **automatically normalized** before TTS processing for natural-sounding speech:

| Input | Normalized Output |
|-------|------------------|
| `https://example.com` | "https example dot com" |
| `user@email.com` | "user at email dot com" |
| `$50.25` | "fifty dollars and twenty-five cents" |
| `123` | "one hundred twenty-three" |
| `5km` | "five kilometers" |
| `3:45 PM` | "three forty-five PM" |
| Phone numbers | Spoken digit by digit |
| Symbols & punctuation | Spoken equivalents |

### 🎨 Interactive Web Interface

Access the modern web UI at `http://127.0.0.1:8000`:

- 📝 Text input with real-time editing
- 🎤 Voice/speaker selection across all languages
- ⚡ Speed control (0.5x - 2.0x)
- 🎵 Audio upsampling toggle (FlashSR)
- 📦 Format selection (Opus, MP3, WAV)
- ▶️ Instant audio playback
- ⬇️ One-click download

---

## 🔧 Alternative Usage Methods

### Traditional CLI
- [Use without Installation](docs/quick_use.md)
- [Install and Use Locally](docs/install.md)
- [Training on Custom Dataset](docs/training.md)

The Python API and model cards can be found in [this repo](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md#python-api) or on [HuggingFace](https://huggingface.co/myshell-ai).

### Web UI (Gradio)

Run the original Gradio-based web UI:
```bash
melo-ui
```

---

## 💻 Python API Usage

```python
from melo.api import TTS
from melo.text_processing import normalize_text
from melo.flashsr_upsampler import FlashSRUpsampler

# Initialize model
model = TTS(language='EN', device='auto')
speaker_ids = model.hps.data.spk2id

# Normalize text (optional but recommended)
text = normalize_text("Visit https://example.com for more info!")

# Generate audio
audio = model.tts_to_file(
    text, 
    speaker_ids['EN-US'], 
    output_path='output.wav',
    speed=1.0
)

# Optional: Apply FlashSR upsampling
upsampler = FlashSRUpsampler(device='auto', enable=True)
upsampler.load()
upsampled_audio = upsampler.upsample(audio, sample_rate=44100)
```

---

## 🐳 Docker Support

Build and run with Docker:

```bash
docker build -t melotts .
docker run -p 8000:8000 melotts
```

---

## 🤝 Contributing

If you find this work useful, please consider contributing to this repo.

**Special Thanks**:
- [@fakerybakery](https://github.com/fakerybakery) for adding the Web UI and CLI part
- [vibevoice-realtimeFASTAPI](https://github.com/groxaxo/vibevoice-realtimeFASTAPI) for FlashSR upsampling and text processing inspiration

---

## 👥 Authors

**Original MeloTTS**:
- [Wenliang Zhao](https://wl-zhao.github.io) at Tsinghua University
- [Xumin Yu](https://yuxumin.github.io) at Tsinghua University
- [Zengyi Qin](https://www.qinzy.tech) (project lead) at MIT and MyShell

**Enhanced Features**:
- FastAPI server with OpenAI-compatible endpoints
- FlashSR audio upsampling integration
- Advanced text processing and normalization

---

## 📄 Citation

```bibtex
@software{zhao2024melo,
  author={Zhao, Wenliang and Yu, Xumin and Qin, Zengyi},
  title = {MeloTTS: High-quality Multi-lingual Multi-accent Text-to-Speech},
  url = {https://github.com/myshell-ai/MeloTTS},
  year = {2023}
}
```

---

## 📜 License

This library is under MIT License, which means it is free for both commercial and non-commercial use.

---

## 🙏 Acknowledgements

This implementation is based on [TTS](https://github.com/coqui-ai/TTS), [VITS](https://github.com/jaywalnut310/vits), [VITS2](https://github.com/daniilrobnikov/vits2) and [Bert-VITS2](https://github.com/fishaudio/Bert-VITS2). We appreciate their awesome work.

Additional features inspired by:
- [vibevoice-realtimeFASTAPI](https://github.com/groxaxo/vibevoice-realtimeFASTAPI) - FlashSR upsampling and API design
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) - Text processing and normalization logic

---

<div align="center">
  <p><strong>⭐ Star this repo if you find it useful!</strong></p>
  <p>Made with ❤️ by the MeloTTS community</p>
</div>
