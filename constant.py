API_KEY = '?api_key=' + 'RGAPI-d8faf3c5-cf10-40a8-a853-7f1acd2f86ca'
MATCH_KEY = 'https://americas.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = 'https://americas.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PPID_KEY = 'C4lYvx3DpbL9aEAV_ukhNgDFidbw4tVExD6Gc1QBatsucGGKuDprnvBMvfwm5Jqp6D1BbsK0mTPnbw'

def getMatchsLink(ppid):
    return MATCH_KEY  + ppid + '/ids' + API_KEY

def getDetailsLink(matchId):
    return DETAILS_KEY + matchId + API_KEY

def getNameLink(ppid):
    return NAME_KEY + ppid + API_KEY