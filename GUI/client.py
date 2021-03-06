import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:6393")

print(c.test())

print(c.opponent())

print(c.matchStatus())

print(c.matchHistory())

print(c.matchSummary())