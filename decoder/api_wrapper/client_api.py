import os
import requests
import logging
import json
from .deck import Deck
from .active_game import GameFrame, ExpeditionState

logger = logging.getLogger("TwistedFateLib")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)s :: %(levelname)s | %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class GameStatus:
    def __init__(self, game_id, is_winner):
        self.game_id = game_id
        self.is_winner = is_winner

    @property
    def result(self):
        if self.game_id == -1:
            return "No games played yet this session"
        if self.is_winner: 
            return "Win"
        else: 
            return "Loss"

    def serialize(self, to_dict=False):
        data = {"game_id": self.game_id, "result": self.result}
        return data if to_dict else json.dumps(data)


class LoRClient:

    baseurl = "http://localhost:"

    def __init__(self, api_key, port=21337):
        self.api_key = api_key
        self.port = "port"
        self.baseurl = f"{LoRClient.baseurl}{port}"

    def get_endpoint(self, endpoint):
        url = f"{self.baseurl}/{endpoint}"
        logger.info(f"Getting {endpoint}")
        try:
            response = requests.get(url)
        except:
            logger.error("Cannot connect to LoR Client")
            return
        status = f"{response.status_code} - {response.ok}"
        logger.info(f"Endpoint: {endpoint} response {status}")
        return response.json()

    def current_decklist(self) -> Deck:
        r = self.get_endpoint("static-decklist")
        deck = Deck(**r)
        return deck

    def card_positions(self) -> GameFrame:
        r = self.get_endpoint("positional-rectangles")
        if r:
            logging.debug(r)
            frame = GameFrame(**r)
            return frame
        # return r

    def game_status(self) -> GameStatus:
        r = self.get_endpoint("game-result")
        if r:
            game = GameStatus(r['GameID'], r["LocalPlayerWon"])
            return game

    def expeditions_state(self) -> ExpeditionState:
        r = self.get_endpoint("expeditions-state")
        if r:
            exp = ExpeditionState(**r)
            return exp
