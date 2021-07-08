from Models import leaderboard
import json

dict = {'Sirturmund': 'NA1', 'Sir Pickle': '80840', '虎牙Ace': '123', 'Trivo': 'BR1', 'Tataa95': 'LAS', 'Drisoth': 'NA1', 'Nix': '4080', 'monke': '2072', 'Doubtfull': 'NA1', 'Calamity Jun': 'NA1', 'AlexTga': 'NA1', 'SUdden': '2002', 'Lazyguga': 'BR1', 'Ogslayer817902': '2667', 'Tako Salvaje': 'PNDEX', 'LuserBeam': '8120', 'Venn': '1119', 'Zorig Dungu': 'NA1', 'Finni': 'STS', 'The ArkKnight': 'NA1', 'Unknow': 'yAD7RdGoqfb5mRzwWXgEiY8KgRK-ROHiNZiNMP0pxMXY340MS8SNjhUJ4R6t-6nPeJ-Xzx7C99avJQ', '420 Minus 351': 'NA1', 'VapozeiroBR': 'HAZE', 'Flock': '2202', 'MonteXristo': 'NA1', 'UchihaJorge': '5833', 'BrokenKokoro': 'OTK', '4LW': 'BR1', 'Darkodius': 'NA1', 'TheBlackBoss': 'moc', 'JD12': '5356', 'Sucessor': 'BR1', 'Minasia': 'OwO', 'Pineapple P4G': 'NA1', 'STAN': 'EU004', 'Jungle Rammus': 'NA1', 'Damian1917': 'LAN', 'DoveLion': 'NA2', 'Card Gamer': 'NA1', 'FilthyGamerWeeb': 'NA1', 'AJTehPro': '2520', 'Im UpSett': 'NA1', 'Vicster': 'ZAD86', 'GhostInMemories': '000', 'leozera': '9238', 'Gillale': '2419', 'iMatt': '8686', 'Elian': '8483', 'Menores': 'BR1', 'Rei Cold': 'BR1', 'bjvee': 'OCE', 'davironti': 'LAN', 'Watch out bro': 'OCE', 'ggDennyS': 'NA1', 'GrandpaRoji': 'NA1', 'Ez2Win': 'HDR', 'ZILterON': 'BR1', 'Pahku': 'OCE', 'LGamesBr': 'HAZE', 'Hazzi': '7904', 'Oneiric': '2639', 'Jason Fleurant': '1313', 'Zult': 'NA2', 'Glop': '2801', 'Busdude': '5648', 'HotSoup': '1516', 'Al3x': '4640', 'ARC Arax': 'LAS', 'AL911AL': '4457', '0511': 'moc', 'Rzoneflame': 'NA1', 'Rods': '015', 'Shadawx': 'NA1', 'mastermind444': 'NA1', 'PsychoPomp': '5486', 'Xeloo': 'LAS', '1longgui': 'NA1', 'Gex': 'DVE', 'AyaneMoonhart': 'OCE', 'RenektonLord44': 'NA1', 'Realkey': 'STS', 'Seku': 'Seku1', 'cayben7': '6996', 'Rüglü': 'DVE', 'HaskeII': 'NA1', 'Yangzera': '000', 'TomasZamo2000': 'LAS', 'BBG': 'CCJY9', 'RhoombaWhack': 'NA1', 'Jonathan Espenan': '4066', 'Autofilled xD': 'NA1', 'MaykaS': 'STS', 'Bluegod': 'NA1', 'FlSHBONES': 'NA1', 'zero': '8819', 'LEOSP': '1214', 'Mr eMOEtional': '1738', 'Maxgotthetracks': '1333', 'FNX Wasrusso': '2020', 'Rhadamanthys': '8993', 'Slyonnic': 'NA1', 'Draquin': '5232', 'diexoazul': 'LAS', 'Chubbs': '8536', 'c is for cookie': 'NA1', 'Secretweaver': 'NA1', 'Hoodeffects': '4739', 'Reginol Blindhop': 'NA1', 'manmart': 'OCE', 'Gru': '9598', 'Okabe': '7380', 'ZeetaB': 'BR1', 'guuuttt': 'gutt', 'Dear Ambellina': 'NA1', 'Cr0cAI': 'LAN', 'Naivye': 'BR1', 'Matias': 'onTop', 'bonzai78': 'OCE', 'Dupl': '8411', 'PrincessPowerful': 'NA1', 'Jables': '5953', 'DeathThePenguin': 'King', 'Fuzzy': 'DVE', 'Coda': '5386', 'Blitz': 'tukay', 'Deach': '2000', 'Duke': '2550', 'LaVieEnRose': 'moc', 'VandalStan': 'VSN', 'Ganancia': '9430', 'Bobagento': 'moc', 'iSanjimo': '777', 'Angeletronic': 'BR1', 'dy岱玄': '7310', 'Rusticles': 'rus', 'PHIBRAIN': 'phi', 'Drandhfc': '2469', 'TTVNicMakesPlays': 'NA1', 'MF Túpac': 'MAFIA', 'abaan': 'NA1', 'FuriousPorobear': 'NA1', 'ChronoMirage': 'NA1', 'turtlduc': '0320', 'Eluwardhayk': 'BR1', 'willtheboss': 'NA1', 'Dyce': 'NA1', 'B1tter': 'lmao', 'mtucks': 'OCE', 'cheeserdude': 'NA1', 'JRellik': 'LAN', 'IzziOwned': 'BR1', 'Reborn NA': 'NA1', 'Dao': 'LAS'}
print(len(dict))

def loadJson():
    try:
        with open('data.json', 'r') as fp:
            global dict
            dict = json.load(fp)
    except IOError as e:
        print('No cache found', e)
        return


leaderboard.updateAll()

board = leaderboard.leaderboards[0]['players']

masterNames = []

masterTags = {}

def getMasterPlayersNames():
    #print(board)
    for player in board:
        #print(player)
        masterNames.append(player['name'])
    print(masterNames)


all = []
noName = []

getMasterPlayersNames()
loadJson()
for name in masterNames:
    if name in dict:
        print(name, dict[name])
        all.append([name, dict[name]])
    else:
        noName.append(name)
print(len(dict))
print(len(all))
print(noName)


from Models import riot
from Models import network
from Models import setting
from Models.setting import Server
from Models import player
from Models import utility
from Models import local
from Models import leaderboard
import json
setting = setting.Setting()
setting.setServer(Server.NA)
network = network.Network(setting)
riot = riot.Riot(network)

for index, name in enumerate(all):
    puuid = riot.getPuuidWithoutCache(name[0], name[1])
    print(index, ':', name, puuid)