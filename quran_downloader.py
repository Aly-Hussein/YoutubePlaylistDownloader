import argparse
import youtube_dl

# Quran playlist I use 
# https://www.youtube.com/playlist?list=PL96519CC4BF5DD993

# To run script in background 
# nohup python3 quran_downloader.py url 

# then add --items 1 2 4 (if you want to download vids 1 2 and 4 only)
# then add --range 5 7 (if you want to download all vids from 5 till 7 inclusivly)

# tail -f nohup.out (to see the output of the background process) 

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('url', help='The URL of the YouTube playlist')

# Add a mutually exclusive group for the indices
group = parser.add_mutually_exclusive_group()
group.add_argument('--items', nargs='+', type=int, help='The indices of the videos to be downloaded')
group.add_argument('--range', nargs=2, type=int, help='The start and end indices of a range of videos to be downloaded')

args = parser.parse_args()

# Set the options in the ydl_opts dictionary based on the arguments
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'retries': 10,  # Retry 10 times if an error occurs
}

if args.items:
    # Convert the list of indices to a comma-separated string
    playlist_items_str = ','.join(str(i) for i in args.items)
    # Set the playlist items based on the string
    ydl_opts['playlist_items'] = playlist_items_str

if args.range:
    # Set the playlist start and end indices based on the arguments
    ydl_opts['playliststart'] = args.range[0]
    ydl_opts['playlistend'] = args.range[1] + 1  # End index should be one past the last video to be downloaded

# Create a YouTube downloader object
ydl = youtube_dl.YoutubeDL(ydl_opts)

# Download the playlist
ydl.download([args.url])
