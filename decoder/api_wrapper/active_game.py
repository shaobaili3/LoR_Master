import json
from .card import Card
from .deck import Deck


class Rectangle:
    def __init__(self, **kwargs):
        self.card_id = kwargs.get("CardID", 0)
        self.card_code = kwargs.get("CardCode", None)
        self.top_left_x = kwargs.get("TopLeftX", 0)
        self.top_left_y = kwargs.get("TopLeftY", 0)
        self.width = kwargs.get("Width", 0)
        self.height = kwargs.get("Height", 0)
        self.isLocalPlayer = kwargs.get("LocalPlayer")
        self.card = Card(self.card_code)

    def __repr__(self):
        return f"Rectangle(Card: {self.card_code})"


class Screen:
    def __init__(self, **kwargs):
        self.width = kwargs.get("ScreenWidth", 0)
        self.height = kwargs.get("ScreenHeight", 0)


class GameFrame:
    def __init__(self, **kwargs):
        self.player = kwargs.get("PlayerName", "The Man With No Name")
        self.opponent = kwargs.get("OpponentName", "The Man With No Name")
        self.game_state = kwargs.get("GameState", "Menus")
        self.screen = Screen(**kwargs.get("Screen", None))
        self._rectangles = kwargs.get("Rectangles", [])
        self.rectangles = self.parse_rectangles()

    def parse_rectangles(self):
        rects = [
            rect for rect in self._rectangles if rect["CardCode"] != "face"
        ]
        return list(map(lambda x: Rectangle(**x), rects))

    @property
    def player_rects(self):
        return filter(lambda x: x.isLocalPlayer, self.rectangles)

    @property
    def opponent_rects(self):
        return filter(lambda x: not x.isLocalPlayer, self.rectangles)


class Game:
    def __init__(self, player, opponent, screen, player_deck):
        self.player = player
        self.opponent = opponent
        self.screen = screen
        self.player_cards_used = Deck()
        self.opponent_cards_used = Deck()
        self.initial_player_deck = self.current_player_deck = player_deck
        self.result = None

    def process_frame(self, frame):
        for rect in frame.player_rects:
            if rect.card_id not in [
                    card.id for card in self.player_cards_used.cards
            ]:
                current_card = Card(CardID=rect.card_id,
                                    CardCode=rect.card_code)
                self.player_cards_used.add_card(current_card)
                #remove card from current player deck

        for rect in frame.opponent_rects:
            if rect.card_id not in [
                    card.id for card in self.opponent_cards_used.cards
            ]:
                current_card = Card(CardID=rect.card_id,
                                    CardCode=rect.card_code)
                self.opponent_cards_used.add_card(current_card)


class ExpeditionState:
    def __init__(self, **kwargs):
        self.is_active = kwargs.get("IsActive", False)
        self.state = kwargs.get("State", "Inactive")
        self.record = kwargs.get("Record", [])
        self.draft_picks = kwargs.get("DraftPicks", [])
        self.deck = kwargs.get("Deck")  # TODO: convert to Deck instance
        self.games_played = kwargs.get("Games", 0)
        self.wins = kwargs.get("Wins", 0)
        self.losses = kwargs.get("Losses", 0)

    def __repr__(self):
        return f"Expedition(State: {self.state}, Games Played: {self.games_played})"