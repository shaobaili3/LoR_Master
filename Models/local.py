import requests
import constants as cs
from Models.deck import getDeckCode
import json
import os
import constants
from datetime import datetime

class Local:
    def __init__(self, setting, cache):
        self.opponentName = None
        self.opponentTag = None
        self.gameId = None
        self.startTime = None
        self.setting = setting
        self.playername = None
        self.trackerDict = {}
        self.session = requests.Session()
        self.playedCards = {}
        self.opGraveyardWithId = {}
        self.opGraveyard = {}
        self.myGraveyard = {}
        self.positional_rectangles = None
        self.static_decklist = None
        self.trackJson = {}
        self.handsInHand = {}

        self.openHand = {}
        self.replacedHnad = {}

        self.timeline = {}
        self.allCard = {}
        self.cache = cache

    # call this function after changes server in the tracker
    def reset(self):
        self.opponentName = None
        self.playername = None
        self.gameId = None
        self.opponentTag = None
        self.playedCards = {}
        self.opGraveyardWithId = {}
        self.opGraveyard = {}
        self.trackJson = {}
        self.trackerDict = {}

        self.openHand = {}
        self.replacedHnad = {}

        self.allCard = {}

    def addCardToTimeline(self, card):
        if card['CardID'] not in self.timeline:
            self.timeline[card['CardID']] = card
            self.timeline[card['CardID']]['drawTime'] = str(datetime.utcnow())

    def updateTimeline(self):
        for cardId in self.timeline.keys():
            if cardId not in self.allCard:
                if self.timeline[cardId].get('exitTime') is None:
                    self.timeline[cardId]['exitTime'] = str(datetime.utcnow())

    # get latest game result and update self.gameId
    def getResult(self):
        try:
            resultRequest = self.session.get(self.getResultLink())
            resultJson = resultRequest.json()
            self.gameId = resultJson['GameID'] + 1
            localPlayerWon = resultJson['LocalPlayerWon']
        except Exception as e:
            print('getResult client is not running: ', e)
            self.gameId = None
            return
        self.startTime = str(datetime.utcnow())
        self.opponentName = 'test'
        self.cache.localMatches[self.startTime + self.opponentName] = {}
        self.cache.localMatches[self.startTime + self.opponentName]['track'] = self.trackerDict
        self.cache.localMatches[self.startTime + self.opponentName]['startTime'] = self.startTime
        self.cache.localMatches[self.startTime + self.opponentName]['localPlayerWon'] = localPlayerWon
        self.cache.localMatches[self.startTime + self.opponentName]['opponentName'] = self.opponentName
        self.cache.localMatches[self.startTime + self.opponentName]['opponentTag'] = self.opponentTag
        self.cache.saveLocal()
        return localPlayerWon

    def updateTracker(self):
        rectangles = self.positional_rectangles['Rectangles']
        if rectangles is None:
            return
        screenHeight = self.positional_rectangles['Screen']['ScreenHeight']
        self.cardsInHand = {}
        self.allCard = {}
        for card in rectangles:
            self.allCard[card['CardID']] = card['CardCode']
            if card['LocalPlayer'] is True:
                # only record the cards in hand for localplayer not on board
                if card['Height'] > screenHeight / 5.2 and card['TopLeftY'] < screenHeight / 2:
                    self.cardsInHand[card['CardID']] = card['CardCode']
                    self.playedCards[card['CardID']] = card['CardCode']
                    self.addCardToTimeline(card)
            else:
                self.opGraveyardWithId[card['CardID']] = card['CardCode']
                self.addCardToTimeline(card)
        self.updateTimeline()
        # player is replacing cards, lor clean all cards after replacement than arrange cards for both players.
        if len(self.playedCards) == 0 and len(self.opGraveyardWithId) == 1 and len(rectangles) == 6:
            self.startTime = str(datetime.utcnow())
            self.opGraveyardWithId = {}
            self.timeline = {}
            # replaceds card will show in the center of screen as same as open cards, so use it to avoid save replaced cards
            if not self.openHand:
                self.openHand = rectangles
        # player has finished replacing
        if len(self.playedCards) == 4 and len(self.cardsInHand) == 4 and len(self.opGraveyardWithId) == 1 and len(rectangles) == 6:
            self.replacedHnad = rectangles

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
        for key in self.opGraveyardWithId:
            cardCode = self.opGraveyardWithId[key]
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
        self.trackerDict['openHand'] = self.openHand
        self.trackerDict['replacedHand'] = self.replacedHnad
        self.trackerDict['timeline'] = self.timeline

    def updateStatusFlask(self):
        try:
            localRequest = self.session.get(self.getLocalLink())
            self.positional_rectangles = localRequest.json()
        except Exception as e:
            print('client is not running: ', e)
            self.reset()
            return {}
        self.opponentName = self.positional_rectangles['OpponentName']
        if self.positional_rectangles['GameState'] == 'InProgress':
            self.updateTracker()
            self.updateMyDeck()
            print(self.trackerDict)
        else:
            # save game result here
            if len(self.openHand) > 0:
                self.getResult()
            self.reset()
            self.trackJson['positional_rectangles'] = self.positional_rectangles
            return self.trackJson

        self.trackJson['positional_rectangles'] = self.positional_rectangles
        self.trackJson['deck_tracker'] = self.trackerDict

        return self.trackJson

    def updateTagByName(self):
        if self.opponentName is None:
            print('updateTagByName:', 'game not start')
            return
        nameListPath = constants.getCacheFilePath(
            self.setting.riotServer.lower() + '.json')
        if not os.path.isfile(nameListPath):
            nameListPath = 'Resource/' + self.setting.riotServer.lower() + '.json'
        try:
            with open(nameListPath, 'r', encoding='utf-8') as fp:
                names = json.load(fp)
                if self.opponentName in names:
                    self.opponentTag = names[self.opponentName]
                    return
            with open(('Resource/' + self.setting.riotServer + '.dat'), 'r', encoding="utf-8") as search:
                for line in search:
                    fullName = line.rstrip().split('#')
                    if self.opponentName == fullName[0]:
                        self.opponentTag = fullName[1]
                        return
        except Exception as e:
            print('updateTagByName', e)
        self.opponentTag = None

    def getLocalLink(self):
        return cs.IP_KEY + self.setting.port + cs.LOCAL_MATCH

    def getLocalDeckLink(self):
        return cs.IP_KEY + self.setting.port + cs.LOCAL_DECK

    def getResultLink(self):
        return cs.IP_KEY + self.setting.port + cs.LOCAL_RESULT
