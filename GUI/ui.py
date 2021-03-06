class GUI:
    def __init__(self):
        self.isInMatch = False
        self.opponentName = '123'
        self.summary = {}
        self.history = ['adf','adfasdf']
        self.testString = 1
        #self.a = '666'

    def opponent(self):
        return self.opponentName

    def matchStatus(self):
        return self.isInMatch

    def matchSummary(self):
        self.isInMatch = False
        return self.summary

    def matchHistory(self):
        return self.history

    def reset(self):
        self.isInMatch = False
        self.opponentName = ''
        self.summary = {}
        self.history = []

    def test(self):
        self.testString += 1
        return self.testString

# a = GUI()
# print(a.a)
