import pygame
from card import Deck

class Solitare:
    def __init__(self) -> None:
        self.deck = Deck()
        self.logic = SolitareGameLogic(self.deck.deck)


    def draw_elements(self):
        pass

class SolitareGameLogic:
    def __init__(self, card_deck) -> None:
        self.deck = card_deck