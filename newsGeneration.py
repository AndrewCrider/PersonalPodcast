import requests
import newspaper
import configparser
import google.generativeai as genai
import random

config = configparser.ConfigParser()
config.read('config.ini')
brave_api_key = config['brave']['apiKey']
gemini_api_key = config['gemini']['apiKey']

#TODO: Modify the news sources as you will
newsSources = ['http://techcrunch.com', 'http://cnn.com', 'http://salon.com' ]


# Including Brave Search and Execute Brave Search are functions that are not used currently, but provide an 
# example on how to augment news sources

class BraveSearch:
  """
  A Python class to interact with the Brave Search API using the requests library.
  """

  def __init__(self, api_key):
    """
    Initializes the BraveSearch class with your API key.

    Args:
      api_key (str): Your Brave Search API token.
    """
    self.api_key = api_key
    self.base_url = "https://api.search.brave.com/res/v1/web/search"

  def search(self, query, headers={}):
    """
    Performs a search on Brave Search using the provided query.

    Args:
      query (str): The search query to be sent to Brave Search.
      headers (dict, optional): Additional headers to be included in the request. Defaults to {}.

    Returns:
      dict: The JSON response from the Brave Search API.

    Raises:
      requests.exceptions.RequestException: If the request fails.
    """
    url = f"{self.base_url}?q={query}"
    headers["Accept"] = "application/json"
    headers["Accept-Encoding"] = "gzip"
    headers["X-Subscription-Token"] = self.api_key
    headers = {**headers, **self.__default_headers()}

    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      return response.json()
    except requests.exceptions.RequestException as e:
      raise e

  def __default_headers(self):
    """
    Returns the default headers used by the class.

    Returns:
      dict: The default headers for Brave Search requests.
    """
    return {"User-Agent": "BraveSearch Python Client"}

def executeBraveSearch(queryString):
  search_client = BraveSearch(api_key=brave_api_key)
  response = search_client.search(queryString)

  if response:
    print("Search results:", response)
  else:
    print("Error: Something went wrong with the search.")

def getNewsPaper(topDomain):
    text_output = ""
    
    newsPaper = newspaper.build(topDomain, memoize_articles=False, language='en')
    articles =newsPaper.articles[:5]
    
    while True:
        chosen = random.choice(articles)

        chosen.download()
        chosen.parse()


        if len(chosen.title) > 10:
        
            text_output += chosen.title + "\n*********\n" +chosen.text + f"\nSource:{topDomain}**********\n"
            break

        else:
            articles.remove(chosen)
            if not articles:
               break
    
    return text_output

def geminiSummary():
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt_prefix = "You are a professional news reader, below are a series of articles, create 75 word summaries for each article. " +\
                    "Try to transition between the articles naturally and include the source, return a series of paragraphs with no special characters" + \
                    " BEGIN Article LIST:\n"

    newsSummaries = ""
    returnText = ""
    for site in newsSources:
        newsSummaries = getNewsPaper(site)
    
        if len(newsSummaries) > 0:
            newsSummaryRequests = prompt_prefix + str(newsSummaries)
            
        try:
            response = model.generate_content(newsSummaryRequests)
            if response.text:
                returnText += response.text
            else:
                returnText += f"News summary generation failed for {site}"
        except Exception as e:
            returnText += "There was a problem with the summarizer. "
            print(f"Error during News Summary Generation for {site}: {e}")
    
    return returnText

    
