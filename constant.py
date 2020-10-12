API_KEY = '?api_key=' + 'RGAPI-b8cd691e-4db7-4cec-9644-84b7e0122286'
MATCH_KEY = 'https://americas.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = 'https://americas.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PPID_KEY = 'R-ZngVUMuoewSO5_Xm6eSCQ3Qk-Tu-631s_uyMZq62pS-4NWjJwU1IVV5jwwWGr_JJUVwtfB8FNQBw'

def getMatchsLink(ppid):
    return MATCH_KEY  + ppid + '/ids' + API_KEY

def getDetailsLink(matchId):
    return DETAILS_KEY + matchId + API_KEY

def getNameLink(ppid):
    return NAME_KEY + ppid + API_KEY