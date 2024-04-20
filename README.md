# PersonalPodcast
 Generate Your Own Personal Podcast

To build our personalized daily podcast, we are going to follow three steps:

1. Ingest our data in a raw form from our various data feeds
2. Use an LLM to summarize and create a narrative of those feeds
3. Use a text to speech model to create a personalized podcast.

We can also add AI generated music to add a little flavor to our podcast.  I've stored some sample .mp3 in the **soundFIles** directory.
For this project, I chose the Gemini API from Google.  Right now you have to sign up for a Google Cloud Project and enable billing, but there is a very generous free tier available.  If you would like, you can easily change the generation to OpenAI, or a local LLM like Llama.  

 ## Configuration Requirements
 1. Read the article here for more information:  
 2. In the **supportFiles** directory make sure that you update the example_supportFiles.json for Calendar Entries
    - Check out more information [here](https://medium.com/technology-hits/create-an-automated-database-of-your-google-calendar-events-e3edb75e681e) on how the Google Calendar Module Works
 3. In the **supportFiles** directory make sure that you update the example_cloudServices.json for GCP, this is used for the Gemini LLM Generation and the Google Calendar.
 4. In the **supportFiles** directory, the example_firebase.json file will be used in further versions of this repository.
 5. Config Parser is used to hold API Keys for the various services, you will need to at least get a Google Gemnini API Key and they key for the text-to-speech service you want to use.  Rename **example_config.ini** and replace the keys as necessary.


