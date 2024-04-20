import feedparser
from datetime import datetime
import google.generativeai as genai
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
gemini_api_key = config['gemini']['apiKey']

#Modify the Feeds, Sample rssFeed Listing available at: 

feeds = [{"title": "On with Kara Swicher", "rssFeed": "https://feeds.megaphone.fm/VMP1684715893"}, 
         {"title": "Offline with Jon Favreau", "rssFeed": "https://feeds.simplecast.com/fQ3mywpV"},
         {"title": "Strict Scrutiny", "rssFeed": "https://feeds.simplecast.com/EyrYWMW2"},
         {"title": "The Dollop", "rssFeed": "https://www.omnycontent.com/d/playlist/885ace83-027a-47ad-ad67-aca7002f1df8/22b063ac-654d-428f-bd69-ae2400349cde/65ff0206-b585-4e2a-9872-ae240034c9c9/podcast.rss"},
         {"title": "The Vergecast", "rssFeed": "https://feeds.megaphone.fm/vergecast"},
         {"title": "The Ezra Klein Show", "rssFeed": "https://feeds.simplecast.com/82FI35Px"},
         {"title": "The Chris Hayes Podcast", "rssFeed": "https://podcastfeeds.nbcnews.com/with"},]

rss_date_format =  "%a, %d %b %Y %H:%M:%S %z"

def getPodCastSummaries():
    todays_podcasts = ""

    for f in feeds:
        NewsFeed = feedparser.parse(f["rssFeed"])
        entry = NewsFeed.entries[0]
        fmtd_date = datetime.strptime(entry.published, rss_date_format)
       
        
        if fmtd_date.date() == datetime.now().date():
            todays_podcasts += (f'{f["title"]}-{entry.published}\n')
            todays_podcasts += entry.title + "\n"
            todays_podcasts += entry.summary + "\n*****\n"
    
    return todays_podcasts

def geminiSummary():
    returnText = ""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt_prefix = "You are a media enthusasist, below are a series of podcast summaries, with each podcast seperated by *****, " + \
                    " your job is to create a one line summary for each one, summarizing the content of each podcast. Try to make each one funny." + \
                    " BEGIN PODCAST LIST:\n"

    todaysPodcasts = getPodCastSummaries()
    
    if len(todaysPodcasts) > 0:
        podcastsSummaryRequest = prompt_prefix + str(todaysPodcasts)
        print(podcastsSummaryRequest)
        
        try:
            response = model.generate_content(podcastsSummaryRequest)
            if response.text:
                returnText = response.text
            else:
                returnText = "Podcast summary generation failed. Please check PodcastAddict for new Podcasts."
        except Exception as e:
            returnText = "There was a problem with the summarizer. Please check PodcastAddict for new Podcasts."
            print(f"Error during Text-to-Speech: {e}")
            
    else:
        returnText = "No new Podcasts today! Go Read a book instead"

    return returnText

   
