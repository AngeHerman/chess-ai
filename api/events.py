import requests
import ndjson
import time
from dotenv import load_dotenv
import os

BASE_URL = "https://lichess.org"
load_dotenv()

def stream_events():
    token = os.getenv("TOKEN")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = BASE_URL+"/api/stream/event"

    with requests.get(url, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                event = ndjson.loads(line)
                handle_event(event)
            else:
                # Empty line for keep alive
                time.sleep(6)

def handle_event(event):
    nombre_d_elements = len(event)
    print(nombre_d_elements)
    print(event)
    for event_item in event:
        event_type = event_item.get('type')
        if event_type == "gameStart":
            handle_game_start(event_item)
        elif event_type == "gameFinish":
            handle_game_finish(event_item)
        elif event_type == "challenge":
            handle_challenge(event_item)
        elif event_type == "challengeCanceled":
            handle_challenge_canceled(event_item)
        elif event_type == "challengeDeclined":
            handle_challenge_declined(event_item)
        else:
            pass

def handle_game_start(event):
    game_info = event.get('game')
    print("game start")
    # Process game start event

def handle_game_finish(event):
    game_info = event.get('game')
    print("game finish")
    # Process game finish event

def handle_challenge(event):
    challenge_info = event.get('challenge')
    challenge_id = challenge_info.get('id')
    challenge_url = challenge_info.get('url')
    status = challenge_info.get('status')
    rated = challenge_info.get('rated')
    color = challenge_info.get('color')
    final_color = challenge_info.get('finalColor')
    speed = challenge_info.get('speed')

    print(f"Challenge recu avec ID: {challenge_id}")
    print(f"Challenge URL: {challenge_url}")
    print(f"Status: {status}")
    print(f"Rated: {rated}")
    print(f"Color: {color}")
    print(f"Final color: {final_color}")
    print(f"Speed: {speed}")

def handle_challenge_canceled(event):
    print("Challenge cancelled")

def handle_challenge_declined(event):
    print("Challenge declined")