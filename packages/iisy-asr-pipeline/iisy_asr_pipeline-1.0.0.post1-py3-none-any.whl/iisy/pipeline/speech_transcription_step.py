import numpy as np
import torch
from iisy.pipeline.pipeline_step import PipelineStep
from iisy.pipeline.audio import Audio
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio

class SpeechTranscriptionStep(PipelineStep):
    def __init__(self, input_sr: int, output_sr: int, whisper_model: WhisperModel):
        super().__init__(input_sr, output_sr)
        self.whisper_model = whisper_model

    @staticmethod
    def to_mono(audio):
        if len(audio.shape) > 1:  # Check if multi-channel
            audio = np.mean(audio, axis=0)
        return audio

    @staticmethod
    def normalize_audio(audio):
        return audio / np.max(np.abs(audio))
    
    @staticmethod
    def resample_audio(audio, resampler):
        return resampler(torch.tensor(audio)).numpy()
        
    def check_output(self, output_str : str) -> bool:

        #empty output
        if output_str == "":
            return False
        
        #often different but way to long noise outputs
        if len(output_str) > 500:
            return False
        
        #remove leading and trailing whitespaces
        output_str = output_str.strip()
            
        comments = [ 
            "Vielen Dank",
            "Das war's für",
            "und wir haben",
            "Ich bin so glücklich",
            "Ich habe es geschafft",
            "und dann kommt",
            "und das ist",
            "und dann können wir",
            "Ich gebe mir",
            "Schönen guten Tag",
            "Danke für",
            "Untertitelung. BR ",
            "Untertitel im Auftrag des "
        ]
        
        # Check if output_str starts with any of the comments
        return not any(output_str.startswith(comment) for comment in comments)

        
    def process(self, audio: Audio) -> tuple[str, bool, float]:
        audio_array = audio.data.detach().cpu()
        audio_array = np.array(audio_array, dtype=np.float32)
        
        # print(f"Audio shape: {audio_array.shape}")
        # print(f"Audio dtype: {audio_array.dtype}")
        
        audio = SpeechTranscriptionStep.to_mono(audio_array)
        audio = SpeechTranscriptionStep.resample_audio(audio, self.resampler)
        audio = SpeechTranscriptionStep.normalize_audio(audio)
        
        audio_len_sec = len(audio) / self.output_sr
        if(audio_len_sec < 0.5):
            return "", False, 0.0
        
        # out = self.whisper_model.transcribe(audio, language="de")
        
        # check = self.check_output(out['text'])
        
        # return out['text'], check
        
        segments, info = self.whisper_model.transcribe(audio=audio, language="de", beam_size=5, vad_filter=True)
        if(info.duration_after_vad < 0.05):
            return "", False, audio_len_sec - info.duration_after_vad
        
        evaluated_segments = [seg for seg in segments]
        if len(evaluated_segments) == 0:
            return "", False, audio_len_sec
        
        text = "".join([seg.text for seg in evaluated_segments])
        check = self.check_output(text)
        
        end_silence_duration = audio_len_sec - evaluated_segments[-1].end
        
        return text, check, end_silence_duration