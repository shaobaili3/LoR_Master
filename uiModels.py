class DeckSummary:
    def __init__(self, matches: int , winNum: int, time: str, startTime: str):
        self.matches = matches
        self.winNum = winNum
        self.time = time
        self.history = ''
        self.startTime = startTime