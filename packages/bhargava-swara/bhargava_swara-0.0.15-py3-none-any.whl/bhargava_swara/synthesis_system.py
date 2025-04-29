import numpy as np
import librosa
import soundfile as sf
from scipy.signal import convolve

class InstrumentSynthesizer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        print(f"Initializing instrument synthesizer with sample rate {sample_rate} Hz")
        self.instruments = {
            "veena": self._load_instrument_model("veena"),
            "flute": self._load_instrument_model("flute"),
            "sitar": self._load_instrument_model("sitar"),
            "tabla": self._load_tabla_model()
        }
        self.tanpura = self._load_tanpura_model()
        print("All instrument models loaded successfully")
        
    def _load_instrument_model(self, instrument_name):
        """
        Load the ML model for a melodic instrument
        In a real implementation, you would load your trained models here
        """
        print(f"Creating {instrument_name} samples")
        instrument_samples = {}
        
        # Load samples for each note (C2 to C7)
        for midi_note in range(36, 96):
            note_name = librosa.midi_to_note(midi_note)
            # In real implementation: load from a sample database
            # instrument_samples[note_name] = librosa.load(f"samples/{instrument_name}/{note_name}.wav")
            
            # For hackathon, create synthesized placeholder sounds
            if instrument_name == "veena":
                # Veena has a distinctive plucked string sound with rich harmonics
                duration = 2.0  # seconds
                t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
                freq = librosa.midi_to_hz(midi_note)
                
                # Create a plucked string sound (basic physical modeling)
                # Combine sine waves at fundamental and harmonics with exponential decay
                sample = 0.7 * np.sin(2 * np.pi * freq * t) * np.exp(-5 * t)
                sample += 0.3 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-7 * t)
                sample += 0.2 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-9 * t)
                sample += 0.1 * np.sin(2 * np.pi * 4 * freq * t) * np.exp(-11 * t)
                
                # Add characteristic veena resonance
                resonance_filter = np.exp(-np.linspace(0, 20, 1000))
                sample = convolve(sample, resonance_filter)[:len(t)]
                
            elif instrument_name == "flute":
                # Flute has a more sinusoidal tone with breathy noise
                duration = 1.5  # seconds
                t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
                freq = librosa.midi_to_hz(midi_note)
                
                # Create a breathy flute sound
                sample = np.sin(2 * np.pi * freq * t)
                
                # Add breathiness with filtered noise
                noise = np.random.normal(0, 0.1, len(t))
                noise = np.convolve(noise, np.hanning(100), mode='same')
                
                # Combine sinusoidal tone with noise
                sample = 0.8 * sample + 0.2 * noise
                
                # Apply envelope
                envelope = np.ones_like(t)
                attack = int(0.1 * self.sample_rate)
                release = int(0.3 * self.sample_rate)
                envelope[:attack] = np.linspace(0, 1, attack)
                envelope[-release:] = np.linspace(1, 0, release)
                sample *= envelope
                
            elif instrument_name == "sitar":
                # Sitar has a bright metallic sound with many harmonics and sympathetic strings
                duration = 3.0  # seconds
                t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
                freq = librosa.midi_to_hz(midi_note)
                
                # Create main note with rich harmonics
                sample = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-2 * t)
                
                # Add many harmonics with varying amplitudes
                for i in range(2, 15):
                    harmonic_amp = 0.5 / i
                    sample += harmonic_amp * np.sin(2 * np.pi * i * freq * t) * np.exp(-2.5 * i * t)
                
                # Add characteristic sitar buzz
                buzz = 0.1 * np.random.random(len(t)) * np.exp(-10 * t)
                sample += buzz
                
                # Add sympathetic string resonance
                sympathetic = 0.2 * np.sin(2 * np.pi * freq * 1.5 * t) * np.exp(-1 * t)
                sample += sympathetic
            
            instrument_samples[note_name] = sample
            
        print(f"Created {len(instrument_samples)} samples for {instrument_name}")
        return instrument_samples
    
    def _load_tabla_model(self):
        """
        Load the tabla synthesis model
        For tabla, we need different bols (strokes) rather than pitched notes
        """
        print("Creating tabla bol samples")
        # In a real implementation, load samples for different tabla bols
        tabla_bols = {
            "dha": None,  # placeholder for dha sample
            "dhin": None, # placeholder for dhin sample
            "ta": None,   # placeholder for ta sample
            "tin": None,  # placeholder for tin sample
            "na": None,   # placeholder for na sample
            "tun": None,  # placeholder for tun sample
            "ge": None,   # placeholder for ge sample
            "ke": None,   # placeholder for ke sample
            "ti": None    # placeholder for ti sample
        }
        
        # For hackathon prototype, create synthesized tabla sounds
        duration = 0.5  # seconds
        t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
        
        # Dha - bass and treble combined (deeper sound)
        tabla_bols["dha"] = 0.7 * np.sin(2 * np.pi * 80 * t) * np.exp(-15 * t)
        tabla_bols["dha"] += 0.3 * np.sin(2 * np.pi * 420 * t) * np.exp(-30 * t)
        
        # Dhin - resonant bass (lower pitch)
        tabla_bols["dhin"] = 0.8 * np.sin(2 * np.pi * 65 * t) * np.exp(-10 * t)
        tabla_bols["dhin"] += 0.2 * np.sin(2 * np.pi * 130 * t) * np.exp(-15 * t)
        
        # Ta - treble sound (higher pitch, shorter)
        tabla_bols["ta"] = 0.9 * np.sin(2 * np.pi * 450 * t) * np.exp(-40 * t)
        
        # Tin - resonant treble
        tabla_bols["tin"] = 0.9 * np.sin(2 * np.pi * 420 * t) * np.exp(-30 * t)
        tabla_bols["tin"] += 0.3 * np.sin(2 * np.pi * 840 * t) * np.exp(-45 * t)
        
        # Na - treble with less attack
        tabla_bols["na"] = 0.7 * np.sin(2 * np.pi * 380 * t) * np.exp(-25 * t)
        envelope = np.ones_like(t)
        attack = int(0.02 * self.sample_rate)
        envelope[:attack] = np.linspace(0, 1, attack)
        tabla_bols["na"] *= envelope
        
        # Tun - bass with less attack
        tabla_bols["tun"] = 0.8 * np.sin(2 * np.pi * 90 * t) * np.exp(-20 * t)
        envelope = np.ones_like(t)
        attack = int(0.03 * self.sample_rate)
        envelope[:attack] = np.linspace(0, 1, attack)
        tabla_bols["tun"] *= envelope
        
        # Ge - medium pitch stroke
        tabla_bols["ge"] = 0.7 * np.sin(2 * np.pi * 200 * t) * np.exp(-30 * t)
        
        # Ke - medium high pitch stroke
        tabla_bols["ke"] = 0.8 * np.sin(2 * np.pi * 280 * t) * np.exp(-35 * t)
        
        # Ti - high pitch stroke
        tabla_bols["ti"] = 0.9 * np.sin(2 * np.pi * 350 * t) * np.exp(-38 * t)
        
        print(f"Created {len(tabla_bols)} tabla bol samples")
        return tabla_bols
    
    def _load_tanpura_model(self):
        """Load or create a tanpura drone synthesis model"""
        print("Creating tanpura synthesis model")
        # In a real implementation, you might use recorded tanpura samples
        # or a more sophisticated physical model
        
        # For hackathon prototype, create a simple tanpura synthesis function
        def synthesize_tanpura(tonic_freq, duration=10.0):
            """Synthesize tanpura drone for a given tonic frequency"""
            print(f"Synthesizing tanpura at {tonic_freq:.1f} Hz for {duration:.1f} seconds")
            t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
            
            # Create base tanpura sound with 4 strings (Pa, Sa, Sa, Sa in traditional tuning)
            # or (Pa, ma, Sa, Sa) or other variations
            
            # Sa (tonic)
            sa = 0.6 * np.sin(2 * np.pi * tonic_freq * t)
            
            # Pa (fifth) - typically 3/2 times the tonic frequency
            pa = 0.4 * np.sin(2 * np.pi * (tonic_freq * 1.5) * t)
            
            # Alternative: ma (fourth) - 4/3 times the tonic
            ma = 0.4 * np.sin(2 * np.pi * (tonic_freq * 4/3) * t)
            
            # Lower Sa (octave below)
            low_sa = 0.5 * np.sin(2 * np.pi * (tonic_freq / 2) * t)
            
            # Combine strings with plucking pattern and resonance
            tanpura = np.zeros_like(t)
            
            # Simulate plucking pattern (repeated every ~2-3 seconds)
            pluck_interval = 2.0  # seconds
            num_plucks = int(duration / pluck_interval)
            
            print(f"Creating tanpura with {num_plucks} plucking cycles")
            
            for i in range(num_plucks):
                pluck_time = i * pluck_interval
                pluck_sample = int(pluck_time * self.sample_rate)
                
                if pluck_sample + int(1.5 * self.sample_rate) > len(tanpura):
                    break
                
                # String 1 (Pa)
                env1 = np.exp(-3 * np.linspace(0, 1.5, int(1.5 * self.sample_rate)))
                tanpura[pluck_sample:pluck_sample + len(env1)] += pa[pluck_sample:pluck_sample + len(env1)] * env1
                
                # String 2 (lower Sa) - plucked slightly after
                pluck_sample += int(0.7 * self.sample_rate)
                if pluck_sample + int(1.8 * self.sample_rate) > len(tanpura):
                    break
                    
                env2 = np.exp(-2 * np.linspace(0, 1.8, int(1.8 * self.sample_rate)))
                tanpura[pluck_sample:pluck_sample + len(env2)] += low_sa[pluck_sample:pluck_sample + len(env2)] * env2
                
                # String 3 (Sa) - plucked slightly after
                pluck_sample += int(0.6 * self.sample_rate)
                if pluck_sample + int(2.0 * self.sample_rate) > len(tanpura):
                    break
                    
                env3 = np.exp(-2.5 * np.linspace(0, 2.0, int(2.0 * self.sample_rate)))
                tanpura[pluck_sample:pluck_sample + len(env3)] += sa[pluck_sample:pluck_sample + len(env3)] * env3
                
                # String 4 (Sa or ma) - plucked slightly after
                pluck_sample += int(0.5 * self.sample_rate)
                if pluck_sample + int(2.0 * self.sample_rate) > len(tanpura):
                    break
                    
                env4 = np.exp(-2.2 * np.linspace(0, 2.0, int(2.0 * self.sample_rate)))
                # Choose between Sa or ma for 4th string
                string4 = sa if np.random.random() > 0.3 else ma  # Occasionally use ma instead of Sa
                tanpura[pluck_sample:pluck_sample + len(env4)] += string4[pluck_sample:pluck_sample + len(env4)] * env4
            
            # Add subtle resonance and overtones
            resonance = np.exp(-np.linspace(0, 10, 5000))
            tanpura = convolve(tanpura, resonance)[:len(t)]
            
            # Normalize
            tanpura = tanpura / np.max(np.abs(tanpura)) * 0.8
            
            print(f"Tanpura synthesis complete: {len(tanpura)} samples")
            return tanpura
            
        return synthesize_tanpura
    
    def synthesize_melody(self, melody_data, instrument_name="sitar", output_path=None):
        """
        Synthesize a melody using the specified instrument
        
        Args:
            melody_data: tuple of (f0, voiced_flag) from pitch extraction
            instrument_name: "veena", "flute", or "sitar"
            output_path: optional path to save the output audio
        
        Returns:
            Synthesized audio array
        """
        print(f"\n=== Synthesizing melody with {instrument_name} ===")
        f0, voiced_flag = melody_data
        
        if instrument_name not in self.instruments:
            print(f"Warning: Unknown instrument '{instrument_name}', defaulting to sitar")
            instrument_name = "sitar"
        
        instrument_samples = self.instruments[instrument_name]
        
        # Calculate total duration based on f0 array length
        # Assuming f0 is computed with hop_length=512
        hop_length = 512
        total_frames = len(f0)
        total_duration = total_frames * hop_length / self.sample_rate
        total_samples = int(total_duration * self.sample_rate)
        
        print(f"Melody data: {total_frames} frames, {total_duration:.2f} seconds")
        print(f"Voiced frames: {np.sum(voiced_flag)} ({np.sum(voiced_flag)/len(voiced_flag)*100:.1f}%)")
        
        # Initialize output audio with enough space
        output_audio = np.zeros(total_samples)
        
        # Track when we play each note
        current_note = None
        note_start_frame = 0
        note_count = 0
        
        # Process each frame
        for i, (pitch, voiced) in enumerate(zip(f0, voiced_flag)):
            # Convert frame index to sample index
            frame_sample = i * hop_length
            
            if np.isnan(pitch) or not voiced:
                # Silent frame - end any current note
                if current_note is not None:
                    # Convert frame indices to sample indices
                    start_sample = note_start_frame * hop_length
                    end_sample = frame_sample
                    note_duration = (end_sample - start_sample) / self.sample_rate
                    
                    if note_duration > 0.02:  # Only add notes longer than 20ms
                        self._add_note(output_audio, current_note, start_sample, 
                                      end_sample - start_sample, instrument_samples)
                        note_count += 1
                    
                    current_note = None
                continue
                
            # Convert frequency to closest MIDI note
            midi_note = int(round(librosa.hz_to_midi(pitch)))
            note_name = librosa.midi_to_note(midi_note)
            
            if current_note != note_name:
                # Note change - end previous note
                if current_note is not None:
                    # Convert frame indices to sample indices
                    start_sample = note_start_frame * hop_length
                    end_sample = frame_sample
                    note_duration = (end_sample - start_sample) / self.sample_rate
                    
                    if note_duration > 0.02:  # Only add notes longer than 20ms
                        self._add_note(output_audio, current_note, start_sample, 
                                      end_sample - start_sample, instrument_samples)
                        note_count += 1
                
                # Start new note
                current_note = note_name
                note_start_frame = i
        
        # Add final note if needed
        if current_note is not None:
            start_sample = note_start_frame * hop_length
            end_sample = total_frames * hop_length
            note_duration = (end_sample - start_sample) / self.sample_rate
            
            if note_duration > 0.02:  # Only add notes longer than 20ms
                self._add_note(output_audio, current_note, start_sample, 
                              end_sample - start_sample, instrument_samples)
                note_count += 1
        
        print(f"Synthesized {note_count} notes for melody")
        
        # Check if melody is too quiet
        if np.max(np.abs(output_audio)) < 0.01:
            print("Warning: Melody is very quiet, applying gain")
            output_audio *= 0.8 / max(0.01, np.max(np.abs(output_audio)))
        
        # Save to file if requested
        if output_path:
            sf.write(output_path, output_audio, self.sample_rate)
            print(f"Saved melody to {output_path}")
        
        print(f"Melody synthesis complete: {len(output_audio)} samples, {len(output_audio)/self.sample_rate:.2f}s")
        return output_audio
    
    def _add_note(self, output_audio, note_name, start_sample, duration_samples, instrument_samples):
        """Add a note to the output audio at the specified position"""
        # Find the closest available note if exact note isn't available
        if note_name not in instrument_samples:
            midi_note = librosa.note_to_midi(note_name)
            available_notes = [librosa.note_to_midi(n) for n in instrument_samples.keys()]
            closest_midi = min(available_notes, key=lambda x: abs(x - midi_note))
            note_name = librosa.midi_to_note(closest_midi)
        
        # Get the sample for this note
        sample = instrument_samples[note_name]
        
        # Adjust duration (either trim or apply envelope to desired length)
        if len(sample) > duration_samples:
            # Trim the sample
            adjusted_sample = sample[:duration_samples]
        else:
            # Pad with zeros
            adjusted_sample = np.zeros(duration_samples)
            adjusted_sample[:len(sample)] = sample
        
        # Add to output at the right position
        end_sample = min(start_sample + len(adjusted_sample), len(output_audio))
        if end_sample > start_sample:
            output_audio[start_sample:end_sample] += adjusted_sample[:end_sample-start_sample]
    
    def generate_tabla_rhythm(self, rhythm_data, thaala_pattern=None, output_path=None):
        """
        Generate tabla rhythm based on detected beats and thaala pattern
        
        Args:
            rhythm_data: tuple of (beats, tempo, downbeats) from rhythm extraction
            thaala_pattern: optional specific thaala pattern to use
            output_path: optional path to save the output audio
        
        Returns:
            Synthesized tabla audio array
        """
        print("\n=== Generating tabla rhythm ===")
        beats, tempo, downbeats = rhythm_data
        
        # If no specific thaala pattern is provided, infer from the beats/downbeats
        if thaala_pattern is None:
            # Try to determine the thaala from the beat pattern
            # This is a simplified approach
            if len(downbeats) < 2:
                # Not enough downbeats to determine thaala cycle
                thaala_pattern = ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha"]  # Default to Teentaal
                print("Using default Teentaal pattern (8 beats)")
            else:
                # Estimate thaala cycle length
                if len(beats) < 2:
                    # Not enough beats, use default
                    thaala_pattern = ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha"]
                    print("Not enough beats, using default Teentaal pattern (8 beats)")
                else:
                    avg_cycle_length = np.mean(np.diff(downbeats)) if len(downbeats) >= 2 else 4 * np.mean(np.diff(beats))
                    num_beats_per_cycle = int(round(avg_cycle_length / np.mean(np.diff(beats))))
                    
                    print(f"Estimated thaala cycle: {num_beats_per_cycle} beats")
                    
                    if num_beats_per_cycle == 16:
                        # Likely Teentaal (16 beats)
                        thaala_pattern = ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha",
                                         "na", "tin", "tin", "ta", "ta", "dhin", "dhin", "dha"]
                        print("Using Teentaal pattern (16 beats)")
                    elif num_beats_per_cycle == 7:
                        # Likely Rupak (7 beats)
                        thaala_pattern = ["tin", "tin", "na", "dhin", "na", "dhin", "na"]
                        print("Using Rupak pattern (7 beats)")
                    elif num_beats_per_cycle == 10:
                        # Likely Jhaptaal (10 beats)
                        thaala_pattern = ["dhin", "na", "dhin", "dhin", "na", "tin", "na", "dhin", "dhin", "na"]
                        print("Using Jhaptaal pattern (10 beats)")
                    elif num_beats_per_cycle == 12:
                        # Likely Ektaal (12 beats)
                        thaala_pattern = ["dhin", "dhin", "dha", "dha", "tin", "tin", "ta", "ta", "dhin", "dhin", "dha", "dha"]
                        print("Using Ektaal pattern (12 beats)")
                    elif num_beats_per_cycle == 8:
                        # Likely Keherwa (8 beats)
                        thaala_pattern = ["dha", "ge", "na", "ti", "na", "ke", "dhin", "na"]
                        print("Using Keherwa pattern (8 beats)")
                    else:
                        # Default to Teentaal
                        thaala_pattern = ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha"]
                        print(f"Unusual cycle length ({num_beats_per_cycle}), using modified Teentaal pattern (8 beats)")
        
        # Get total duration (add extra time after the last beat)
        if len(beats) > 0:
            duration = beats[-1] + 2.0  # Add a little extra time
        else:
            # No beats detected, create a default rhythm
            print("Warning: No beats detected, creating default rhythm")
            duration = 30.0  # 30 seconds
            tempo = 80 if tempo <= 0 else tempo  # Default tempo if not detected
            beat_interval = 60.0 / tempo
            beats = np.arange(0, duration - beat_interval, beat_interval)
            print(f"Created {len(beats)} default beats at {tempo} BPM")
        
        # Initialize output audio
        output_audio = np.zeros(int(duration * self.sample_rate))
        tabla_count = 0
        
        # Use tabla samples for each beat
        for i, beat_time in enumerate(beats):
            # Get the appropriate bol for this beat
            bol_idx = i % len(thaala_pattern)
            bol = thaala_pattern[bol_idx]
            
            # Check if bol is available
            if bol not in self.instruments["tabla"]:
                print(f"Warning: Tabla bol '{bol}' not found, using 'dha' instead")
                bol = "dha"  # Default to dha if bol not found
            
            # Get tabla sample for this bol
            sample = self.instruments["tabla"][bol]
            
            # Add to output at the right time
            start_idx = int(beat_time * self.sample_rate)
            end_idx = min(start_idx + len(sample), len(output_audio))
            
            if end_idx > start_idx:
                output_audio[start_idx:end_idx] += sample[:end_idx-start_idx]
                tabla_count += 1
        
        print(f"Added {tabla_count} tabla strokes over {duration:.2f} seconds")
        
        # Save to file if requested
        if output_path:
            sf.write(output_path, output_audio, self.sample_rate)
            print(f"Saved tabla rhythm to {output_path}")
        
        print(f"Tabla rhythm generation complete: {len(output_audio)} samples, {len(output_audio)/self.sample_rate:.2f}s")
        return output_audio
    
    def generate_tanpura(self, raga_data, duration=60.0, output_path=None):
        """
        Generate tanpura drone based on detected raga
        
        Args:
            raga_data: dictionary with raga information including tonic
            duration: duration in seconds
            output_path: optional path to save the output audio
        
        Returns:
            Synthesized tanpura audio array
        """
        print(f"\n=== Generating tanpura drone ===")
        
        # Extract tonic note and convert to frequency
        tonic = raga_data["tonic"]
        try:
            tonic_freq = librosa.note_to_hz(tonic)
            print(f"Using detected tonic: {tonic} ({tonic_freq:.1f} Hz)")
        except Exception as e:
            print(f"Warning: Could not convert tonic {tonic} to frequency: {str(e)}")
            print("Using default frequency of 196 Hz (G3)")
            tonic_freq = 196.0  # G3 as fallback
        
        # Generate tanpura
        tanpura_audio = self.tanpura(tonic_freq, duration)
        
        # Save to file if requested
        if output_path:
            sf.write(output_path, tanpura_audio, self.sample_rate)
            print(f"Saved tanpura to {output_path}")
        
        print(f"Tanpura generation complete: {len(tanpura_audio)} samples, {len(tanpura_audio)/self.sample_rate:.2f}s")
        return tanpura_audio
    
    def mix_outputs(self, melody_audio, tabla_audio, tanpura_audio, melody_gain=1.0, 
                   tabla_gain=0.8, tanpura_gain=0.5, output_path=None):
        """
        Mix different instrument tracks together
        
        Args:
            melody_audio: synthesized melody audio array
            tabla_audio: synthesized tabla audio array
            tanpura_audio: synthesized tanpura audio array
            melody_gain: volume for melody (0.0-1.0)
            tabla_gain: volume for tabla (0.0-1.0)
            tanpura_gain: volume for tanpura (0.0-1.0)
            output_path: optional path to save the output audio
            
        Returns:
            Mixed audio array
        """
        print("\n=== Mixing audio tracks ===")
        
        # Make sure we have audio to mix
        if len(melody_audio) == 0:
            print("Warning: Empty melody audio, using silence")
            melody_audio = np.zeros(10)
        
        if len(tabla_audio) == 0:
            print("Warning: Empty tabla audio, using silence")
            tabla_audio = np.zeros(10)
            
        if len(tanpura_audio) == 0:
            print("Warning: Empty tanpura audio, using silence")
            tanpura_audio = np.zeros(10)
        
        # Determine max length
        max_length = max(len(melody_audio), len(tabla_audio), len(tanpura_audio))
        print(f"Mixing tracks with max length: {max_length} samples ({max_length/self.sample_rate:.2f} seconds)")
        
        # Pad all to same length
        if len(melody_audio) < max_length:
            print(f"Padding melody from {len(melody_audio)} to {max_length} samples")
            melody_audio = np.pad(melody_audio, (0, max_length - len(melody_audio)), 'constant')
        
        if len(tabla_audio) < max_length:
            print(f"Padding tabla from {len(tabla_audio)} to {max_length} samples")
            tabla_audio = np.pad(tabla_audio, (0, max_length - len(tabla_audio)), 'constant')
        
        if len(tanpura_audio) < max_length:
            print(f"Padding tanpura from {len(tanpura_audio)} to {max_length} samples")
            tanpura_audio = np.pad(tanpura_audio, (0, max_length - len(tanpura_audio)), 'constant')
        
        # Mix with specified gains
        print(f"Mixing with gains: melody={melody_gain}, tabla={tabla_gain}, tanpura={tanpura_gain}")
        mixed_audio = (melody_audio * melody_gain + 
                       tabla_audio * tabla_gain + 
                       tanpura_audio * tanpura_gain)
        
        # Check for silence or very low levels
        max_amp = np.max(np.abs(mixed_audio))
        print(f"Mixed audio max amplitude: {max_amp:.4f}")
        
        if max_amp < 1e-6:
            print("Warning: Audio is nearly silent, applying gain")
            mixed_audio = mixed_audio * 0.5  # Arbitrary gain to avoid silence
        else:
            # Normalize to prevent clipping
            mixed_audio = mixed_audio / max_amp * 0.9
            print(f"Normalized mixed audio to prevent clipping (max: {np.max(np.abs(mixed_audio)):.4f})")
        
        # Save to file if requested
        if output_path:
            print(f"Saving mixed audio to {output_path}")
            sf.write(output_path, mixed_audio, self.sample_rate)
        
        print(f"Mixing complete: {len(mixed_audio)} samples, {len(mixed_audio)/self.sample_rate:.2f}s")
        return mixed_audio