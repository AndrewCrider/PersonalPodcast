import os
from glob import glob
from pydub import AudioSegment
import datetime

def combine_audio_files(fileOrder, output_filename):
  
  # Combine audio files
  combined_audio = AudioSegment.empty()
  for audio_file in fileOrder:
    combined_audio += AudioSegment.from_mp3(f"outputLocation/{audio_file}.mp3")

  # Save combined audio
  combined_audio.export(os.path.join("outputLocation", output_filename), format="mp3")  # Modify for other formats
  print(f"Combined audio files into {output_filename}")

# Example usage
output_filename = "finalPodcast.mp3"  # You can change the output filename

today = datetime.date.today()
todaysPrefix = today.strftime("%Y%m%d")
introMusic = "entry_music"
outroMusic = "exit_music"
podcastOrder = [introMusic, f"{todaysPrefix}_open", f"{todaysPrefix}_calendar", f"{todaysPrefix}_tasks", f"{todaysPrefix}_podcast", f"{todaysPrefix}_news", f"{todaysPrefix}_close",outroMusic  ]

#combine_audio_files(podcastOrder, output_filename)
