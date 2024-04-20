from unrealspeech import UnrealSpeechAPI
import unrealspeech.utils as unreal
import configparser
import podcastReader
from elevenlabs import save, play
from elevenlabs.client import ElevenLabs
from google.cloud import texttospeech
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import timedelta, datetime
from pathlib import Path
from openai import OpenAI


config = configparser.ConfigParser()
config.read('config.ini')
eleven_api_key = config['elevenLabs']['apiKey']
unrealSpeech_api_key = config['unrealSpeech']['apiKey']
credentials_file = config['googleJsonFileLocation']['jsonFile']
openAI_key = config['OpenAI']['apiKey']


#elevenLabs
client = ElevenLabs(
  api_key= eleven_api_key # Defaults to ELEVEN_API_KEY
)

def generateText(texttoSpeak, voiceID, file_prefix):

    audio = client.generate(
        text = texttoSpeak,
        voice = voiceID,
        model="eleven_multilingual_v2"
    )

    save(audio, f"outputLocation/{file_prefix}.mp3")


#Google Speech
class googleSpeech:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.client = None

    def authenticate(self):
            # Load credentials from the JSON file
        credentials = service_account.Credentials.from_service_account_file(self.credentials_file)

        # Create a Text-to-Speech client
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
    
    def speech_generation(self, text,  voice_name="en-US-Standard-C", fileprefix = "test_output"):

        # Build the synthesis request
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_selection = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        try:
            # Send the request and get the response
            speechResponse = self.client.synthesize_speech(
                input= synthesis_input, voice =voice_selection, audio_config=audio_config
            )

            # Get the synthesized audio data
            audio_content = speechResponse.audio_content

            # Save the audio to a file 
            with open(f"outputLocation/{fileprefix}.mp3", "wb") as out:
                out.write(audio_content)
                print(f"Speech synthesized and saved to output.mp3")

            return audio_content  # You can optionally return the audio data

        except Exception as e:
            raise Exception(f"Error during Text-to-Speech: {e}")

def googleText_to_mp3(text: str, voice: str, fileprefix: str):
    client = googleSpeech(credentials_file)
    client.authenticate()
    client.speech_generation(text, voice, fileprefix)


#OpenAI Voice
open_ai_client = OpenAI(api_key=openAI_key)

def generateOpenAISpeech(texttoSpeak, voiceID, file_prefix):

  response = open_ai_client.audio.speech.create(
    model="tts-1",
    voice=voiceID,
    input=texttoSpeak
  )

  response.write_to_file(f"outputLocation/{file_prefix}.mp3")


#Unreal Speech

def generateUnrealSpeech(texttoSpeak, voiceID, file_prefix):
    speech_api = UnrealSpeechAPI(unrealSpeech_api_key)  
    
    response = speech_api.speech(
        text=texttoSpeak,
        voice_id=voiceID, 
    )

    # you can use the save function to save the audio
       
    unreal.save(response, f"outputLocation/{file_prefix}.mp3")
    
   

