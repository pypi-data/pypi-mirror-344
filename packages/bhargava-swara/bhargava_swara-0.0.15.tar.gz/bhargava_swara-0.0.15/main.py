# main.py (in BHARGAVASWARALIB directory)
from bhargava_swara import AudioAnalyzer, InstrumentSynthesizer
import os
import argparse
import soundfile as sf
import time

def process_music(input_file, output_file, instrument="sitar", debug=False):
    """
    Analyze and synthesize Indian classical music
    
    Args:
        input_file: Path to input audio file
        output_file: Path to save the output audio
        instrument: Instrument to use for melody (veena, flute, or sitar)
        debug: Whether to save intermediate files for debugging
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input audio file not found: {input_file}")
    
    # Check if output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)
    
    # Validate instrument choice
    valid_instruments = ["veena", "flute", "sitar"]
    if instrument not in valid_instruments:
        raise ValueError(f"Instrument must be one of {valid_instruments}")
    
    # Step 1: Analyze the input file
    print(f"\n{'='*50}")
    print(f"ANALYZING: {input_file}")
    print(f"{'='*50}")
    
    analyzer = AudioAnalyzer()
    start_time = time.time()
    try:
        analysis = analyzer.analyze_song(input_file)
    except Exception as e:
        raise RuntimeError(f"Error during audio analysis: {str(e)}")
    
    analysis_time = time.time() - start_time
    print(f"\nAnalysis complete. Elapsed time: {analysis_time:.2f} seconds")
    print(f"Detected tonic: {analysis['raga']['tonic']}")
    print(f"Estimated tempo: {analysis['rhythm'][1]:.1f} BPM")
    
    # Step 2: Synthesize using the analysis results
    print(f"\n{'='*50}")
    print(f"SYNTHESIZING: Using {instrument}")
    print(f"{'='*50}")
    
    synthesizer = InstrumentSynthesizer()
    
    try:
        # Synthesize melody
        print(f"\nGenerating melody using {instrument}...")
        start_time = time.time()
        melody_audio = synthesizer.synthesize_melody(
            analysis["melody"],
            instrument_name=instrument,
            output_path=os.path.join(output_dir, "debug_melody.wav") if debug else None
        )
        print(f"Melody generation complete. Elapsed time: {time.time() - start_time:.2f} seconds")
        
        # Generate tabla rhythm
        print("\nGenerating tabla rhythm...")
        start_time = time.time()
        tabla_audio = synthesizer.generate_tabla_rhythm(
            analysis["rhythm"],
            output_path=os.path.join(output_dir, "debug_tabla.wav") if debug else None
        )
        print(f"Tabla rhythm generation complete. Elapsed time: {time.time() - start_time:.2f} seconds")
        
        # Generate tanpura drone
        print("\nGenerating tanpura drone...")
        start_time = time.time()
        tanpura_audio = synthesizer.generate_tanpura(
            analysis["raga"],
            duration=max(len(melody_audio), len(tabla_audio)) / synthesizer.sample_rate,
            output_path=os.path.join(output_dir, "debug_tanpura.wav") if debug else None
        )
        print(f"Tanpura generation complete. Elapsed time: {time.time() - start_time:.2f} seconds")
        
        # Mix everything together
        print("\nMixing tracks...")
        start_time = time.time()
        mixed_audio = synthesizer.mix_outputs(
            melody_audio,
            tabla_audio,
            tanpura_audio,
            melody_gain=1.0,
            tabla_gain=0.8,
            tanpura_gain=0.6,
            output_path=output_file
        )
        print(f"Mixing complete. Elapsed time: {time.time() - start_time:.2f} seconds")
        
        output_duration = len(mixed_audio) / synthesizer.sample_rate
        print(f"\nSynthesis complete. Output saved to {output_file}")
        print(f"Output duration: {output_duration:.2f} seconds")
        
        return mixed_audio
    
    except Exception as e:
        raise RuntimeError(f"Error during audio synthesis: {str(e)}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze and synthesize Indian classical music")
    parser.add_argument("input_file", help="Path to input audio file")
    parser.add_argument("output_file", help="Path to save the output audio")
    parser.add_argument("--instrument", choices=["veena", "flute", "sitar"], default="sitar",
                        help="Instrument to use for melody (default: sitar)")
    parser.add_argument("--debug", action="store_true", help="Save intermediate files for debugging")
    
    args = parser.parse_args()
    
    try:
        process_music(args.input_file, args.output_file, args.instrument, args.debug)
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())