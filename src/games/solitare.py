import pygame
from card import Deck, PlayingCard

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
        self.stockpile = []
        self.talon_pile = []

        self.deck.shuffle_deck()
        self.stockpile = self.deck.deck.tolist() #Do this so i can pop from the list

        for i in range(1, 8): #Tableau col marked as i-1 (array indexing)
            for j in range(i): #Range of i because of solitare shtife
                card = self.stockpile.pop()
                if j != i-1: card.front_shown = False

                self.tableau[i-1].append(card)

    # In solitare, to shift from tableau piles you must satisfy these conditions:
    #   1.) The cards you are shifting is of opposite color to the card you are putting it on
    #   2.) The cards you are shifting must be a number one lower than the card you are putting it on
    # Index exists if moving a group of cards (idx should be -1) if just moving one card)
    def swap_tableau_to_tableau(self, orig_pile: list, new_pile: list, idx):

        #Start out with a bunch of guard clauses
        if len(new_pile) != 0:
            if orig_pile[idx].is_same_color(new_pile[-1]): return
            if orig_pile[idx].rank != new_pile[-1].rank - 1: return
        else: #When a tableau pile is empty, you can only put a king on it
            if orig_pile[idx].rank != PlayingCard.KING: return

        new_pile.append(orig_pile[idx:])
        del orig_pile[idx:]
        if len(orig_pile) != 0: orig_pile[-1].front_shown = True

    # Cards from stockpile fall into talon pile until there is no more cards
    # in stockpile, where which all the talon pile cards go back to stockpile.
    def swap_stockpile_to_talon(self):
        if len(self.stockpile) == 0:
            self.stockpile = self.talon_pile[:]
            self.talon_pile.clear()
        else:
            self.talon_pile.append(self.stockpile.pop())

    def swap_talon_to_tableau(self, tableau_pile: list):
        self.swap_tableau_to_tableau(self.talon_pile, tableau_pile, -1)

    def swap_talon_to_foundation(self, tableau_pile: list, foundation_pile: list):
        pass

    def swap_foundation_to_talon(self, foundation_pile: list, tableau_pile: list):
        self.swap_tableau_to_tableau(foundation_pile, tableau_pile, -1)
