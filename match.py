import constant
import requests
import pip._vendor.requests

import constant as cs




def getMatchs(ppid):
    matchLink = cs.getMatchsLink(ppid)
    #print(matchLink)
    matchRequest =requests.get(matchLink)
    #print(matchRequest.status_code)
    matchs = matchRequest.json()
    return matchs


def getDetails(matchid):
    detailsLink = cs.getDetailsLink(matchid)
    detailsRequest = requests.get(detailsLink)
    details = detailsRequest.json()
    #print(detailsLink)
    #print(str(detailsRequest.status_code) + 'details matchid:' + matchid)
    return details


def getPlayerName(ppid):
    nameLink = cs.getNameLink(ppid)
    nameRequest =requests.get(nameLink)
    name = nameRequest.json()
    #print(nameRequest.status_code)
    return name['gameName'] + "#" + name['tagLine']


def getPlayerPUUID(name, tag):
    puuidLink = cs.getPUUID(name, tag)
    puuidRequest =requests.get(puuidLink)
    id = puuidRequest.json()
    print(puuidLink)
    print(id)
    return id['puuid']



