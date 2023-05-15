import requests
import json
import os
import time
import urllib.request
from dotenv import load_dotenv
import math

# Load the .env file
load_dotenv()

# Get the value of the PLAYHT_API_KEY variable
PLAYHT_API_KEY = os.getenv('PLAYHT_API_KEY')
PLAYHT_API_USER_ID = os.getenv('PLAYHT_API_USER_ID')


def generate_ultra_track(body, voice="Larry", speed="0.85"):
    """
    Generate an audio track using Play.ht API with the given text, voice, and speed.

    Args:
        body (str): The text content to be converted to audio.
        voice (str, optional): The voice to be used for the audio. Defaults to "Larry".
        speed (str, optional): The speed of the audio playback. Defaults to "0.85".

    Returns:
        str: The transcription ID of the generated audio track.
    """
    url = "https://play.ht/api/v1/convert"

    payload = json.dumps({
    "voice": voice,
    "content": [
        body,
    ],
    "speed": speed,
    "preset": "balanced"
    })
    headers = {
    'Authorization': PLAYHT_API_KEY,
    'X-User-ID': PLAYHT_API_USER_ID,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)['transcriptionId']


def download_file(file_url, file_name, directory):
    """
    Download a file from the specified URL and save it to the given directory with the given file name.

    Args:
        file_url (str): The URL of the file to download.
        file_name (str): The name to save the downloaded file as.
        directory (str): The directory to save the file in.

    Returns:
        None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}  
    r = requests.get(file_url,headers=headers)


    url = 'https://example.com/myfile.txt'
    local_filename, headers = urllib.request.urlretrieve(file_url, file_path)


def ultra_play_ht_get_id(transaction_id: str):
    """
    Get the audio URL for the given transcription ID using Play.ht API.

    Args:
        transaction_id (str): The transcription ID to get the audio URL for.

    Returns:
        str: The audio URL of the generated audio track.
    """
    url = f"https://play.ht/api/v1/articleStatus?transcriptionId={transaction_id}&ultra=true"
    payload = json.dumps({
    'transcriptionId': transaction_id,

    })

    headers = {
    'Authorization': PLAYHT_API_KEY,
    'X-User-ID': PLAYHT_API_USER_ID,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)['audioUrl'][0]


def generate_track_on_machine(body, file_name, directory, voice="Larry", speed="0.85"):
    """
    Generate an audio track on a local machine with the given text, voice, and speed.

    Args:
        body (str): The text content to be converted to audio.
        file_name (str): The name to save the generated audio file as.
        directory (str): The directory to save the audio file in.
        voice (str, optional): The voice to be used for the audio. Defaults to "Larry".
        speed (str, optional): The speed of the audio playback. Defaults to "0.85".

    Returns:
        None
    """
    id = generate_ultra_track(body,voice,speed)

    audio_url = ultra_play_ht_get_id(id)
    print(audio_url)
    time.sleep(45)
    try:
        download_file(audio_url,file_name,directory)
    except:
        print("Issue downloading audio")
        

if __name__ == "__main__":
    text = 'This was a few weeks ago. I was flying to visit my best friend across the USA FL-CA. I get on and am in the back of the plane in an aisle seat 23C. Upon arrival I see a 20 something (f) sitting in my seat so I point out "Hey sorry you are probably in the wrong seat" and show her my ticket. With an eye roll that could have sounded like she was playing Yahtzee she says "oh I\'m 24C." I look at 24C right behind her and see why she took my seat. There is a 300-400lb (f) sitting in the middle seat. I\'m a 6\'1 230lb (m) ...not ideal. After a 15 second stare down I say "well?" and she says she is \'comfortable already\' and \'not moving\' and \'wants to sleep\' blah blah. OK I see how it is....real dumb to put someone upset with you in the seat behind you...I proceeded to set a silent timer on my phone that went off every two minutes to remind myself to kick her seat, violently, and then every time the seat belt sign went off I\'d get up, grabbing the top of the seat to lift myself up pulling her seat back and forth and one time (accidental but worth) pulled her hair she put over the back of the seat. Safe to say she had lots of extra \'turbulence\' and got absolutely no sleep. There were MANY death stares and head turns. Each time I would just smile and wave. I knew she wouldn\'t say anything either because she is not even supposed to be in that seat anyways. Happy travels.'
    words = text.split()
    chunk_size = 10
    num_chunks = math.ceil(len(words) / chunk_size)
    time.sleep(400)

    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk = " ".join(words[start:end])
        filename = f"track_{i}.wav"
        generate_track_on_machine(chunk, filename, r"\sample")
        time.sleep(400)