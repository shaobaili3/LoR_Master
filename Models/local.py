import requests
from requests import models
from Models import setting
from Models.setting import Server
import constants as cs
from Models.deck import getDeckCode
from Models.process import updateTrackServer
import json


class Local:
    def __init__(self, setting):
        self.opponentName = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False
        self.setting = setting
        self.playername = None
        self.trackerDict = {}
        self.session = requests.Session()
        self.playedCards = {}
        self.graveyard = {}
        self.opGraveyard = {}
        self.myGraveyard = {}
        self.positional_rectangles = None
        self.static_decklist = None
        self.trackJson = {}
        self.handsInHand = {}

    # call this function after changes server in the tracker
    def reset(self):
        self.opponentName = None
        self.playername = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False
        self.playedCards = {}
        self.graveyard = {}
        self.opGraveyard = {}
        self.trackJson = {}
        self.trackerDict = {}

    def updateTracker(self):
        rectangles = self.positional_rectangles['Rectangles']
        if rectangles is None:
            return
        screenHeight = self.positional_rectangles['Screen']['ScreenHeight']
        self.cardsInHand = {}
        for card in rectangles:
            if card['LocalPlayer'] is True:
                if card['Height'] > screenHeight / 5.2 and card['TopLeftY'] < screenHeight / 2:
                    self.cardsInHand[card['CardID']] = card['CardCode']
                    self.playedCards[card['CardID']] = card['CardCode']
            else:
                self.graveyard[card['CardID']] = card['CardCode']
        # have to know if player have changed cards
        if len(self.playedCards) == 0 and len(self.graveyard) == 1:
            self.playedCards = {}
            self.graveyard = {}

    def updateLeftCards(self, currentCards):
        if currentCards is None:
            return
        for key in self.playedCards:
            cardCode = self.playedCards[key]
            if cardCode in currentCards:
                num = currentCards[cardCode]
                if num > 0:
                    num -= 1
                currentCards[cardCode] = num
                if num == 0:
                    del currentCards[cardCode]
        return {x: y for x, y in currentCards.items() if y != 0}

    def updateOpGraveyard(self):
        self.opGraveyard = {}
        for key in self.graveyard:
            cardCode = self.graveyard[key]
            if cardCode in self.opGraveyard:
                self.opGraveyard[cardCode] += 1
            else:
                self.opGraveyard[cardCode] = 1
        if 'face' in self.opGraveyard:
            del self.opGraveyard['face']

    # get drew cards but not in hand and board.
    def updateMyGraveyard(self):
        rectangles = self.positional_rectangles['Rectangles']
        if rectangles is None:
            return
        self.myGraveyard = {}
        myGraveyardWithId = self.playedCards.copy()
        if self.playedCards == {}:
            return
        for card in rectangles:
            if card['LocalPlayer'] is True:
                if card['CardID'] in myGraveyardWithId:
                    del myGraveyardWithId[card['CardID']]
        for key in myGraveyardWithId:
            cardCode = myGraveyardWithId[key]
            if cardCode in self.myGraveyard:
                self.myGraveyard[cardCode] += 1
            else:
                self.myGraveyard[cardCode] = 1
        if 'face' in self.myGraveyard:
            del self.myGraveyard['face']

    def playedCardsToDeck(self):
        myPlayedCards = {}
        # Remove cards in hand
        playedCardWithoutHand = dict(
            self.playedCards.items() - self.cardsInHand.items())
        for cardId, cardCode in playedCardWithoutHand.items():
            if cardCode in myPlayedCards:
                myPlayedCards[cardCode] += 1
            else:
                myPlayedCards[cardCode] = 1
        if 'face' in myPlayedCards:
            del myPlayedCards['face']
        return myPlayedCards

    def updateMyDeck(self):
        try:
            localDeckRequest = self.session.get(self.getLocalDeckLink())
            details = localDeckRequest.json()
        except Exception as e:
            print('updateMyDeck Error: ', e)
            return
        if details['DeckCode'] is None:
            print('updateMyDeck Match is not start')
            return
        currentCards = details['CardsInDeck']
        currentCards = self.updateLeftCards(currentCards)
        currentDeckCode = getDeckCode(currentCards)
        self.trackerDict['deckCode'] = details['DeckCode']
        self.trackerDict['cardsInDeck'] = details['CardsInDeck']
        self.trackerDict['currentDeckCode'] = currentDeckCode
        self.updateOpGraveyard()
        self.trackerDict['opGraveyard'] = self.opGraveyard
        self.trackerDict['opGraveyardCode'] = getDeckCode(self.opGraveyard)
        self.trackerDict['myGraveyard'] = self.myGraveyard
        self.trackerDict['myGraveyardCode'] = getDeckCode(self.myGraveyard)
        self.trackerDict['myPlayedCards'] = self.playedCardsToDeck()
        self.trackerDict['myPlayedCardsCode'] = getDeckCode(
            self.trackerDict['myPlayedCards'])
        self.trackerDict['cardsInHandNum'] = len(self.cardsInHand)

    def updateStatusFlask(self):
        try:
            localRequest = self.session.get(self.getLocalLink())
            self.positional_rectangles = localRequest.json()
        except Exception as e:
            print('client is not running: ', e)
            self.reset()
            return {}
        if self.positional_rectangles['GameState'] == 'InProgress':
            self.updateTracker()
            self.updateMyDeck()
            print(self.trackerDict)
        else:
            self.reset()
            self.trackJson
            self.trackJson['positional_rectangles'] = self.positional_rectangles
            return self.trackJson

        self.trackJson['positional_rectangles'] = self.positional_rectangles
        self.trackJson['deck_tracker'] = self.trackerDict

        opInfo = {}
        self.trackJson['opponent_info'] = opInfo

        return self.trackJson

    def updateTagByName(self, name):
        try:
            with open('data/' + self.setting.getServer() + '.json', 'r', encoding='utf-8') as fp:
                names = json.load(fp)
                if name in names:
                    self.opponentTag = names[name]
                    return
            with open(('Resource/' + self.setting.getServer() + '.dat'), 'r', encoding="utf-8") as search:
                for line in search:
                    fullName = line.rstrip().split('#')
                    if name == fullName[0]:
                        # print(fullName)
                        self.opponentTag = fullName[1]
                        return
        except Exception as e:
            print('updateTagByName', e)
        self.opponentTag = None

    def getLocalLink(self):
        return cs.IP_KEY + self.setting.getPort() + cs.LOCAL_MATCH

    def getLocalDeckLink(self):
        return cs.IP_KEY + self.setting.getPort() + cs.LOCAL_DECK
