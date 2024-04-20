import datetime
import google.generativeai as genai
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
gemini_api_key = config['gemini']['apiKey']

today = datetime.date.today()


def openingDialogue(transcript):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt_prefix = f"You are an enthusastic pod cast host.  The podcast you are hosting covers tasks, calendars, and news of the day.  Todays's date is {today}" + \
                    "Your job is to give a burst of energy at the top of the podcast. Given the summary presented below, give a 45 word intro. Try to make it funny." + \
                    " Here's the transcript for today:\n"

   
    podcastsSummaryRequest = prompt_prefix + str(transcript)
    
    response = model.generate_content(podcastsSummaryRequest)
    returnText = response.text
    
    return returnText

def closingDialogue(transcript):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt_prefix = "You are an enthusastic pod cast host.  The podcast you are hosting covers tasks, calendars, and news of the day. " + \
                    "Your job is to send the listerner off on a high note. Given the summary presented below, give a 45 word outro. Try to make it funny." + \
                    " Here's the transcript for today:\n"

    podcastsSummaryRequest = prompt_prefix + str(transcript)
   
    try:
        response = model.generate_content(podcastsSummaryRequest)
        if response.text:
            returnText = response.text
        else:
            returnText = "That's it for today!  Check Back Tomorrow"
    except Exception as e:
        returnText = "There was a problem with my summarizer. I must have been naughty"
        print(f"Error during Text-to-Speech: {e}")

   
    
      
    return returnText


