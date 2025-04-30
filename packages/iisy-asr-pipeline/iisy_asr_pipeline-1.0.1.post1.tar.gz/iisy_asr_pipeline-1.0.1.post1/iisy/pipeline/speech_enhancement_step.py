import torchaudio
from df.enhance import enhance
from iisy.pipeline.pipeline_step import PipelineStep
from iisy.pipeline.audio import Audio

class SpeechEnhancementStep(PipelineStep):
    def __init__(self, input_sr: int, output_sr: int, deep_filter_model, df_state):
        super().__init__(input_sr, output_sr)
        self.deep_filter_model = deep_filter_model
        self.df_state = df_state
        
        
    def process(self, audio: Audio) -> Audio:
        audio = audio.resample(self.output_sr, self.resampler)
        
        # Pass the audio through DeepFilterNet
        filtered_audio = enhance(self.deep_filter_model, self.df_state, audio.data)
        
        return Audio(filtered_audio, self.output_sr)