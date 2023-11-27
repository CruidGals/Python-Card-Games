import pygame
from card import Deck, PlayingCard

'''
TODO Stub:
    - When picking a card, use the "in" operator to detect which pile it is in.
'''

class Solitare:
    def __init__(self, screen_size) -> None:
        self.logic = SolitareGameLogic(screen_size)
        self.start_game()

    def start_game(self):
        pass

    def draw_elements(self):
        pass

    def draw_tableau(self, screen, tableau_pile, starting_pos):
        pos = [starting_pos[0], starting_pos[1]]
        for card in tableau_pile:
            card.draw_card(screen, pos)
            pos[1] = card.front_image.get_size()[1] / 3 + pos[1]

    def draw_stockpile_and_talon(self, screen, starting_pos):
        pos = [starting_pos[0], starting_pos[1]]
        if len(self.logic.stockpile) != 0: self.logic.stockpile[-1].draw_card(screen, pos)
        if len(self.logic.talon_pile) != 0: self.logic.talon_pile[-1].draw_card(screen, (pos[0] + self.logic.talon_pile[-1].front_image.get_size()[0], pos[1]))

#Will include no pygame
class SolitareGameLogic:
    def __init__(self, screen_size) -> None:
        self.deck = Deck(screen_size)
        self.setup_game()

    def setup_game(self):
        self.tableau = [[], [], [], [], [], [], []] #Main playing area
        self.foundation_piles = [[], [], [], []] #Piles that start with ace
        self.stockpile = []
        self.talon_pile = []

        self.points = 0
        self.move_count = 0

        self.deck.shuffle_deck()
        self.stockpile = self.deck.deck.tolist() #Do this so i can pop from the list

        #Flip all cards in stockpile
        for card in self.stockpile:
            card.front_shown = False

        for i in range(1, 8): #Tableau col marked as i-1 (array indexing)
            for j in range(i): #Range of i because of solitare shtife
                card = self.stockpile.pop()
                if j != i-1: card.front_shown = False

                self.tableau[i-1].append(card)

    def is_game_won(self):
        return len(self.foundation_piles[0]) + len(self.foundation_piles[1]) + len(self.foundation_piles[2]) + len(self.foundation_piles[3]) == 52

    #---------------- Swapping Functions ----------------#

    # In solitare, to shift from tableau piles you must satisfy these conditions:
    #   1.) The cards you are shifting is of opposite color to the card you are putting it on
    #   2.) The cards you are shifting must be a number one lower than the card you are putting it on
    # Index exists if moving a group of cards (idx should be -1 if just moving one card)
    def swap_tableau_to_tableau(self, orig_pile: list, new_pile: list, idx):

        #Start out with a bunch of guard clauses
        if len(new_pile) != 0:
            if orig_pile[idx].is_same_color(new_pile[-1]): return
            if orig_pile[idx].rank != new_pile[-1].rank - 1: return
        else: #When a tableau pile is empty, you can only put a king on it
            if orig_pile[idx].rank != PlayingCard.KING: return

        new_pile.append(orig_pile[idx:])
        del orig_pile[idx:]
        if len(orig_pile) != 0 and not orig_pile[-1].front_shown:
            orig_pile[-1].front_shown = True
            self.points += 5

        self.move_count += 1

    # Cards from stockpile fall into talon pile until there is no more cards
    # in stockpile, where which all the talon pile cards go back to stockpile.
    def swap_stockpile_to_talon(self):
        if len(self.stockpile) == 0:
            self.stockpile = self.talon_pile[::-1]

            for card in self.stockpile:
                card.front_shown = False

            self.talon_pile.clear()
        else:
            self.talon_pile.append(self.stockpile.pop())
            self.talon_pile[-1].front_shown = True
        
        self.move_count += 1

    def swap_talon_to_tableau(self, tableau_pile: list):
        self.swap_tableau_to_tableau(self.talon_pile, tableau_pile, -1)
        self.points += 5

    # Foundation piles must "claim" a suit, and will have to be placed in increasing order
    def swap_tableau_to_foundation(self, tableau_pile: list, foundation_pile: list):
        if len(foundation_pile) != 0:
            if tableau_pile[-1].suit != foundation_pile[-1].suit: return
            if tableau_pile[-1].rank != foundation_pile[-1].rank + 1: return
        else:
            if tableau_pile[-1].rank != PlayingCard.ACE: return

        foundation_pile.append(tableau_pile.pop())
        if len(tableau_pile) != 0 and not tableau_pile[-1].front_shown:
            tableau_pile[-1].front_shown = True
            self.point += 10

        self.move_count += 1

    def swap_talon_to_foundation(self, foundation_pile: list):
        self.swap_tableau_to_foundation(self.talon_pile, foundation_pile)

    def swap_foundation_to_tableau(self, foundation_pile: list, tableau_pile: list):
        self.swap_tableau_to_tableau(foundation_pile, tableau_pile, -1)
