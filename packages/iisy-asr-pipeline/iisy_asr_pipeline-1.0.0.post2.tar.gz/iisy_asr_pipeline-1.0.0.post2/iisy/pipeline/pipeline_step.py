import torchaudio
from iisy.pipeline.audio import Audio

class PipelineStep:
    def __init__(self, input_sr: int, output_sr: int):
        self.resampler = torchaudio.transforms.Resample(orig_freq=input_sr, new_freq=output_sr)
        self.input_sr = input_sr
        self.output_sr = output_sr

    def process(self, audio: Audio) -> Audio:
        raise NotImplementedError