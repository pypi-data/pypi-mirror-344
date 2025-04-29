# tests/test_analysis_synthesis.py
import unittest
import numpy as np
import soundfile as sf
from bhargava_swara import AudioAnalyzer, InstrumentSynthesizer

class TestAnalysisSynthesis(unittest.TestCase):
    def setUp(self):
        # Create a simple test audio file (sine wave at 261.63 Hz, Middle C)
        self.sample_rate = 22050
        t = np.linspace(0, 5, 5 * self.sample_rate)  # 5 seconds
        self.test_audio = 0.5 * np.sin(2 * np.pi * 261.63 * t)
        self.test_file = "test_input.wav"
        sf.write(self.test_file, self.test_audio, self.sample_rate)

    def tearDown(self):
        # Clean up the test file
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_audio_analyzer(self):
        # Test AudioAnalyzer
        analyzer = AudioAnalyzer(sample_rate=self.sample_rate)
        analysis = analyzer.analyze_song(self.test_file)
        
        # Check if analysis returns expected keys
        self.assertIn("melody", analysis)
        self.assertIn("rhythm", analysis)
        self.assertIn("raga", analysis)
        self.assertIn("timbre", analysis)
        
        # Check melody data
        f0, voiced_flag = analysis["melody"]
        self.assertTrue(len(f0) > 0)
        self.assertTrue(len(voiced_flag) > 0)
        self.assertEqual(len(f0), len(voiced_flag))
        
        # Check rhythm data
        beats, tempo, downbeats = analysis["rhythm"]
        self.assertTrue(isinstance(beats, list))
        self.assertTrue(isinstance(tempo, float))
        self.assertTrue(isinstance(downbeats, list))
        
        # Check raga data
        self.assertIn("tonic", analysis["raga"])
        self.assertTrue(isinstance(analysis["raga"]["tonic"], str))

    def test_instrument_synthesizer(self):
        # Test InstrumentSynthesizer
        synthesizer = InstrumentSynthesizer(sample_rate=self.sample_rate)
        
        # Create dummy analysis data for synthesis
        analysis = {
            "melody": (np.full(1000, 261.63), np.ones(1000, dtype=bool)),  # Constant pitch at Middle C
            "rhythm": ([0, 1, 2, 3, 4], 60.0, [0, 2, 4]),  # Simple rhythm
            "raga": {"tonic": "C4"},
        }
        
        # Test melody synthesis
        melody_audio = synthesizer.synthesize_melody(analysis["melody"], instrument_name="sitar")
        self.assertTrue(len(melody_audio) > 0)
        self.assertTrue(np.max(np.abs(melody_audio)) > 0)  # Ensure audio isn’t silent
        
        # Test tabla rhythm generation
        tabla_audio = synthesizer.generate_tabla_rhythm(analysis["rhythm"])
        self.assertTrue(len(tabla_audio) > 0)
        self.assertTrue(np.max(np.abs(tabla_audio)) > 0)
        
        # Test tanpura generation
        tanpura_audio = synthesizer.generate_tanpura(analysis["raga"], duration=2.0)
        self.assertTrue(len(tanpura_audio) > 0)
        self.assertTrue(np.max(np.abs(tanpura_audio)) > 0)
        
        # Test mixing
        mixed_audio = synthesizer.mix_outputs(melody_audio, tabla_audio, tanpura_audio)
        self.assertTrue(len(mixed_audio) > 0)
        self.assertTrue(np.max(np.abs(mixed_audio)) > 0)

if __name__ == "__main__":
    unittest.main()