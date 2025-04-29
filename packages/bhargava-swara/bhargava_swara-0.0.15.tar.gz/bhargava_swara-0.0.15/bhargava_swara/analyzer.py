import librosa
import numpy as np

class AudioAnalyzer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        
    def load_audio(self, file_path):
        """Load audio file and return signal and sample rate"""
        print(f"Loading audio file: {file_path}")
        y, sr = librosa.load(file_path, sr=self.sample_rate)
        print(f"Loaded audio: {len(y)} samples, {sr} Hz, duration: {len(y)/sr:.2f}s")
        return y, sr
    
    def extract_melody(self, y, sr):
        """Extract the main melody contour from the audio"""
        print("Extracting melody contour...")
        try:
            # Using librosa's melody extraction
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y, 
                fmin=librosa.note_to_hz('C2'), 
                fmax=librosa.note_to_hz('C7'),
                sr=sr
            )
            
            # Filter out NaN values and show stats
            valid_f0 = f0[~np.isnan(f0)]
            if len(valid_f0) > 0:
                print(f"Melody extraction: {np.sum(voiced_flag)} voiced frames out of {len(voiced_flag)}")
                print(f"F0 range: {np.min(valid_f0):.1f} - {np.max(valid_f0):.1f} Hz")
            else:
                print("Warning: No valid F0 values detected")
                
            return f0, voiced_flag
        except Exception as e:
            print(f"Error in melody extraction: {str(e)}")
            print("Using fallback method for melody extraction")
            
            # Fallback method
            hop_length = 512
            n_frames = 1 + len(y) // hop_length
            f0 = np.zeros(n_frames)
            voiced_flag = np.zeros(n_frames, dtype=bool)
            
            # Extract pitch using simple spectral peaks
            S = np.abs(librosa.stft(y, hop_length=hop_length))
            for i in range(S.shape[1]):
                if np.sum(S[:, i]) > 0:  # If there's energy in this frame
                    peak_idx = np.argmax(S[:, i])
                    f0[i] = librosa.fft_frequencies(sr=sr)[peak_idx]
                    voiced_flag[i] = S[peak_idx, i] > 0.1 * np.max(S[:, i])
            
            print(f"Fallback melody extraction: {np.sum(voiced_flag)} voiced frames")
            return f0, voiced_flag
    
    def extract_rhythm(self, y, sr):
        """Extract rhythm patterns and tempo information"""
        print("Analyzing rhythm...")
        try:
            # Get beat positions using librosa
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Convert tempo to scalar if it's a numpy value
            if isinstance(tempo, np.ndarray):
                tempo = float(tempo)
            
            # Convert beat frames to time
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            # Detect downbeats using onset strength
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            _, downbeat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
            downbeats = downbeat_frames[::4]  # Assuming 4/4 time signature
            downbeat_times = librosa.frames_to_time(downbeats, sr=sr)
            
            print(f"Detected tempo: {tempo:.1f} BPM")
            print(f"Found {len(beat_times)} beats and {len(downbeat_times)} downbeats")
            
            # Make sure we're returning Python lists/floats instead of numpy arrays
            # This prevents formatting issues when these values are printed
            return beat_times.tolist(), float(tempo), downbeat_times.tolist()
        
        except Exception as e:
            print(f"Error in rhythm extraction: {str(e)}")
            print("Using fallback rhythm method")
            
            # Create a simple fallback rhythm
            # Assume a default tempo of 80 BPM if we can't detect it
            default_tempo = 80.0
            
            # Create some beats at regular intervals
            duration = len(y) / sr
            beat_interval = 60.0 / default_tempo  # seconds per beat
            num_beats = int(duration / beat_interval)
            
            # Create beat times at regular intervals
            beat_times = np.linspace(0, duration - beat_interval, num_beats)
            
            # Create downbeats (every 4th beat)
            downbeat_times = beat_times[::4]
            
            print(f"Fallback rhythm: Using default tempo of {default_tempo:.1f} BPM")
            print(f"Created {len(beat_times)} beats and {len(downbeat_times)} downbeats")
            
            return beat_times.tolist(), float(default_tempo), downbeat_times.tolist()
    
    def detect_raga(self, y, sr):
        """Detect the raga (scale) used in the music"""
        print("Analyzing pitch distribution for raga detection...")
        # Extract chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Aggregate chroma to get pitch distribution
        pitch_dist = np.sum(chroma, axis=1)
        pitch_dist = pitch_dist / np.sum(pitch_dist)  # Normalize
        
        # Return the detected tonic and dominant notes
        tonic_idx = np.argmax(pitch_dist)
        tonic = librosa.midi_to_note(tonic_idx + 60)
        
        # Find secondary peaks for scale inference
        pitch_peaks = []
        for i in range(12):
            if pitch_dist[i] > 0.5 * pitch_dist[tonic_idx] and i != tonic_idx:
                pitch_peaks.append(i)
        
        pitch_peaks_notes = [librosa.midi_to_note((p + 60) % 12 + 60) for p in pitch_peaks]
        
        print(f"Detected tonic: {tonic}")
        print(f"Secondary peaks: {', '.join(pitch_peaks_notes) if pitch_peaks_notes else 'None'}")
        
        return {
            "tonic": tonic,
            "pitch_distribution": pitch_dist.tolist(),  # Convert to list for safer serialization
            "chroma": chroma,
            "pitch_peaks": pitch_peaks_notes
        }
    
    def analyze_song(self, file_path):
        """Complete analysis of an input song"""
        print(f"\n=== Starting analysis of {file_path} ===")
        y, sr = self.load_audio(file_path)
        
        print("\n--- Extracting melody ---")
        melody_data = self.extract_melody(y, sr)
        
        print("\n--- Analyzing rhythm ---")
        rhythm_data = self.extract_rhythm(y, sr)
        
        print("\n--- Detecting raga ---")
        raga_data = self.detect_raga(y, sr)
        
        print("\n--- Extracting additional features ---")
        # Extract additional features for synthesis
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        
        print(f"Spectral centroid mean: {float(np.mean(spectral_centroid)):.2f} Hz")
        print(f"Spectral bandwidth mean: {float(np.mean(spectral_bandwidth)):.2f} Hz")
        
        print("\n=== Analysis complete ===\n")
        
        return {
            "melody": melody_data,
            "rhythm": rhythm_data,
            "raga": raga_data,
            "timbre": {
                "spectral_centroid": spectral_centroid,
                "spectral_bandwidth": spectral_bandwidth,
                "spectral_contrast": spectral_contrast
            },
            "audio": y,
            "sr": sr
        }