import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:6393")

    # def opponent(self):
    #     return self.opponentName

    # # def matchStatus(self):
    # #     return self.isInMatch

    # def matchSummary(self):
    #     self.isInMatch = False
    #     return self.summary

    # def matchHistory(self):
    #     return self.history


print(c.test())

print(c.opponent())

print(c.matchStatus())

print(c.matchHistory())

print(c.matchSummary())