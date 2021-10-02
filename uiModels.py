class DeckSummary:
    def __init__(self, matches: int, winNum: int, time: str, startTime: str, deckCode: str):
        self.matches = matches
        self.winNum = winNum
        self.time = time
        self.history = ''
        self.startTime = startTime
        self.deckCode = deckCode
