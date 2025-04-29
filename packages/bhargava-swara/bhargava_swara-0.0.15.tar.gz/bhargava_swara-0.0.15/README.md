# Bhargava Swara

A Python library for analyzing and visualizing Indian classical music, including spectrogram generation (Mel-frequency, Chroma, CQT, and Cent filterbank), raga, tala, tempo, tradition, ornaments, and full analysis.

## Prerequisites

- **Gemini API Key:**  
  This library uses Google's Gemini API for music analysis. To obtain a key:  
  1. Sign up for a Google Cloud account  
  2. Enable the Generative AI API in the Google Cloud Console  
  3. Create an API key in the "Credentials" section  
  Refer to [Google's Generative AI Docs](https://cloud.google.com/generative-ai/docs) for details

- **Audio Files:**  
  Supported formats include WAV and MP3 for analysis and spectrogram generation

## Installation

Install the library using pip:

```sh
pip install bhargava_swara
```

## Dependencies

- `google-generativeai>=0.1.0`  
- `librosa>=0.10.0`  
- `matplotlib>=3.7.0`  
- `numpy>=1.24.0`

## Spectrogram Generation

Generate various types of spectrograms to visualize different aspects of audio frequency content over time.

### Mel-Frequency Spectrogram
```python
from bhargava_swara import generate_mel_spectrogram

audio = "path/to/audio.wav"
output = "path/to/output_mel_spectrogram.png"
generate_mel_spectrogram(audio, output, n_mels=128, fmax=8000)
print("Mel spectrogram generated successfully!")
```

#### Spectrogram Parameters:
- `audio`: Path to the input audio file (e.g., WAV or MP3)
- `output`: Path to save the PNG file
- Mel-specific: `n_mels` (default: 128), `fmax` (default: 8000)

## Music Analysis

Analyze various aspects of Indian classical music using the Gemini API.

### Raga Analysis
```python
from bhargava_swara import analyze_raga

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_raga(audio, api_key)
print(f"Raga: {result}")
```

### Tala Analysis
```python
from bhargava_swara import analyze_tala

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_tala(audio, api_key)
print(f"Tala: {result}")
```

### Tempo Analysis
```python
from bhargava_swara import analyze_tempo

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_tempo(audio, api_key)
print(f"Tempo: {result}")
```

### Tradition Analysis
```python
from bhargava_swara import analyze_tradition

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_tradition(audio, api_key)
print(f"Tradition: {result}")
```

### Ornament Analysis
```python
from bhargava_swara import analyze_ornaments

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_ornaments(audio, api_key)
print(f"Ornaments: {result}")
```

### Full Music Analysis
```python
from bhargava_swara import analyze_music_full

api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"
result = analyze_music_full(audio, api_key)
print(f"Full Analysis:\n{result}")
```

## Music Synthesis

Create Indian classical music elements with ease.

### New Synthesis Capabilities
In this release, we’ve added advanced synthesis capabilities to generate music based on analyzed audio input. Users can now synthesize melodies, rhythms, and drones using traditional Indian instruments.

#### Usage Example
```python
from bhargava_swara import AudioAnalyzer, InstrumentSynthesizer

# Analyze an audio file
analyzer = AudioAnalyzer()
analysis = analyzer.analyze_song("input.wav")

# Synthesize using sitar, tabla, and tanpura
synthesizer = InstrumentSynthesizer()
melody = synthesizer.synthesize_melody(analysis["melody"], instrument_name="sitar")
tabla = synthesizer.generate_tabla_rhythm(analysis["rhythm"])
tanpura = synthesizer.generate_tanpura(analysis["raga"], duration=2.0)
mixed = synthesizer.mix_outputs(melody, tabla, tanpura, output_path="output.wav")
print("Synthesis completed! Output saved to output.wav")
```

##### Parameters:
- `instrument_name`: Choose from "sitar", "veena", or "flute" for melody synthesis.
- `output_path`: Path to save the synthesized audio file (optional).
- `duration`: Duration of the tanpura drone in seconds (default: 2.0).

#### Command-Line Example
An example script (`main.py`) is provided in the repository for quick testing:
```bash
git clone https://github.com/yourusername/bhargava_swara.git
cd bhargava_swara
python main.py input.wav output.wav --instrument sitar --debug
```
- `--instrument`: Specify the instrument (default: "sitar").
- `--debug`: Save intermediate files for debugging (e.g., melody, tabla, tanpura).
- 
  **Note**: Ensure `ffmpeg` is installed for audio processing. On macOS/Linux:
  - `brew install ffmpeg` (macOS)
  - `sudo apt-get install ffmpeg` (Ubuntu)
  On Windows, download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Future Development

We plan to enhance Bhargava Swara with the following features:

### Spectrogram Enhancements
- **Chroma Spectrogram**: Add support for visualizing pitch class distributions over time.
- **CQT Spectrogram**: Implement constant-Q transform spectrograms for better frequency resolution.
- **Cent Filterbank Spectrogram**: Generate spectrograms using cent-scaled filterbanks for microtonal analysis.

### Analysis Features
- **Automatic Raga Recognition**: Develop algorithms to identify ragas automatically from audio input.
- **Tonic Identification**: Detect the tonic (base pitch) of a performance for accurate analysis.
- **Pitch Extraction**: Extract pitch contours from audio to analyze melodic structure.
- **Rhythm Analysis**: Analyze meter, rhythmic patterns, and structure in talas.

### Synthesis Tools
- **Tala Generation**: Create rhythmic cycles (talas) programmatically for practice or composition.
- **Generate Music Based on Raga**: Synthesize music adhering to a specific raga's rules.
- **Music Imitation**: Generate music imitating the style of a given audio input.

Contributions and suggestions for these features are welcome! Please submit ideas or pull requests to the [GitHub repository](https://github.com/Shouryaanga-Tribe/BhargavaSwaraLibrary).

## License

This library is licensed under the MIT License. See the `LICENSE` file for details.


