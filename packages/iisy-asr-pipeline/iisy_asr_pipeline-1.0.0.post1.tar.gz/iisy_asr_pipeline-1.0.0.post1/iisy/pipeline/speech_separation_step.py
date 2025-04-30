import torchaudio
from df.enhance import enhance
from iisy.pipeline.pipeline_step import PipelineStep
from iisy.pipeline.audio import Audio

class SpeechSeparationStep(PipelineStep):
    def __init__(self, input_sr: int, output_sr: int, separation_model):
        super().__init__(input_sr, output_sr)
        self.separation_model = separation_model
        
        
    def process(self, audio: Audio) -> list[Audio]:
        sr = self.separation_model.hparams.sample_rate
        audio = audio.resample(sr, self.resampler)
        
        est_sources = self.separation_model.separate_batch(audio.data)
        speaker1 = est_sources[:, :, 0]
        speaker2 = est_sources[:, :, 1]
        
        return Audio(speaker1, sr), Audio(speaker2, sr)