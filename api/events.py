import requests
import ndjson
import time
from dotenv import load_dotenv
import os

GAME_ID = None
CODE_CHALLENGE_SUCCES = 201
CODE_MOVE_SUCCES = 200
BASE_URL = "https://lichess.org"
LEVEL_IA = 1
CLOCK_LIMIT = 10800
CLOCK_INCREMENT = 5
COLOR = "black"
GAME_TYPE = "standard"
load_dotenv()
token = os.getenv("TOKEN")
headers = {
    "Authorization": "Bearer "+token
}

def stream_events():
    url = BASE_URL+"/api/stream/event"
    with requests.get(url, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                event = ndjson.loads(line)
                handle_event(event)
            else:
                time.sleep(2)

def challenge_ai():
    url = BASE_URL+"/api/challenge/ai"
    data = {
        "level": LEVEL_IA,
        "clock.limit": CLOCK_LIMIT,
        "clock.increment": CLOCK_INCREMENT,
        "color": COLOR,
        "variant": GAME_TYPE
    }

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == CODE_CHALLENGE_SUCCES:
        print("AI challenge request successful")
        # C est du ndjon du coup je convertis en python bref en une liste d'objets
        response_json = process_ndjson_response(response)
        handle_challenge_accepted(response_json)
        return True
    else:
        print("Failed to send AI challenge request")
        print(response)
        return False

def make_move(move):
    url = f"https://lichess.org/api/bot/game/{GAME_ID}/move/{move}"

    response = requests.post(url, data='', headers=headers)

    if response.status_code == CODE_MOVE_SUCCES:
        print("Move successful")
        return True
    else:
        print("Failed to make move")
        return False

def process_ndjson_response(response):
    response_lines = response.iter_lines()
    response_json = ndjson.loads(next(response_lines))
    return response_json

def handle_challenge_accepted(response_json):
    global GAME_ID
    GAME_ID = response_json[0].get("id")
    print("Challenge ID:", GAME_ID)
    print(response_json)
    
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