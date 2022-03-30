import requests
import constants as cs
from Models.deck import getDeckCode
import requests
import datetime
import json
from datetime import datetime
import time
import threading

class Local:
    def __init__(self, setting, cache):
        self.setting = setting
        self.cache = cache
        self.session = requests.Session()

        self.reset()

    # call this function after changes server in the tracker

    def reset(self):
        self.opponentName = None
        self.opponentTag = None
        self.playername = None
        self.gameId = None

        self.positional_rectangles = None
        self.trackerDict = {}
        self.playedCards = {}
        self.opGraveyardWithId = {}
        self.opGraveyard = {}
        self.myGraveyard = {}
        self.trackJson = {}

        self.openHand = {}
        self.replacedHnad = {}
        self.startTime = None

        self.timeline = {}
        self.allCard = {}

    def addCardToTimeline(self, card):
        if card['CardID'] not in self.timeline:
            self.timeline[card['CardID']] = card
            self.timeline[card['CardID']
                          ]['showTime'] = datetime.utcnow().isoformat()
            if card['LocalPlayer']:
                self.timeline[card['CardID']
                              ]['drawTime'] = datetime.utcnow().isoformat()
        else:
            if card['LocalPlayer']:
                self.timeline[card['CardID']]['playTime'] = None

    def updateTimeline(self):
        for cardId in self.timeline.keys():
            if cardId not in self.allCard:
                if self.timeline[cardId].get('exitTime') is None:
                    self.timeline[cardId]['exitTime'] = datetime.utcnow(
                    ).isoformat()

        # check if card still in hand for local player for playtime
        for cardId in self.timeline.keys():
            if self.timeline[cardId].get('playTime') is None:
                if cardId not in self.cardsInHand:
                    self.timeline[cardId]['playTime'] = datetime.utcnow(
                    ).isoformat()

    # get latest game result and update self.gameId
    def getResult(self):
        riot_id_lower = self.setting.playerId.lower()
        try:
            resultRequest = self.session.get(self.getResultLink())
            resultJson = resultRequest.json()
            self.gameId = resultJson['GameID'] + 1
            localPlayerWon = resultJson['LocalPlayerWon']
        except Exception as e:
            print('getResult client is not running: ', e)
            self.gameId = None
            return
        # self.startTime = str(datetime.utcnow())
        if riot_id_lower not in self.cache.localMatches:
            self.cache.localMatches[riot_id_lower] = []
        localMatch = {}
        localMatch['startTime'] = self.startTime
        localMatch['endTime'] = datetime.utcnow().isoformat()
        localMatch['localPlayerWon'] = localPlayerWon
        localMatch['opponentName'] = self.opponentName
        localMatch['opponentTag'] = self.opponentTag
        localMatch['deck_tracker'] = self.trackerDict
        localMatch['riot_id'] = self.setting.playerId
        self.cache.localMatches[riot_id_lower].insert(0, localMatch)
        self.cache.saveLocal()
        try:
            url = "https://lormaster.herokuapp.com/tracker"
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = requests.post(url, data=json.dumps(localMatch), headers=headers)
            print(response.text)
        except requests.exceptions.RequestException as e:
            print('post error', e.response)
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
            # self.startTime = datetime.utcnow().isoformat()
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
        if details['CardsInDeck'] is None:
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
        self.trackerDict['timeline'] = list(self.timeline.values())
        self.trackerDict['opponentName'] = self.opponentName
        self.trackerDict['opponentTag'] = self.opponentTag

    def updateStatusFlask(self):
        try:
            localRequest = self.session.get(self.getLocalLink())
            self.positional_rectangles = localRequest.json()
        except Exception as e:
            print('client is not running: ', e)
            self.reset()
            self.setting.isLocalApiEnable = False
            return {}
        self.setting.isLocalApiEnable = True
        if self.positional_rectangles['GameState'] == 'InProgress':
            self.opponentName = self.positional_rectangles['OpponentName']
            if self.startTime is None:
                self.startTime = datetime.utcnow().isoformat()
            self.updateTracker()
            self.updateMyDeck()
            print(self.trackerDict)
        else:
            # save game result here
            if self.startTime is not None:
                self.getResult()
            self.reset()
            self.trackJson['positional_rectangles'] = self.positional_rectangles
            return self.trackJson

        self.trackJson['positional_rectangles'] = self.positional_rectangles
        self.trackJson['deck_tracker'] = self.trackerDict

        return self.trackJson

    def getLocalLink(self):
        return cs.IP_KEY + self.setting.port + cs.LOCAL_MATCH

    def getLocalDeckLink(self):
        return cs.IP_KEY + self.setting.port + cs.LOCAL_DECK

    def getResultLink(self):
        return cs.IP_KEY + self.setting.port + cs.LOCAL_RESULT


    def getWorker(self):
        while True:
            time.sleep(0.2)
            self.updateStatusFlask()

    def startWorker(self):
        n = threading.Thread(target=self.getWorker)
        n.daemon = True
        n.start()