class GUI:
    def __init__(self):
        self.isInMatch = False
        self.summary = [123456, 1234568, 513558]
        self.history = ['aaaa', 'aaaa', ['asdf', 'adfassdfadf']]
        #self.a = '666'

    def matchStatus(self):
        return self.isInMatch

    def matchSummary(self):
        return self.summary

    def matchHistory(self):
        return self.history

    def matchEnd(self):
        self.isInMatch = True



# a = GUI()
# print(a.a)
