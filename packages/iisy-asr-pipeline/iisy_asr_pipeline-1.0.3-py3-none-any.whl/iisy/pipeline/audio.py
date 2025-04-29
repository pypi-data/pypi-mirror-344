import numpy as np
import torch
import torchaudio

class Audio:
    data: torch.Tensor
    sr: int
    
    def __init__(self, data: torch.Tensor, sr: int):
        self.data = data
        self.sr = sr
        
    @staticmethod
    def from_numpy(array: np.ndarray, sr: int) -> 'Audio':
        data = torch.from_numpy(array.copy()).float().unsqueeze(0).cpu()
        return Audio(data, sr)
    
    def to_numpy(self) -> np.ndarray:
        return self.data.squeeze(0).cpu().numpy().astype(np.int16)
        
    def tensor(self) -> torch.Tensor:
        return torch.from_numpy(self.data).float().unsqueeze(0)
    
    def resample(self, target_sr: int, resampler: torchaudio.transforms.Resample) -> 'Audio':
        if resampler is None:
            resampler = torchaudio.transforms.Resample(self.sr, target_sr)
        
        if self.sr != target_sr:
            resampled_data = resampler(self.data)
            resampled_data = resampled_data.mean(dim=0, keepdim=True)
            return Audio(resampled_data, target_sr)
        return Audio(self.data, self.sr)
            
    def to_mono(self) -> 'Audio':
        if len(self.data.shape) > 1:
            data = self.data.mean(dim=0, dtype=torch.float32)
            return Audio(data, self.sr)
        return Audio(self.data.copy(), self.sr)
    
    def normalize(self) -> 'Audio':
        return Audio(self.data / torch.max(torch.abs(self.data)), self.sr)
    
def is_silence(audio_chunk: bytes, sample_rate: int=16000, silence_threshold: float=0.03, min_silence_duration: float=0.3) -> bool:
    # Convert to numpy array if needed
    if isinstance(audio_chunk, bytes):
        audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
    else:
        audio_np = audio_chunk.astype(np.float32)
        if audio_np.max() > 1.0:  # Normalize if needed
            audio_np = audio_np / 32768.0
    
    # Get the minimum number of samples for silence duration
    min_silence_samples = int(sample_rate * min_silence_duration)
    
    # If the chunk is too short, it can't contain the required silence
    if len(audio_np) < min_silence_samples:
        return False
    
    # Check the energy of the entire audio since it is at least the minimum duration
    energy = np.sqrt(np.mean(audio_np**2))
    
    # Return True if energy is below the threshold
    return energy < silence_threshold

def is_end_silence(audio_chunk: bytes, sample_rate: int=16000, silence_threshold: float=0.03, min_silence_duration: float=0.3) -> bool:
    """
    Check if the audio chunk contains enough silence and low energy at the end to
    consider it as a sentence boundary.
    
    Args:
        audio_chunk: Audio data as bytes or numpy array
        sample_rate: Audio sample rate in Hz
        silence_threshold: Energy threshold below which audio is considered silence
        min_silence_duration: Minimum duration of silence in seconds
    
    Returns:
        bool: True if the end of the chunk contains silence
    """
    # Convert to numpy array if needed
    if isinstance(audio_chunk, bytes):
        audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
    else:
        audio_np = audio_chunk.astype(np.float32)
        if audio_np.max() > 1.0:  # Normalize if needed
            audio_np = audio_np / 32768.0
    
    # Get the minimum number of samples for silence duration
    min_silence_samples = int(sample_rate * min_silence_duration)
    
    # If the chunk is too short, it can't contain the required silence
    if len(audio_np) < min_silence_samples:
        return False
    
    # Check the energy of the last portion of the audio
    end_portion = audio_np[-min_silence_samples:]
    energy = np.sqrt(np.mean(end_portion**2))
    
    # Return True if energy is below the threshold
    return energy < silence_threshold

def is_silence(audio_chunk: bytes, sample_rate: int=16000, silence_threshold: float=0.03, min_silence_duration: float=0.3) -> bool:
    """
    Check if the audio chunk contains enough silence and low energy to be considered silence.
    
    Args:
        audio_chunk: Audio data as bytes or numpy array
        sample_rate: Audio sample rate in Hz
        silence_threshold: Energy threshold below which audio is considered silence
        min_silence_duration: Minimum duration of silence in seconds
    
    Returns:
        bool: True if the audio chunk is considered silence
    """
    # Convert to numpy array if needed
    if isinstance(audio_chunk, bytes):
        audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
    else:
        audio_np = audio_chunk.astype(np.float32)
        if audio_np.max() > 1.0:  # Normalize if needed
            audio_np = audio_np / 32768.0
    
    # Get the minimum number of samples for silence duration
    min_silence_samples = int(sample_rate * min_silence_duration)
    
    # If the chunk is too short, it can't contain the required silence
    if len(audio_np) < min_silence_samples:
        return False
    
    # Check the energy of the entire audio since it is at least the minimum duration
    energy = np.sqrt(np.mean(audio_np**2))
    
    # Return True if energy is below the threshold
    return energy < silence_threshold