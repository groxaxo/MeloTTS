#!/usr/bin/env python3
"""
Startup script for MeloTTS FastAPI server.
Run this to start the OpenAI-compatible TTS API server.
"""

import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Start MeloTTS FastAPI server with OpenAI-compatible API"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "cuda", "mps"],
        help="Device to use for inference (default: auto)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )
    parser.add_argument(
        "--disable-flashsr",
        action="store_true",
        help="Disable FlashSR audio upsampling",
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ["MODEL_DEVICE"] = args.device
    os.environ["ENABLE_FLASHSR"] = "false" if args.disable_flashsr else "true"
    
    print("=" * 60)
    print("🎵 MeloTTS FastAPI Server")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Device: {args.device}")
    print(f"FlashSR: {'Disabled' if args.disable_flashsr else 'Enabled'}")
    print("=" * 60)
    print(f"\n🌐 Server will be available at: http://{args.host}:{args.port}")
    print(f"📖 API Documentation: http://{args.host}:{args.port}/docs")
    print(f"🎨 Web UI: http://{args.host}:{args.port}/\n")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "melo.fastapi_server:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
