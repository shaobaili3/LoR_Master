from typing import List
import json

class Opponent:
    def __init__(self, name: str, rank: int, matches):
        self.name = name
        self.rank = rank
        self.matches = matches
        self.type = 'match'
        self.deckCode = ''

class DeckDetail:
    def __init__(self, matches: int , winNum: int, time: str):
        self.matches = matches
        self.winNum = winNum
        self.time = time
        self.history = ''


class DeckCode:
    def __init__(self, deckCode: str):
        self.type = ''
        self.deckCode = deckCode
