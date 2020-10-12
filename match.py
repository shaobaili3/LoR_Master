import constant
import requests

from constant import getDetailsLink, getMatchsLink, getNameLink

def getMatchs(ppid):
    matchLink = getMatchsLink(ppid)
    #print(matchLink)
    matchRequest =requests.get(matchLink)
    #print(matchRequest.status_code)
    matchs = matchRequest.json()
    return matchs


def getDetails(matchid):
    detailsLink = getDetailsLink(matchid)
    detailsRequest = requests.get(detailsLink)
    details = detailsRequest.json()
    #print(detailsLink)
    #print(str(detailsRequest.status_code) + 'details matchid:' + matchid)
    return details


def getPlayerName(ppid):
    nameLink = getNameLink(ppid)
    nameRequest =requests.get(nameLink)
    name = nameRequest.json()
    #print(nameRequest.status_code)
    return name['gameName'] + "#" + name['tagLine']




