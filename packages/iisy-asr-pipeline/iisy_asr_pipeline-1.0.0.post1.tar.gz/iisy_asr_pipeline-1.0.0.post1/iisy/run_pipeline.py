#!/usr/bin/env python3
import argparse
import logging
import threading
from typing import Tuple

import pyaudio
import torch

from iisy.context_window import ContextWindow

from iisy.pipeline.asr_pipeline import AsrPipeline


def list_audio_devices() -> None:
    """List all available audio devices and their properties."""
    p = pyaudio.PyAudio()

    print("\nAvailable Audio Devices:")
    print("------------------------")

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info["name"]
        max_input_channels = device_info["maxInputChannels"]
        max_output_channels = device_info["maxOutputChannels"]
        default_sample_rate = device_info["defaultSampleRate"]

        print(f"Device {i}: {device_name}")
        print(f"  Max Input Channels: {max_input_channels}")
        print(f"  Max Output Channels: {max_output_channels}")
        print(f"  Default Sample Rate: {default_sample_rate}")
        print()

    p.terminate()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for the audio processing pipeline."""
    parser = argparse.ArgumentParser(description="Audio Processing Pipeline")

    # Device settings
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu",
                        help="Device to run models on (cuda/cpu)")
    parser.add_argument("--input-device-index", type=int, default=1,
                        help="Input audio device index")
    parser.add_argument("--list-devices", action="store_true",
                        help="List all available audio devices and exit")

    # Audio parameters
    parser.add_argument("--chunk-size", type=int, default=2048,
                        help="Number of audio frames per buffer")
    parser.add_argument("--channels", type=int, default=1,
                        help="Number of audio channels (1=mono, 2=stereo)")
    parser.add_argument("--buffer-size", type=int, default=1000,
                        help="Size of the audio buffer")

    # Model parameters
    parser.add_argument("--whisper-model", type=str, default="medium",
                        help="Whisper model size (tiny, base, small, medium, large, turbo)")
    
    # SpeechBrain models
    parser.add_argument("--speaker-model", type=str,
                        default="speechbrain/spkrec-resnet-voxceleb",
                        help="Speaker identification model path (speechbrain/spkrec-resnet-voxceleb or speechbrain/spkrec-ecapa-voxceleb)")

    # Silence detection parameters
    parser.add_argument("--silence-threshold", type=float, default=0.01,
                        help="Energy threshold for silence detection")
    parser.add_argument("--min-silence-duration", type=float, default=2.0,
                        help="Minimum duration of silence for sentence boundary (seconds)")

    # Other parameters
    parser.add_argument("--speaker-threshold", type=float, default=0.55,
                        help="Threshold for speaker identification")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose logging")

    return parser.parse_args()


def get_sample_rate(p: pyaudio.PyAudio, device_index: int) -> int:
    """Get the sample rate of an audio device.

    Args:
        p: PyAudio instance
        device_index: Index of the audio device

    Returns:
        Sample rate of the device
    """
    device_info = p.get_device_info_by_index(device_index)
    return int(device_info["defaultSampleRate"])


def initialize_audio(input_device_index: int, chunk_size: int,
                     channels: int) -> Tuple[pyaudio.PyAudio, pyaudio.Stream, int]:
    """Initialize PyAudio and open the input stream.

    Args:
        input_device_index: Index of the input audio device
        chunk_size: Number of audio frames per buffer
        channels: Number of audio channels

    Returns:
        pyaudio.PyAudio: PyAudio object
        pyaudio.Stream: Input audio stream
        int: Sample rate of the input device
    """
    p = pyaudio.PyAudio()

    input_device_sr = get_sample_rate(p, input_device_index)

    # Open input stream (microphone)
    in_stream = p.open(
        format=pyaudio.paInt16,  # 16-bit resolution
        channels=channels,
        rate=input_device_sr,
        input=True,
        input_device_index=input_device_index,
        frames_per_buffer=chunk_size
    )

    return p, in_stream, input_device_sr


def setup_audio_capture(in_stream: pyaudio.Stream, audio_buffer: ContextWindow, chunk_size: int) -> threading.Thread:
    """Set up and start the audio capturing thread.

    Args:
        in_stream: Input audio stream
        audio_buffer: Buffer to store audio data
        chunk_size: Number of audio frames per buffer

    Returns:
        threading.Thread: Audio capture thread
    """
    def audio_capture():
        while True:
            try:
                # Read audio from the input stream
                audio_data = in_stream.read(
                    chunk_size, exception_on_overflow=False)
                audio_buffer.add(audio_data)
            except Exception as e:
                logging.error(f"Audio capture error: {e}")
                break

    # Start the audio capturing thread
    capture_thread = threading.Thread(target=audio_capture, daemon=True)
    capture_thread.start()

    return capture_thread


def run_pipeline():
    """Main entry point for the audio processing pipeline."""
    # Parse command line arguments
    args = parse_arguments()

    # List devices if requested
    if args.list_devices:
        list_audio_devices()
        return

    # Convert arguments to a dictionary for easier access
    config = vars(args)

    # Initialize audio
    p, in_stream, input_device_sr = initialize_audio(
        config["input_device_index"],
        config["chunk_size"],
        config["channels"]
    )

    # Create audio buffer
    audio_buffer = ContextWindow(config["buffer_size"])
    
    pipeline_config = {
        'speaker': {
            'model': config["speaker_model"],
            'savedir': config["speaker_model"].split("/")[-1],
            'speaker_threshold': config["speaker_threshold"]
        },
        'whisper': {
            "model_size": config["whisper_model"],
            "device_index": 0,
            "loglevel": logging.ERROR,
        }
    }

    # create the pipeline
    pipeline = AsrPipeline(
        input_sr=input_device_sr,
        device=config["device"],
        min_silence_duration=config["min_silence_duration"],
        verbose=config["verbose"],
        **pipeline_config,
    )

    # Start audio capture thread
    _ = setup_audio_capture(
        in_stream, audio_buffer, config["chunk_size"])

    try:
        pipeline.run(audio_buffer)
    finally:
        logging.info("Stopping audio capture...")
        in_stream.stop_stream()
        in_stream.close()
        p.terminate()

if __name__ == "__main__":
    run_pipeline()
    
    
