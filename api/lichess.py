import requests
import ndjson
import time
from dotenv import load_dotenv
import os


STREAM_SLEEP_TIME = 0
GAME_ID = None
CODE_CHALLENGE_SUCCES = 201
CODE_CHALLENGE_ACCEPTED_SUCCES = 200
CODE_MOVE_SUCCES = 200
BASE_URL = "https://lichess.org"
LEVEL_IA = 1
CLOCK_LIMIT = 10800
CLOCK_INCREMENT = 5
# COLOR = "black"
COLOR = "white"
GAME_TYPE = "standard"
load_dotenv()
token = os.getenv("TOKEN")
headers = {
    "Authorization": "Bearer "+token
}

class Lichess:
    def __init__(self):
        self.moves = []
        self.game_against_player_started = False
        self.game_against_ai_started = False
        self.game_id = None
        self.color = None
        self.winner = None
        self.is_finished = False
    
    def stream_events(self):
        url = BASE_URL+"/api/stream/event"
        with requests.get(url, headers=headers, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    event = ndjson.loads(line)
                    self.handle_event(event)
                else:
                    time.sleep(STREAM_SLEEP_TIME)

    def stream_board_state(self,is_my_turn):
        
        url = f"{BASE_URL}/api/bot/game/stream/{self.game_id}"
        with requests.get(url, headers=headers, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    state = ndjson.loads(line)
                    self.handle_board_state(state,is_my_turn)
                else:
                    time.sleep(STREAM_SLEEP_TIME)

    def challenge_ai(self):
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
            response_json = self.process_ndjson_response(response)
            self.handle_challenge_accepted(response_json)
            return True
        else:
            print("Failed to send AI challenge request")
            print(response)
            return False

    def make_move(self,move,is_my_turn):
        url = f"{BASE_URL}/api/bot/game/{self.game_id}/move/{move}"
        response = requests.post(url, data='', headers=headers)
        if response.status_code == CODE_MOVE_SUCCES:
            is_my_turn.clear()
            print("Move successful")
            return True
        else:
            print("Failed to make move "+str(move))
            return False

    def process_ndjson_response(self,response):
        response_lines = response.iter_lines()
        response_json = ndjson.loads(next(response_lines))
        return response_json

    def handle_board_state(self,state,is_my_turn):
        # print("State:--")
        # print(state)
        # print("-------")
        string_moves = ""
        if state[0].get('state'):
            # print(state[0].get('state'))
            # print("-------")
            #print(state[0].get('state').get('moves'))
            string_moves = state[0].get('state').get('moves')
        else:
            #print(state[0].get('moves'))
            string_moves = state[0].get('moves')
        # print(string_moves)
        moves_splited = string_moves.split()
        len_moves = len(moves_splited)
        # print("-------------------------------------------------------------------Longueur est "+str(len(moves_splited)))
        if(self.color == "black"):
            if (len_moves %2 == 0):
                is_my_turn.clear()
                print("pas mon tour")
            else:
                is_my_turn.set()
                print("mon tour ")
        if(self.color == "white"):
            if (len_moves %2 == 1):
                is_my_turn.clear()
                print("pas mon tour")
            else:
                is_my_turn.set()
                print("mon tour ")
        # all_moves[0] = string_moves
        self.moves = moves_splited
        # print("Moves splited")
        print(self.color)
        # print(moves_splited)

    def handle_challenge_accepted(self,response_json):
        #global GAME_ID
        if self.game_id is None:
            self.color = COLOR
            self.game_id = response_json[0].get("id")
            print("Challenge ID:", self.game_id)
            #print(response_json)
        
    def handle_event(self,event):
        nombre_d_elements = len(event)
        # print("Event:--")
        # print(event)
        for event_item in event:
            event_type = event_item.get('type')
            if event_type == "gameStart":
                self.handle_game_start(event_item)
            elif event_type == "gameFinish":
                self.handle_game_finish(event_item)
            elif event_type == "challenge":
                self.handle_challenge(event_item)
            elif event_type == "challengeCanceled":
                self.handle_challenge_canceled(event_item)
            elif event_type == "challengeDeclined":
                self.handle_challenge_declined(event_item)
            else:
                pass

    def handle_game_start(self,event):
        print("game start")
        

    def handle_game_finish(self,event):
        print("game finish")
        game = event.get('game')
        # If our current game is finished
        if( self.game_id is not None and self.game_id == game.get("gameId")):
            self.is_finished = True
            self.winner = game.get("winner")
        
        
        

    def handle_challenge(self,event):
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
        self.color = final_color
        if self.game_id is None:
            self.accept_challenge(challenge_id)
    
    def accept_challenge(self,challenge_id):
        url = f"{BASE_URL}/api/challenge/{challenge_id}/accept"
        response = requests.post(url, headers=headers)
        if response.status_code == CODE_CHALLENGE_ACCEPTED_SUCCES:
            print("challenge request successful")
            #global GAME_ID
            self.game_id = challenge_id
            self.game_against_player_started = True
        else:
            print("Failed to accept challenge request")
            print(response)
        
    def handle_challenge_canceled(self,event):
        print("Challenge cancelled")

    def handle_challenge_declined(self,event):
        print("Challenge declined")