from typing import List
import json

class OpponentFlask:
    def __init__(self):
        self.history = []

class DeckDetail:
    def __init__(self, matches: int , winNum: int, time: str):
        self.matches = matches
        self.winNum = winNum
        self.time = time
        self.history = ''