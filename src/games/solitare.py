import pygame
from card import Deck

class Solitare:
    def __init__(self) -> None:
        self.logic = SolitareGameLogic()


    def draw_elements(self):
        pass

#Will include no pygame
class SolitareGameLogic:
    def __init__(self) -> None:
        self.deck = Deck()
        self.setup_game()
        
    def setup_game(self):
        self.tableau = [[], [], [], [], [], [], []] #Main playing area
        self.foundation_piles = [[], [], [], []] #Piles that start with ace
        self.stockpile = [[], []] #Includes talon pile (waste pile)

        self.deck.shuffle_deck()
        self.stockpile[0] = self.deck.deck.tolist() #Do this so i can pop from the list

        for i in range(1, 8): #Tableau col marked as i-1 (array indexing)
            for j in range(i): #Range of i because of solitare shtife
                card = self.stockpile[0].pop()
                if j != i-1: card.front_shown = False

                self.tableau[i-1].append(card)