#!/usr/bin/env python3
"""
Automatic Subtitle Generator
Extracts audio from video files and generates SRT subtitle files using VOSK speech recognition.
"""
import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
import vosk
import wave
import subprocess
import argparse
from datetime import timedelta


class SubtitleGenerator:
    def __init__(self, vosk_model_path=None, language='en', custom_model=False):
        """
        Initialize the subtitle generator.
        
        Args:
            vosk_model_path (str): Path to the VOSK model directory
            language (str): Language code ('en' for English, 'hi' for Hindi)
            custom_model (bool): Whether using a custom model path
        """
        self.language = language
        self.custom_model = custom_model
        
        if custom_model and vosk_model_path:
            self.vosk_model_path = vosk_model_path
        else:
            self.vosk_model_path = vosk_model_path or self._get_default_model_path()
        
        self.model = None
        self._load_vosk_model()
    
    def _get_default_model_path(self):
        """
        Get default VOSK model path based on your project structure.
        """
        # Get the directory where this script is located (SRT folder)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define model paths based on your structure
        if self.language.lower() == 'hi':
            model_path = os.path.join(script_dir, 'models', 'vosk-model-small-hi-0.22')
        else:  # Default to English
            model_path = os.path.join(script_dir, 'models', 'vosk-model-small-en-us-0.15')
        
        return model_path
    
    def _load_vosk_model(self):
        """Load the VOSK speech recognition model."""
        if not self.vosk_model_path or not os.path.exists(self.vosk_model_path):
            raise ValueError(
                "VOSK model path not found. Please:\n"
                "1. Download a VOSK model from https://alphacephei.com/vosk/models\n"
                "2. Extract it to a directory\n"
                "3. Set the model path in the script or pass it as argument"
            )
        
        print(f"Loading VOSK model from: {self.vosk_model_path}")
        self.model = vosk.Model(self.vosk_model_path)
        print("VOSK model loaded successfully")
    
    def extract_audio(self, video_path, output_audio_path=None, progress_callback=None):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if output_audio_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, 'output')
            os.makedirs(output_dir, exist_ok=True)
            video_name = Path(video_path).stem
            output_audio_path = os.path.join(output_dir, f"{video_name}_extracted.wav")
        
        print(f"Extracting audio from: {video_path}")
        print(f"Output audio file: {output_audio_path}")
        
        if progress_callback:
            progress_callback("Extracting audio from video...")
        
        # Use local ffmpeg.exe from project directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_path = os.path.join(script_dir, 'ffmpeg.exe')

        ffmpeg_cmd = [
            ffmpeg_path,
            '-i', video_path,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-y',
            output_audio_path
        ]
        
        try:
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print("Audio extraction completed successfully")
            return output_audio_path

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            raise RuntimeError(f"Failed to extract audio: {e}")
        except FileNotFoundError:
            raise RuntimeError("FFmpeg is missing. Make sure ffmpeg.exe is in the same folder as this script.")

    
    def transcribe_audio(self, audio_path, progress_callback=None):
        """
        Transcribe audio file using VOSK speech recognition.
        
        Args:
            audio_path (str): Path to audio file
            progress_callback (callable): Callback for progress updates
        
        Returns:
            list: List of transcription segments with timestamps
        """
        print(f"Transcribing audio: {audio_path}")
        
        if progress_callback:
            progress_callback("Transcribing audio...")
        
        # Open audio file
        wf = wave.open(audio_path, 'rb')
        
        # Check audio format
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != 'NONE':
            print("Warning: Audio format might not be optimal for VOSK")
        
        # Initialize VOSK recognizer
        rec = vosk.KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)  # Enable word-level timestamps
        
        results = []
        
        print("Processing audio chunks...")
        total_frames = wf.getnframes()
        processed_frames = 0
        
        while True:
            data = wf.readframes(4000)  # Read 4000 frames at a time
            if len(data) == 0:
                break
            
            processed_frames += 4000
            if progress_callback and total_frames > 0:
                progress = min(processed_frames / total_frames * 100, 100)
                progress_callback(f"Transcribing audio... {progress:.1f}%")
            
            if rec.AcceptWaveform(data):
                # Process complete phrase
                result = json.loads(rec.Result())
                if result.get('text'):
                    results.append(result)
        
        # Get final result
        final_result = json.loads(rec.FinalResult())
        if final_result.get('text'):
            results.append(final_result)
        
        wf.close()
        print(f"Transcription completed. Found {len(results)} segments.")
        return results
    
    def format_timestamp(self, seconds):
        """
        Convert seconds to SRT timestamp format (HH:MM:SS,mmm).
        
        Args:
            seconds (float): Time in seconds
        
        Returns:
            str: Formatted timestamp
        """
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
    
    def generate_srt(self, transcription_results, output_srt_path, progress_callback=None):
        """
        Generate SRT subtitle file from transcription results.
        
        Args:
            transcription_results (list): List of transcription segments
            output_srt_path (str): Path for output SRT file
            progress_callback (callable): Callback for progress updates
        """
        print(f"Generating SRT file: {output_srt_path}")
        
        if progress_callback:
            progress_callback("Generating subtitle file...")
        
        with open(output_srt_path, 'w', encoding='utf-8') as srt_file:
            subtitle_index = 1
            
            for result in transcription_results:
                if not result.get('text'):
                    continue
                
                text = result['text'].strip()
                if not text:
                    continue
                
                # Handle different result formats from VOSK
                if 'result' in result and result['result']:
                    # Word-level timestamps available
                    words = result['result']
                    
                    # Group words into phrases (max 10 words or 3 seconds per subtitle)
                    current_phrase = []
                    phrase_start = None
                    phrase_end = None
                    
                    for word_info in words:
                        word = word_info.get('word', '')
                        start_time = word_info.get('start', 0)
                        end_time = word_info.get('end', 0)
                        
                        if phrase_start is None:
                            phrase_start = start_time
                        
                        current_phrase.append(word)
                        phrase_end = end_time
                        
                        # Create subtitle if phrase is long enough or reaches end
                        if (len(current_phrase) >= 10 or 
                            (phrase_end - phrase_start) >= 3.0 or 
                            word_info == words[-1]):
                            
                            if current_phrase:
                                # Write subtitle entry
                                srt_file.write(f"{subtitle_index}\n")
                                srt_file.write(f"{self.format_timestamp(phrase_start)} --> {self.format_timestamp(phrase_end)}\n")
                                srt_file.write(f"{' '.join(current_phrase)}\n\n")
                                
                                subtitle_index += 1
                                current_phrase = []
                                phrase_start = None
                else:
                    # No word-level timestamps, use segment timestamps
                    start_time = result.get('start', 0)
                    end_time = result.get('end', start_time + 3)  # Default 3-second duration
                    
                    # Split long text into multiple subtitles
                    words = text.split()
                    chunk_size = 10  # Max words per subtitle
                    
                    for i in range(0, len(words), chunk_size):
                        chunk_words = words[i:i + chunk_size]
                        chunk_text = ' '.join(chunk_words)
                        
                        # Calculate proportional timing for chunk
                        chunk_duration = (end_time - start_time) * len(chunk_words) / len(words)
                        chunk_start = start_time + (end_time - start_time) * i / len(words)
                        chunk_end = chunk_start + chunk_duration
                        
                        srt_file.write(f"{subtitle_index}\n")
                        srt_file.write(f"{self.format_timestamp(chunk_start)} --> {self.format_timestamp(chunk_end)}\n")
                        srt_file.write(f"{chunk_text}\n\n")
                        
                        subtitle_index += 1
        
        print(f"SRT file generated successfully with {subtitle_index - 1} subtitles")
    
    def process_video(self, video_path=None, output_srt_path=None, keep_audio=False, progress_callback=None):
        """
        Complete pipeline: extract audio, transcribe, and generate SRT file.
        
        Args:
            video_path (str): Path to input video file (optional, defaults to video folder)
            output_srt_path (str): Path for output SRT file (optional, defaults to output folder)
            keep_audio (bool): Whether to keep extracted audio file
            progress_callback (callable): Callback for progress updates
        
        Returns:
            str: Path to generated SRT file
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Default video path based on your structure
        if video_path is None:
            video_dir = os.path.join(script_dir, 'video')
            video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv','.webm'))]
            if video_files:
                video_path = os.path.join(video_dir, video_files[0])  # Use first video file found
                print(f"Using default video: {video_files[0]}")
            else:
                raise FileNotFoundError("No video files found in video folder")
        
        video_path = os.path.abspath(video_path)
        
        # Default output path based on your structure
        if output_srt_path is None:
            output_dir = os.path.join(script_dir, 'output')
            os.makedirs(output_dir, exist_ok=True)
            video_stem = Path(video_path).stem
            output_srt_path = os.path.join(output_dir, f"{video_stem}_subtitles.srt")
        
        print("="*50)
        print("AUTOMATIC SUBTITLE GENERATOR")
        if self.custom_model:
            print(f"Model: Custom - {os.path.basename(self.vosk_model_path)}")
        else:
            print(f"Language: {'Hindi' if self.language == 'hi' else 'English'}")
            print(f"Model: {os.path.basename(self.vosk_model_path)}")
        print("="*50)
        
        try:
            # Step 1: Extract audio
            audio_path = self.extract_audio(video_path, progress_callback=progress_callback)
            
            # Step 2: Transcribe audio
            transcription_results = self.transcribe_audio(audio_path, progress_callback=progress_callback)
            
            # Step 3: Generate SRT file
            self.generate_srt(transcription_results, output_srt_path, progress_callback=progress_callback)
            
            # Cleanup
            if not keep_audio and os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Temporary audio file removed: {audio_path}")
            
            print("="*50)
            print(f"SUCCESS! Subtitle file created: {output_srt_path}")
            print("="*50)
            
            return output_srt_path
            
        except Exception as e:
            print(f"Error processing video: {e}")
            raise


def main():
    """Main function to run the subtitle generator from command line."""
    parser = argparse.ArgumentParser(description="Generate SRT subtitles from video files")
    parser.add_argument("video_path", nargs='?', help="Path to input video file (optional if using default video folder)")
    parser.add_argument("-o", "--output", help="Output SRT file path")
    parser.add_argument("-m", "--model", help="Path to VOSK model directory")
    parser.add_argument("-l", "--language", choices=['en', 'hi'], default='en', 
                       help="Language for speech recognition (en=English, hi=Hindi)")
    parser.add_argument("--keep-audio", action="store_true", help="Keep extracted audio file")
    parser.add_argument("--custom-model", action="store_true", help="Use custom model path")
    
    args = parser.parse_args()
    
    try:
        # Initialize subtitle generator
        generator = SubtitleGenerator(
            vosk_model_path=args.model, 
            language=args.language,
            custom_model=args.custom_model
        )
        
        # Process video
        srt_path = generator.process_video(
            video_path=args.video_path,
            output_srt_path=args.output,
            keep_audio=args.keep_audio
        )
        
        print(f"\nSubtitle generation completed successfully!")
        print(f"Output file: {srt_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()