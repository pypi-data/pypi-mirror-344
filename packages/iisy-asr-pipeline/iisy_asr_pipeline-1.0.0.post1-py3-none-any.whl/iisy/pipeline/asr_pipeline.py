#!/usr/bin/env python3
import argparse
import logging
import threading
from typing import Dict, Any, Tuple

import numpy as np
import pyaudio
import torch
import torchaudio
#import whisper
from faster_whisper import WhisperModel
from colorama import init
from df.enhance import init_df
from speechbrain.pretrained import EncoderClassifier
from rich.console import Console

from iisy.context_window import ContextWindow
from iisy.pipeline.audio import Audio
from iisy.pipeline.speech_enhancement_step import SpeechEnhancementStep
from iisy.pipeline.speech_transcription_step import SpeechTranscriptionStep
from iisy.pipeline.speaker_identification_step import SpeakerIdentificationStep
from iisy.transcription_display import TranscriptionDisplay

init()

class AsrPipeline:
    def __init__(self,
                input_sr: int = 16000,
                device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
                enhancement_step: SpeechEnhancementStep = None, 
                transcription_step: SpeechTranscriptionStep = None, 
                identification_step: SpeakerIdentificationStep = None,
                min_silence_duration: float = 2.0,
                verbose: bool = False,
                **kwargs
                ):
        self._init_logger(verbose)
        
        if enhancement_step is None:
            self.enhancement_step = self._get_default_enhancement_step(device, input_sr, **kwargs)
        else:
            self.enhancement_step = enhancement_step
        if transcription_step is None:
            self.transcription_step = self._get_default_transcription_step(device, **kwargs)
        else:
            self.transcription_step = transcription_step
        if identification_step is None:
            self.identification_step = self._get_default_identification_step(device, **kwargs)
        else:
            self.identification_step = identification_step
        
        self.console = Console()
        self.display = TranscriptionDisplay()
        
        self.audio_chunk_array = bytearray(100 * 100 * 1024) #100MB buffer
        self.amt_buffered_bytes = 0
        self.amt_buffered_chunks = 0
        
        self.input_sr = input_sr
        self.min_silence_duration = min_silence_duration
        self.device = device
        
        self.current_transcription = ""
        
    def reset(self):
        #self.audio_chunk_array.clear()
        self.amt_buffered_bytes = 0
        self.amt_buffered_chunks = 0
        
    def _init_logger(self, verbose: bool) -> None:
        """Initialize the logger."""
        self.logger = logging.getLogger(__name__)
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
        
    def _get_default_enhancement_step(self, device: torch.device, input_sr: int, **kwargs) -> SpeechEnhancementStep:
        """Create and return a default speech enhancement step."""
        self.logger.info("Creating default speech enhancement step.")
        
        # Load deep filter model
        deep_filter_model, df_state, _ = init_df()
        deep_filter_model.to(device)

        speech_enhancement_step = SpeechEnhancementStep(
            input_sr=input_sr,
            output_sr=48000, #The output sample rate of the deep filter model
            deep_filter_model=deep_filter_model,
            df_state=df_state
        )
        
        return speech_enhancement_step
    
    def _get_default_transcription_params(self, device: torch.device, **kwargs) -> Dict[str, Any]:
        defaults = {
            "model_size": "medium",
            "device_index": 0,
            "compute_type": "float16" if device == torch.device("cuda") else "int8_float16",
            "loglevel": logging.ERROR,
        }
        
        if kwargs == None:
            return defaults
        
        #check if kwargs contain a 'whisper' key
        if "whisper" in kwargs:
            defaults.update(kwargs["whisper"])
            
        return defaults
    
    def _get_default_transcription_step(self, device: torch.device, **kwargs) -> SpeechTranscriptionStep:
        """Create and return a default speech transcription step."""
        #get transcription params from kwargs
        defaults = self._get_default_transcription_params(device, **kwargs)
        
        whisper_model = WhisperModel(
            defaults["model_size"],
            device=device,
            device_index=defaults["device_index"],
            compute_type=defaults["compute_type"],
        )
        whisper_model.logger.setLevel(defaults["loglevel"])
        
        transcription_step = SpeechTranscriptionStep(
            input_sr=48000,
            output_sr=16000,
            whisper_model=whisper_model
        )
        
        return transcription_step
    
    def _get_default_identification_params(self, **kwargs) -> Dict[str, Any]:
        defaults = {
            "speaker_model": "speechbrain/spkrec-resnet-voxceleb",
            "savedir": "pretrained_models/spkrec-resnet-voxceleb",
            "speaker_threshold": 0.55,
        }
        
        if kwargs == None:
            return defaults
        
        #check if kwargs contain a 'speaker' key
        if "speaker" in kwargs:
            defaults.update(kwargs["speaker"])
            
        return defaults
    
    def _get_default_identification_step(self, device: torch.device, **kwargs) -> SpeakerIdentificationStep:
        """Create and return a default speaker identification step."""
        # Load speaker identification model
        run_opts = {
            "device": device
        }
        defaults = self._get_default_identification_params(**kwargs)
        
        speaker_identification_model = EncoderClassifier.from_hparams(
            source=defaults["speaker_model"],
            savedir=defaults["savedir"],
            run_opts=run_opts,
        )
        
        speaker_identification_step = SpeakerIdentificationStep(
            input_sr=48000,
            output_sr=16000,
            model=speaker_identification_model,
            threshold=defaults["speaker_threshold"],
        )
        
        return speaker_identification_step

    def step(self, audio_buffer: ContextWindow, current_transcription: str, quiet: bool = False) -> Tuple[int, str, bool]:
        """
        Process a single step of the pipeline.
        Returns the speaker ID and the current transcription as well as a boolean depiciting if the sentence is finished.
        """
        
        if audio_buffer.is_empty():
            return (-1, "", False)
        
        self.amt_buffered_chunks += audio_buffer.amt_chunks()
                
        #audio_chunk += audio_buffer.consume()
        self.amt_buffered_bytes += audio_buffer.consume_into(self.audio_chunk_array, self.amt_buffered_bytes)
        audio_chunk = bytes(self.audio_chunk_array[:self.amt_buffered_bytes])

        audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
        audio = Audio.from_numpy(audio_array, self.input_sr)

        audio = self.enhancement_step.process(audio)
        # Get the energy of the audio chunk
        energy = torch.mean(torch.abs(audio.data)).item()
        if energy < 1.5 and self.amt_buffered_chunks > 50:
            self.amt_buffered_bytes = 0
            self.amt_buffered_chunks = 0
            if not quiet:
                self.display.display_in_progress(
                    "...",
                    "(0)",
                    self.amt_buffered_chunks
                )
            self.logger.debug("Audio chunk is silent, skipping.")
            return (-1, "", False)
        
        out, checkOutput, end_silence_duration = self.transcription_step.process(audio)

        if checkOutput:
            current_transcription = out
            if not quiet:
                self.display.display_in_progress(
                    out,
                    "(0)",
                    self.amt_buffered_chunks,
                )
        else:
            if not quiet:
                self.display.display_in_progress(
                    "...",
                    "(0)",
                    self.amt_buffered_chunks
                )

        # Check if the audio chunk contains enough silence and low energy at the end
        # to consider it as a sentence boundary.
        # or if the audio chunk is too long, since a very long audio chunks stall the pipeline
        if end_silence_duration > self.min_silence_duration or self.amt_buffered_chunks > 400:
            if current_transcription:
                audio_array = np.frombuffer(
                    audio_chunk, dtype=np.int16)
                audio = Audio.from_numpy(audio_array, self.input_sr)
                speaker_id = self.identification_step.process(audio)

                # Print the full sentence
                if not quiet:
                    self.display.display_complete(
                        current_transcription,
                        speaker_id,
                        self.amt_buffered_chunks
                    )

                # Clear the buffer
                self.amt_buffered_chunks = 0
                #audio_chunk = b""
                self.amt_buffered_bytes = 0
                
                return speaker_id, current_transcription, True
            else:
                return (-1, "", False)
            
        return (-1, current_transcription if current_transcription else "", False)
                
        
    def run(self, audio_buffer: ContextWindow) -> None:
        self.console.print("[bold green]Starting pipeline...[/bold green]")
        sentences = []
        current_transcription = ""
        
        try:
            while True:
                speaker_id, current_transcription, finished = self.step(audio_buffer, current_transcription)
                
                if finished:
                    sentences.append((speaker_id, current_transcription))
                
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Pipeline Stopped.[/bold red]")
            self.console.print("[bold green]Final sentences:[/bold green]")
            for speaker_id, sentence in sentences:
                self.console.print(f"Speaker {speaker_id}: {sentence}")
        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
            raise e
        finally:
            pass
        