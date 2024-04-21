import talktracks
import newsGeneration
import googleCalendar
import podcastReader
import weather
import todoist
import textToSpeech
import podcastPublication

import datetime
import random


today = datetime.date.today()
todaysPrefix = today.strftime("%Y%m%d")
#Choose Your Voices Here: https://elevenlabs.io/app/voice-lab
elevenLabvoiceID = "Eq7d3S8Qw8wQD5JNck7B"
#From https://cloud.google.com/text-to-speech/docs/voices
googleVoiceID = "en-US-Wavenet-F"
#From: https://platform.openai.com/docs/guides/text-to-speech
openAIVoiceID = "nova"
#From: https://docs.unrealspeech.com/reference/parameter-details
unrealSpeechVoiceID = "Liv"
transcript = ""

def getCalendarSummary():
    global transcript
    calendarSummary = googleCalendar.geminiSummary()
    transcript += calendarSummary + "\n"
    textToSpeech.generateUnrealSpeech(calendarSummary, unrealSpeechVoiceID, f"{todaysPrefix}_calendar")
   

def getTasksAudio():
    global transcript
    # Call function from todoist module
    taskResponse = todoist.geminiSummary()
    transcript += taskResponse + "\n"
    textToSpeech.generateUnrealSpeech(taskResponse, unrealSpeechVoiceID, f"{todaysPrefix}_tasks")

def getPodcastAudio():
    global transcript
    # Call function from podcastReader module
    podcastResponse = podcastReader.geminiSummary()
    transcript += podcastResponse + "\n"
    textToSpeech.generateUnrealSpeech(podcastResponse, unrealSpeechVoiceID, f"{todaysPrefix}_podcast")

def getWeatherAudio():
    global transcript
    # Call function from weather module
    weatherResponse = weather.geminiSummary()
    transcript += weatherResponse + "\n"
    textToSpeech.generateUnrealSpeech(weatherResponse, unrealSpeechVoiceID, f"{todaysPrefix}_weather")
    

def getNewsSummary():
    global transcript
    # Call function from articleSummary module
    articleReponse = newsGeneration.geminiSummary()
    transcript += articleReponse + "\n"
    textToSpeech.generateUnrealSpeech(articleReponse, unrealSpeechVoiceID, f"{todaysPrefix}_news")



def assemblePodcast():
    global transcript
    
    with open(f'outputLocation/{todaysPrefix}_transcript.txt', 'w') as file:
        file.write(transcript)

    openTrack = talktracks.openingDialogue(transcript)
    textToSpeech.generateUnrealSpeech(openTrack, unrealSpeechVoiceID, f"{todaysPrefix}_open")
    closing = talktracks.closingDialogue(transcript)
    textToSpeech.generateUnrealSpeech(closing, unrealSpeechVoiceID, f"{todaysPrefix}_close")
    
    introMusic = "entry_music"
    outroMusic = "exit_music"
    podcastOrder = [introMusic, f"{todaysPrefix}_open", f"{todaysPrefix}_calendar", f"{todaysPrefix}_tasks", f"{todaysPrefix}_podcast", f"{todaysPrefix}_news", f"{todaysPrefix}_close", outroMusic  ]


    podcastPublication.combine_audio_files(podcastOrder, f"{todaysPrefix}_finalPodcast.mp3" )
    print("Successfull Generation")
   

def main():
    global transcript
    # Call all the other functions
    
    getWeatherAudio()
    getPodcastAudio()
    getTasksAudio()
    getNewsSummary()
    getCalendarSummary()
    
    assemblePodcast()

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
