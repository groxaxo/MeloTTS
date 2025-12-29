# MeloTTS API Testing Guide

This document describes how to test the MeloTTS FastAPI server with OpenAI-compatible endpoints.

## Prerequisites

1. Install MeloTTS with all dependencies:
   ```bash
   pip install -r requirements.txt
   python -m unidic download
   ```

2. Ensure you have ffmpeg installed for audio format conversion:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   ```

## Starting the Server

### Method 1: Using the startup script
```bash
python start_server.py --port 8000 --device auto
```

### Method 2: Using uvicorn directly
```bash
python -m uvicorn melo.fastapi_server:app --host 0.0.0.0 --port 8000
```

### Method 3: Using the console script (after installation)
```bash
pip install -e .
melo-server --port 8000
```

## Testing the API

### 1. Test Health Check
Visit the interactive API docs:
- Open browser to: http://127.0.0.1:8000/docs
- Or visit the web UI: http://127.0.0.1:8000/

### 2. Test Voice Listing
```bash
curl http://127.0.0.1:8000/v1/audio/voices
```

Expected response:
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
    ...
  ]
}
```

### 3. Test Speech Generation

#### Generate Opus audio (default):
```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello, this is MeloTTS with FlashSR upsampling!",
    "voice": "EN-Default",
    "response_format": "opus"
  }' \
  --output test_output.opus
```

#### Generate MP3 audio:
```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "The field of text-to-speech has seen rapid development recently.",
    "voice": "EN-US",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output test_output.mp3
```

#### Generate WAV audio:
```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Testing advanced text processing: Visit https://example.com at 3:45 PM for $50 deals!",
    "voice": "EN-BR",
    "response_format": "wav"
  }' \
  --output test_output.wav
```

### 4. Test with Python Client

```python
import requests

# Generate speech
response = requests.post(
    "http://127.0.0.1:8000/v1/audio/speech",
    json={
        "model": "tts-1",
        "input": "This is a test of the MeloTTS API.",
        "voice": "EN-Default",
        "response_format": "mp3",
        "speed": 1.0
    }
)

# Save audio
with open("output.mp3", "wb") as f:
    f.write(response.content)

print("Audio saved to output.mp3")
```

### 5. Test Text Processing

Test various text normalizations:
```bash
# URLs
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Visit https://github.com for code.", "voice": "EN-Default"}' \
  --output url_test.mp3

# Numbers
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "There are 123 items and 45.67 percent discount.", "voice": "EN-Default"}' \
  --output numbers_test.mp3

# Money
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "The price is $50.25 per item.", "voice": "EN-Default"}' \
  --output money_test.mp3
```

### 6. Test Multi-Language Support

```bash
# Spanish
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Hola mundo. ¿Cómo estás?", "voice": "ES"}' \
  --output spanish_test.mp3

# French
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Bonjour le monde.", "voice": "FR"}' \
  --output french_test.mp3

# Japanese
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "こんにちは世界", "voice": "JP"}' \
  --output japanese_test.mp3
```

## Testing FlashSR Upsampling

### With FlashSR (default):
```bash
export ENABLE_FLASHSR=true
python start_server.py
```

Generate audio and check sample rate:
```bash
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Testing FlashSR upsampling.", "voice": "EN-Default", "response_format": "wav"}' \
  --output flashsr_test.wav

# Check sample rate (should be 48kHz)
ffprobe flashsr_test.wav 2>&1 | grep "Audio"
```

### Without FlashSR:
```bash
export ENABLE_FLASHSR=false
python start_server.py --disable-flashsr
```

Generate audio and check sample rate:
```bash
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "input": "Testing without FlashSR.", "voice": "EN-Default", "response_format": "wav"}' \
  --output no_flashsr_test.wav

# Check sample rate (should be 44.1kHz or 24kHz)
ffprobe no_flashsr_test.wav 2>&1 | grep "Audio"
```

## Web UI Testing

1. Start the server
2. Open browser to http://127.0.0.1:8000
3. Test the web interface:
   - Enter text in the text area
   - Select a voice from the dropdown
   - Adjust speed slider
   - Select output format
   - Click "Generate Speech"
   - Verify audio plays automatically
   - Test the download button

## Expected Behavior

1. **Text Processing**: 
   - URLs, numbers, symbols should be normalized
   - Example: "https://example.com" → "https example dot com"
   - Example: "$50" → "fifty dollars"

2. **FlashSR Upsampling**:
   - When enabled: Output should be 48kHz
   - When disabled: Output should be at native rate (~44.1kHz)

3. **Audio Formats**:
   - Opus: Should produce .opus file
   - MP3: Should produce .mp3 file
   - WAV: Should produce .wav file

4. **Speed Control**:
   - Values 0.5-2.0 should work
   - Lower values = slower speech
   - Higher values = faster speech

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

### Issue: "ffmpeg not found" warning
**Solution**: Install ffmpeg for audio format conversion
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Issue: Models not loading
**Solution**: The first run will download models automatically. Ensure you have internet connection and sufficient disk space.

### Issue: CUDA/GPU errors
**Solution**: Use CPU fallback
```bash
python start_server.py --device cpu
```

## Performance Notes

- First request may be slower as models are loaded
- Subsequent requests should be fast (near real-time)
- FlashSR adds minimal overhead (200-400x realtime)
- GPU acceleration significantly improves performance
