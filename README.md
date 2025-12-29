<div align="center">
  <div>&nbsp;</div>
  <img src="logo.png" width="300"/> <br>
  <a href="https://trendshift.io/repositories/8133" target="_blank"><img src="https://trendshift.io/api/badge/repositories/8133" alt="myshell-ai%2FMeloTTS | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>

## Introduction
MeloTTS is a **high-quality multi-lingual** text-to-speech library by [MIT](https://www.mit.edu/) and [MyShell.ai](https://myshell.ai).

### 🚀 New Features

- **OpenAI-Compatible API**: Drop-in replacement for OpenAI's TTS API with FastAPI server
- **FlashSR Audio Upsampling**: Ultra-fast upsampling from 24kHz → 48kHz at 200-400x realtime
- **Advanced Text Processing**: Automatic normalization of URLs, numbers, symbols, and more
- **Interactive Web UI**: Built-in web interface for easy testing and demo
- **Multiple Audio Formats**: Support for Opus, MP3, and WAV output formats

### Supported Languages

MeloTTS supports the following languages:

| Language | Example |
| --- | --- |
| English (American)    | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-US/speed_1.0/sent_000.wav) |
| English (British)     | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-BR/speed_1.0/sent_000.wav) |
| English (Indian)      | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN_INDIA/speed_1.0/sent_000.wav) |
| English (Australian)  | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-AU/speed_1.0/sent_000.wav) |
| English (Default)     | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-Default/speed_1.0/sent_000.wav) |
| Spanish               | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/es/ES/speed_1.0/sent_000.wav) |
| French                | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/fr/FR/speed_1.0/sent_000.wav) |
| Chinese (mix EN)      | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/zh/ZH/speed_1.0/sent_008.wav) |
| Japanese              | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/jp/JP/speed_1.0/sent_000.wav) |
| Korean                | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/kr/KR/speed_1.0/sent_000.wav) |

Some other features include:
- The Chinese speaker supports `mixed Chinese and English`.
- Fast enough for `CPU real-time inference`.

## ⚡ Quick Start with FastAPI Server

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/groxaxo/MeloTTS.git
   cd MeloTTS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m unidic download
   ```

3. **Run the FastAPI server**:
   ```bash
   python -m melo.fastapi_server
   ```

   The server will start at `http://0.0.0.0:8000`

4. **Access the Web UI**:
   Open your browser and navigate to `http://127.0.0.1:8000`

### Environment Variables

- `MODEL_DEVICE`: Device to use (`auto`, `cuda`, `mps`, or `cpu`). Default: `auto`
- `ENABLE_FLASHSR`: Enable FlashSR audio upsampling (`true` or `false`). Default: `true`

Example:
```bash
export ENABLE_FLASHSR=true
export MODEL_DEVICE=cuda
python -m melo.fastapi_server
```

## 📖 API Documentation

### OpenAI-Compatible TTS Endpoint

**Endpoint**: `POST /v1/audio/speech`

Generates audio from text with optional FlashSR upsampling (24kHz → 48kHz).

**Example using cURL**:
```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello, this is MeloTTS with FlashSR upsampling!",
    "voice": "EN-Default",
    "response_format": "opus"
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
        "speed": 1.0
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
- ES (Spanish)
- FR (French)
- ZH (Chinese - supports mixed Chinese and English)
- JP (Japanese)
- KR (Korean)

## 🎯 Features

### FlashSR Audio Super-Resolution

FlashSR is **enabled by default** to upsample audio from the native sample rate to 48kHz at ultra-fast speeds (200-400x realtime). This provides:

- Higher quality 48kHz audio output
- Minimal performance impact
- Better compatibility with modern audio formats (especially Opus)

To disable FlashSR:
```bash
export ENABLE_FLASHSR=false
python -m melo.fastapi_server
```

### Advanced Text Processing

Text is automatically normalized before TTS processing, including:

- **URLs and Emails**: Converted to speakable format
- **Numbers**: "123" → "one hundred twenty-three"
- **Money**: "$50.25" → "fifty dollars and twenty-five cents"
- **Units**: "5km" → "five kilometers"
- **Phone Numbers**: Spoken digit by digit
- **Time**: "3:45 PM" → "three forty-five PM"
- **Symbols**: Replaced with spoken equivalents
- **CJK Punctuation**: Normalized for better pronunciation

### Web Interface

The built-in web UI provides:
- Easy text-to-speech generation
- Voice selection dropdown
- Speed control
- Output format selection
- Audio playback and download
- Real-time status updates

## 🔧 Command Line Usage
- [Use without Installation](docs/quick_use.md)
- [Install and Use Locally](docs/install.md)
- [Training on Custom Dataset](docs/training.md)

## 🔧 Command Line Usage

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

## 🐳 Docker Support

Build and run with Docker:

```bash
docker build -t melotts .
docker run -p 8000:8000 melotts
```

## 🤝 Contributing

## 🤝 Contributing

If you find this work useful, please consider contributing to this repo.

- Many thanks to [@fakerybakery](https://github.com/fakerybakery) for adding the Web UI and CLI part.
- Thanks to the [vibevoice-realtimeFASTAPI](https://github.com/groxaxo/vibevoice-realtimeFASTAPI) project for inspiration on FlashSR upsampling and text processing.

## 👥 Authors

## 👥 Authors

**Original MeloTTS**:
- [Wenliang Zhao](https://wl-zhao.github.io) at Tsinghua University
- [Xumin Yu](https://yuxumin.github.io) at Tsinghua University
- [Zengyi Qin](https://www.qinzy.tech) (project lead) at MIT and MyShell

**Enhanced Features**:
- FastAPI server with OpenAI-compatible endpoints
- FlashSR audio upsampling integration
- Advanced text processing and normalization

## 📄 Citation
## 📄 Citation

```bibtex
@software{zhao2024melo,
  author={Zhao, Wenliang and Yu, Xumin and Qin, Zengyi},
  title = {MeloTTS: High-quality Multi-lingual Multi-accent Text-to-Speech},
  url = {https://github.com/myshell-ai/MeloTTS},
  year = {2023}
}
```

## 📜 License

## 📜 License

This library is under MIT License, which means it is free for both commercial and non-commercial use.

## 🙏 Acknowledgements

This implementation is based on [TTS](https://github.com/coqui-ai/TTS), [VITS](https://github.com/jaywalnut310/vits), [VITS2](https://github.com/daniilrobnikov/vits2) and [Bert-VITS2](https://github.com/fishaudio/Bert-VITS2). We appreciate their awesome work.

Additional features inspired by:
- [vibevoice-realtimeFASTAPI](https://github.com/groxaxo/vibevoice-realtimeFASTAPI) - FlashSR upsampling and API design
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) - Text processing and normalization logic
