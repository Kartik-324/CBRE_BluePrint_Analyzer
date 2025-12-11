#backend/voice_handler.py
import os
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class VoiceHandler:
    """
    Handle voice input/output for blueprint analysis
    """
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            return transcript.text
        
        except Exception as e:
            print(f"OpenAI Whisper error: {e}")
            # Fallback to Google Speech Recognition
            return self.transcribe_with_google(audio_path)
    
    def transcribe_with_google(self, audio_path: str) -> str:
        """
        Fallback transcription using Google Speech Recognition
        """
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def text_to_speech(self, text: str, output_path: str) -> str:
        """
        Convert text to speech using gTTS
        """
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
    
    def record_audio_from_microphone(self, duration: int = 10) -> str:
        """
        Record audio from microphone (for future use if needed)
        """
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=duration)
                
                # Save to temporary file
                temp_path = "temp_recording.wav"
                with open(temp_path, "wb") as f:
                    f.write(audio.get_wav_data())
                
                return temp_path
        
        except Exception as e:
            raise Exception(f"Recording failed: {str(e)}")