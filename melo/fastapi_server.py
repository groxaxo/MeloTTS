"""
FastAPI server with OpenAI-compatible API endpoints for MeloTTS.
Includes FlashSR audio upsampling and text processing from vibevoice.
"""

import io
import os
import numpy as np
import scipy.io.wavfile
from typing import Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydub import AudioSegment

from .api import TTS
from .text_processing import normalize_text, split_text_into_sentences
from .flashsr_upsampler import FlashSRUpsampler

app = FastAPI(title="MeloTTS API", description="OpenAI-compatible TTS API with MeloTTS")

# Global state
tts_models = {}
flashsr_upsampler = None
SAMPLE_RATE = 44100  # MeloTTS native sample rate
UPSAMPLED_RATE = 48000


class OpenAISpeechRequest(BaseModel):
    """OpenAI TTS API compatible request model"""
    model: str = "tts-1"
    input: str
    voice: Optional[str] = "EN-Default"
    response_format: Optional[str] = "opus"  # opus, mp3, wav
    speed: Optional[float] = 1.0


@app.on_event("startup")
async def startup_event():
    """Initialize TTS models and FlashSR upsampler on startup"""
    global tts_models, flashsr_upsampler
    
    device = os.environ.get("MODEL_DEVICE", "auto")
    
    # Load TTS models for all supported languages
    print("[Startup] Loading MeloTTS models...")
    for language in ['EN', 'ES', 'FR', 'ZH', 'JP', 'KR']:
        try:
            tts_models[language] = TTS(language=language, device=device)
            print(f"[Startup] Loaded {language} model")
        except Exception as e:
            print(f"[Startup] Warning: Failed to load {language} model: {e}")
    
    # Initialize FlashSR upsampler
    enable_flashsr_str = os.environ.get("ENABLE_FLASHSR", "true").lower()
    enable_flashsr = enable_flashsr_str in ("true", "1", "yes", "on")
    
    if enable_flashsr:
        print("[Startup] Initializing FlashSR upsampler...")
        flashsr_upsampler = FlashSRUpsampler(device=device, enable=True)
        flashsr_upsampler.load()
    else:
        print("[Startup] FlashSR disabled")
        flashsr_upsampler = FlashSRUpsampler(device=device, enable=False)
    
    print("[Startup] Server ready!")


@app.post("/v1/audio/speech")
async def create_speech(request: OpenAISpeechRequest):
    """
    OpenAI-compatible TTS endpoint.
    Generates audio from text with optional FlashSR upsampling.
    """
    try:
        # Normalize and sanitize text
        normalized_text = normalize_text(request.input)
        
        if not normalized_text.strip():
            raise HTTPException(status_code=400, detail="Input text is empty after normalization")
        
        # Determine language and speaker from voice parameter
        voice = request.voice or "EN-Default"
        
        # Extract language from voice (e.g., "EN-Default" -> "EN")
        language = voice.split('-')[0].upper() if '-' in voice else 'EN'
        
        # Fallback to EN if language not supported
        if language not in tts_models:
            language = 'EN'
        
        model = tts_models[language]
        speaker_ids = model.hps.data.spk2id
        
        # Determine speaker ID
        if voice in speaker_ids:
            speaker_id = speaker_ids[voice]
        else:
            # Use first available speaker for the language
            speaker_id = speaker_ids[list(speaker_ids.keys())[0]]
        
        # Generate audio
        audio = model.tts_to_file(
            normalized_text,
            speaker_id,
            output_path=None,
            speed=request.speed or 1.0,
            quiet=True
        )
        
        if audio is None or len(audio) == 0:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Apply FlashSR upsampling if enabled
        output_sample_rate = SAMPLE_RATE
        if flashsr_upsampler and flashsr_upsampler.enabled:
            audio = flashsr_upsampler.upsample(audio, sample_rate=SAMPLE_RATE)
            output_sample_rate = UPSAMPLED_RATE
        
        # Convert to WAV first
        buffer = io.BytesIO()
        scipy.io.wavfile.write(buffer, output_sample_rate, audio)
        wav_data = buffer.getvalue()
        
        # Convert to requested format
        response_format = request.response_format or "opus"
        
        if response_format == "mp3":
            buffer.seek(0)
            audio_segment = AudioSegment.from_wav(buffer)
            mp3_buffer = io.BytesIO()
            audio_segment.export(mp3_buffer, format="mp3")
            return Response(content=mp3_buffer.getvalue(), media_type="audio/mpeg")
        
        elif response_format == "opus":
            try:
                buffer.seek(0)
                audio_segment = AudioSegment.from_wav(buffer)
                opus_buffer = io.BytesIO()
                audio_segment.export(
                    opus_buffer, 
                    format="opus", 
                    codec="libopus",
                    parameters=["-ar", str(output_sample_rate)]
                )
                return Response(content=opus_buffer.getvalue(), media_type="audio/opus")
            except Exception as e:
                # Fallback to WAV if opus encoding fails
                print(f"[Warning] Opus encoding failed: {e}. Falling back to WAV format.")
                return Response(content=wav_data, media_type="audio/wav")
        
        else:  # wav or default
            return Response(content=wav_data, media_type="audio/wav")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Error] Speech generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/audio/voices")
def get_voices():
    """
    Get list of available voices.
    Returns all speaker IDs from all loaded language models.
    """
    voices = []
    
    for language, model in tts_models.items():
        speaker_ids = model.hps.data.spk2id
        for voice_id in sorted(speaker_ids.keys()):
            voices.append({
                "id": voice_id,
                "name": voice_id,
                "object": "voice",
                "category": f"melo_{language.lower()}",
                "language": language
            })
    
    return {"voices": voices}


@app.get("/")
def index():
    """Serve the web UI"""
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return {"message": "MeloTTS API Server", "docs": "/docs"}


@app.get("/config")
def get_config():
    """Get server configuration for web UI"""
    voices = []
    default_voice = None
    
    for language, model in tts_models.items():
        speaker_ids = model.hps.data.spk2id
        for voice_id in sorted(speaker_ids.keys()):
            voices.append(voice_id)
            if default_voice is None:
                default_voice = voice_id
    
    return {
        "voices": voices,
        "default_voice": default_voice,
        "flashsr_enabled": flashsr_upsampler.enabled if flashsr_upsampler else False,
        "sample_rate": UPSAMPLED_RATE if (flashsr_upsampler and flashsr_upsampler.enabled) else SAMPLE_RATE
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
