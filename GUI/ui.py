from typing import List
import json

# class Match:
#     def __init__(self, outcome: str, time: str, regions: str, champions: str,
#                  deckCode: str):
#         self.outcome = outcome
#         self.time = time
#         self.regions = regions
#         self.champions = champions
#         self.deckCode = deckCode


class Opponent:
    def __init__(self, name: str, rank: int, matches):
        self.name = name
        self.rank = rank
        self.matches = matches

class DeckDetail:
    def __init__(self, matches: int , winNum: int, time: str):
        self.matches = matches
        self.winNum = winNum
        self.time = time


# match = Match('a', 'a', 'a', 'a', 'a')
# jsonStr = json.dumps(match.__dict__)
# # print(jsonStr)

# op = Opponent('a', 1, [match] * 3)


# jsonStr2 = json.dumps(op.__dict__)

