from iisy.pipeline.pipeline_step import PipelineStep
from iisy.pipeline.audio import Audio
import numpy as np
from sklearn.neighbors import NearestNeighbors
from collections import Counter
from scipy.spatial.distance import cdist

class SpeakerIdentificationStep(PipelineStep):
    def __init__(self, input_sr: int, output_sr: int, model, threshold: float):
        super().__init__(input_sr, output_sr)
        self.threshold = threshold
        self.model = model
        self.known_speakers = []
        self.max_embeddings = 20  # Maximum number of embeddings per speaker

    def extract_embedding(self, audio: Audio) -> np.ndarray:
        """Extracts speaker embedding from the audio using the model."""
        return self.model.encode_batch(audio.data).squeeze(0).detach().cpu().numpy().reshape(1, -1)
    
    def process(self, audio):
        """Processes audio and assigns a speaker index."""
        audio = audio.resample(self.output_sr, self.resampler)
        embedding = self.extract_embedding(audio)
        
        embedding = embedding / np.linalg.norm(embedding)
        
        # This is for the first call, where we don't have any known speakers yet
        if not self.known_speakers:
            self.known_speakers.append([embedding])
            return "Speaker 0"
        
        # Compute distances to all known speaker embeddings
        distances = [cdist(embedding, np.vstack(speaker), metric='cosine').flatten() for speaker in self.known_speakers]
        
        # Find the closest speaker (the one with the smallest mean distance)
        min_distances = [np.mean(d) for d in distances]
        
        # Find the closest speaker
        closest_speaker = np.argmin(min_distances)
        min_distance = min_distances[closest_speaker]
        
        if min_distance < self.threshold:
            self.known_speakers[closest_speaker].append(embedding)
            if len(self.known_speakers[closest_speaker]) > self.max_embeddings:
                self.known_speakers[closest_speaker].pop(0)  # Keep memory under control
            return f"Speaker {closest_speaker}"
        else:
            self.known_speakers.append([embedding])
        return f"Speaker {len(self.known_speakers) - 1}"