from pytube import YouTube  # !pip install pytube
from pytube.exceptions import RegexMatchError

# where to save
save_path = "./Downloads"

import argparse

parser = argparse.ArgumentParser(description="YouTube Video tag.")
parser.add_argument("--path", type=str)
parser.add_argument("--pod", type=str)
args = parser.parse_args()


url = f"https://youtu.be/{args.path}"
try:
    yt = YouTube(url)
except RegexMatchError:
    print(f"RegexMatchError for '{url}'")

itag = None
# we only want audio files
files = yt.streams.filter(only_audio=True)
for file in files:
    # from audio files we grab the first audio for mp4 (eg mp3)
    if file.mime_type == 'audio/mp4':
        itag = file.itag
        break
    if itag is None:
        # just incase no MP3 audio is found (shouldn't happen)
        print("NO MP3 AUDIO FOUND")

# get the correct mp3 'stream'
stream = yt.streams.get_by_itag(itag)
# downloading the audio
stream.download(
    output_path=save_path,
    filename=f"{args.pod}.mp3"
)