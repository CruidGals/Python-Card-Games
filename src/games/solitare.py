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
        self.stockpile = [[], []] #Includes talon pile (waste pile)

        self.deck.shuffle_deck()
        self.stockpile[0] = self.deck.deck.tolist() #Do this so i can pop from the list

        for i in range(1, 8): #Tableau col marked as i-1 (array indexing)
            for j in range(i): #Range of i because of solitare shtife
                card = self.stockpile[0].pop()
                if j != i-1: card.front_shown = False

                self.tableau[i-1].append(card)

    # In solitare, to shift from tableau piles you must satisfy these conditions:
    #   1.) The card you are shifting is of opposite color to the card you are putting it on
    #   2.) The card you are shifting must be a number one lower than the card you are putting it on
    def swap_tableau_to_tableau(orig_pile: list, new_pile: list):

        #Start out with a bunch of guard clauses
        if(len(new_pile) != 0): #making sure the pile isn't empty before we do this
            if(PlayingCard.is_same_color(orig_pile[-1], new_pile[-1])): return
            if(orig_pile[-1].rank != new_pile[-1].rank - 1): return
        else: #When a tableau pile is empty, you can only put a king on it
            if(orig_pile[-1].rank != PlayingCard.KING): return

        new_pile.append(orig_pile.pop())
        orig_pile[-1].front_shown = True