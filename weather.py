# import required modules
import requests, json
import configparser
import datetime
import google.generativeai as genai
import configparser

#configStuff
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['OpenWeather']['apiKey']
lat = config['OpenWeather']['lat']
long= config['OpenWeather']['long']
gemini_api_key = config['gemini']['apiKey']

# base_url variable to store url
base_url = "https://api.openweathermap.org/data/3.0/onecall?"

complete_url = base_url + f"lat={lat}&lon={long}&exclude=minutely&units=imperial&appid={api_key}"

def getDailyWeather():
    response = requests.get(complete_url)
    x = response.json()
    dailyForecast = x['daily']

    for i, forecast in enumerate(dailyForecast[:2]):
        date = datetime.datetime.utcfromtimestamp(forecast['dt'])
        formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
        
        if i == 0:
            label = "today"
        else:
            label = "tomorrow"
        
        forAudio = f"{label}: {formatted_date}\n{forecast['summary']}\nfeelslike: {forecast['feels_like']}\n*****"
        
        #print(forAudio)

def getWeeklyWeather():
    response = requests.get(complete_url)
    x = response.json()
    dailyForecast = x['daily']
    
    for i, forecast in enumerate(dailyForecast[:7]):
        date = datetime.datetime.utcfromtimestamp(forecast['dt'])
        formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
        
        if i == 0:
            label = "today"
        else:
            label = formatted_date
        
        forAudio = f"{label} \n{forecast['summary']}\nfeelslike: {forecast['feels_like']}\n*****"
        
        #print(forAudio)

        return forAudio

def geminiSummary():
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt_prefix = "You are a weather reporter, you are going to create a short weather forecast for the next week.  I'm going to give you a day " + \
                    "and what it feels like.  Tell me the weather today, what you think a man should wear, and then summarize the next few days." + \
                    " Do not return any special characters and format it as a paragraph. You should make puns when possible and only return the next two days. BEGIN Weather Forecast LIST:\n"

    weatherSummaryRequest = prompt_prefix + str(getWeeklyWeather())
    response = model.generate_content(weatherSummaryRequest)
   

    return response.text


