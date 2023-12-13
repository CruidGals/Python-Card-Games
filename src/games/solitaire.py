import pygame
import os
from card import Deck, PlayingCard

'''
TODO Stub:
    - When picking a card, use the "in" operator to detect which pile it is in.
'''

class Solitaire:
    def __init__(self, screen_size) -> None:
        self.logic = SolitaireGameLogic()

        scale = min(screen_size[0]/7, screen_size[1]/5.5)
        self.logic.deck.resize_all_cards(scale)

        self.setup_collision_rects(screen_size)

        #For moving card
        self.selected_card = None
        self.selected_pile = None
    
    # Should only be called on mouse clicked
    def select_card(self, pos):
        for card in self.logic.deck.deck:
            if card.rect.collidepoint(pos):
                self.selected_pile = self.logic.pile_from_card(card)
                if card.front_shown: 
                    self.selected_card = card
                break
    
    # Should only be called on mouse held
    def move_card(self, pos):
        pass
    
    # Should only be called on mouse release
    def release_card(self, pos):
        if self.selected_pile == None: return
        
        for collision_rect in self.all_collision_rects():
            if collision_rect.collidepoint(pos):

                if self.selected_card == None: #Semi-guard clause
                    if self.selected_pile is self.logic.stockpile and self.selected_pile is self.pile_from_collision_rect(collision_rect): # if the pile is stockpile
                        self.logic.swap_stockpile_to_talon()
                    break

                if self.selected_pile is self.pile_from_collision_rect(collision_rect): #If origin piles and released piles equal
                    pass #TODO Make automatic card player
                elif collision_rect in self.tableau_pile_collision_rects:
                    tableau_pile = self.pile_from_collision_rect(collision_rect)

                    if self.selected_pile is self.logic.talon_pile:
                        self.logic.swap_talon_to_tableau(tableau_pile)
                    elif self.selected_pile in self.logic.tableau:
                        self.logic.swap_tableau_to_tableau(self.selected_pile, tableau_pile)
                    elif self.selected_pile in self.logic.foundation_piles:
                        self.logic.swap_foundation_to_tableau(self.selected_pile, tableau_pile)
                
                elif collision_rect in self.foundation_pile_collision_rects:
                    foundation_pile = self.pile_from_collision_rect(collision_rect)

                    if self.selected_pile in self.logic.tableau:
                        self.logic.swap_tableau_to_foundation(self.selected_pile, foundation_pile)
                
                break
            

        self.selected_card = None
        self.selected_pile = None

    #-----------------Collision Functions-----------------#
    # Will help with accurate detection of tableau pile placement
    # Use index() to correctly match tableau or foundation collision rects with corresponding pile
    def setup_collision_rects(self, screen_size):
        center = (screen_size[0]/2, screen_size[1]/2)
        pos = [center[0] - 3.5 * self.logic.deck.card_size, center[1] - 2.5 * self.logic.deck.card_size]
        
        self.stockpile_collision_rect = pygame.Rect(pos[0], pos[1], self.logic.deck.card_size, self.logic.deck.card_size)
        pos[0] += self.logic.deck.card_size
        self.talon_collision_rect = pygame.Rect(pos[0]. pos[1], self.logic.deck.card_size, self.logic.deck.card_size)
        pos[0] += 2 * self.logic.deck.card_size
        self.foundation_pile_collision_rects = [pygame.Rect(pos[0] + i * self.logic.deck.card_size, pos[1], self.logic.deck.card_size, self.logic.deck.card_size) for i in range(4)]
        pos = [center[0] - 3.5 * self.logic.deck.card_size, center[1] - 1.25 * self.logic.deck.card_size]
        self.tableau_pile_collision_rects = [pygame.Rect(pos[0] + i * self.logic.deck.card_size, pos[1], self.logic.deck.card_size, self.logic.deck.card_size * 7) for i in range(7)]
    
    def all_collision_rects(self) -> list:
        all_rects = [self.stockpile_collision_rect, self.talon_collision_rect]
        all_rects.extend(self.tableau_pile_collision_rects, self.foundation_pile_collision_rects)

        return all_rects
    
    def pile_from_collision_rect(self, collision_rect):
        if collision_rect not in self.all_collision_rects(): return

        if collision_rect is self.stockpile_collision_rect:
            return self.logic.stockpile
        elif collision_rect is self.talon_collision_rect:
            return self.logic.talon_pile
        elif collision_rect in self.tableau_pile_collision_rects:
            return self.logic.tableau[self.tableau_pile_collision_rects.index(collision_rect)]
        else: #if collision_rect ins foundation piles
            return self.logic.foundation_piles[self.foundation_pile_collision_rects.index(collision_rect)]

    #-----------------Drawing Functions-----------------#

    def setup_layered_groups(self):
        self.groups = [
            pygame.sprite.LayeredUpdates(self.logic.stockpile),
            pygame.sprite.LayeredUpdates(self.logic.talon_pile),
        ] + [pygame.sprite.LayeredUpdates(pile) for pile in self.logic.tableau] + [pygame.sprite.LayeredUpdates(pile) for pile in self.logic.tableau]

    def setup_solitare(self, screen_size):

        center = (screen_size[0]/2, screen_size[1]/2)
        pos = [center[0] - 3.5 * self.logic.deck.card_size, center[1] - 2.5 * self.logic.deck.card_size]
        
        self.stockpile_collision_rect = pygame.Rect(pos[0], pos[1], self.logic.deck.card_size, self.logic.deck.card_size)
        pos[0] += self.logic.deck.card_size
        self.talon_collision_rect = pygame.Rect(pos[0]. pos[1], self.logic.deck.card_size, self.logic.deck.card_size)
        pos[0] += 2 * self.logic.deck.card_size
        self.foundation_pile_collision_rects = [pygame.Rect(pos[0] + i * self.logic.deck.card_size, pos[1], self.logic.deck.card_size, self.logic.deck.card_size) for i in range(4)]
        pos = [center[0] - 3.5 * self.logic.deck.card_size, center[1] - 1.25 * self.logic.deck.card_size]
        self.tableau_pile_collision_rects = [pygame.Rect(pos[0] + i * self.logic.deck.card_size, pos[1], self.logic.deck.card_size, self.logic.deck.card_size * 7) for i in range(7)]

    def draw_solitaire(self, screen):
        #Start the "drawing" position at the top right corner
        center = (screen.get_size()[0]/2, screen.get_size()[1]/2)
        pos = [center[0] - 3.5 * self.logic.deck.card_size, center[1] - 2.5 * self.logic.deck.card_size]

        self.draw_stockpile_and_talon(screen, pos)
        pos[0] += 3 * self.logic.deck.card_size
        self.draw_foundation_piles(screen, pos)
        pos = [center[0] - 3.5 * self.logic.deck.card_size, center[1] - 1.25 * self.logic.deck.card_size]
        self.draw_tableau(screen, pos)

    def draw_tableau_pile(self, screen, tableau_pile, collision_rect, starting_pos):
        pos = starting_pos[:]
        for card in tableau_pile:
            card.draw_card(screen, pos)
            pos[1] = card.front_image.get_size()[1] / 4 + pos[1]

    def draw_tableau(self, screen, starting_pos):
        pos = starting_pos[:]
        for i in range(7):
            self.draw_tableau_pile(screen, self.logic.tableau[i], self.tableau_pile_collision_rects[i], pos)
            pos[0] = pos[0] + self.logic.deck.card_size #Multiply by 1.2 to add more spacing

    def draw_stockpile_and_talon(self, screen, starting_pos):
        pos = starting_pos[:]
        if len(self.logic.stockpile) != 0: self.logic.stockpile[-1].draw_card(screen, pos)
        if len(self.logic.talon_pile) != 0: self.logic.talon_pile[-1].draw_card(screen, (pos[0] + self.logic.deck.card_size, pos[1]))

    def draw_foundation_piles(self, screen, starting_pos):
        pos = starting_pos[:]

        for pile in self.logic.foundation_piles:
            pile[-1].draw_card(screen, pos) if len(pile) != 0 else self.logic.deck.placeholder_card.draw_card(screen, pos)
            pos[0] = pos[0] + self.logic.deck.card_size
        

#Will include no pygame
class SolitaireGameLogic:
    def __init__(self) -> None:
        self.deck = Deck()
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

        for i in range(1, 8): #Tableau col marked as i-1 (array indexing)
            for j in range(i): #Range of i because of solitaire shtife
                card = self.stockpile.pop()
                if j != i-1: card.front_shown = False
        
                self.tableau[i-1].append(card)

        #Flip all cards in stockpile
        for card in self.stockpile:
            card.front_shown = False
    
    #returns piles that has card
    def pile_from_card(self, card):
        all_piles = [self.stockpile, self.talon_pile]
        all_piles.extend(self.tableau + self.foundation_piles)
        for pile in all_piles:
            if len(pile) != 0 and card in pile:
                return pile

    def is_game_won(self):
        return len(self.foundation_piles[0]) + len(self.foundation_piles[1]) + len(self.foundation_piles[2]) + len(self.foundation_piles[3]) == 52

    #---------------- Swapping Functions ----------------#

    #If has two piles of unknown identity, use this
    def swap_piles_unknown_identity(self, pile1, pile2):
        if pile1 in self.tableau:
            if pile2 in self.tableau:
                self.swap_tableau_to_tableau(pile1, pile2)
            if pile2 in self.foundation_piles:
                self.swap_tableau_to_foundation(pile1, pile2)
        elif pile1 in self.foundation_piles:
            if pile2 in self.tableau:
                self.swap_foundation_to_tableau(pile1, pile2)
        elif pile1 is self.stockpile:
            if pile2 is self.talon_pile:
                self.swap_stockpile_to_talon()
        elif pile1 is self.talon_pile:
            if pile2 in self.tableau:
                self.swap_talon_to_tableau(pile2)
            if pile2 in self.foundation_piles:
                self.swap_talon_to_foundation(pile2)


    # In solitaire, to shift from tableau piles you must satisfy these conditions:
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

        new_pile.extend(orig_pile[idx:])
        del orig_pile[idx:]
        if len(orig_pile) != 0 and not orig_pile[-1].front_shown:
            orig_pile[-1].front_shown = True
            self.points += 5

        self.move_count += 1

    # Cards from stockpile fall into talon pile until there is no more cards
    # in stockpile, where which all the talon pile cards go back to stockpile.
    def swap_stockpile_to_talon(self):
        if len(self.stockpile) == 0:
            if len(self.talon_pile) == 0: return # Makes sure if no list out of bounds error if stockpile is exhausted
            self.stockpile = self.talon_pile[::-1]

            for card in self.stockpile:
                card.front_shown = False

            self.talon_pile.clear()
        else:
            self.talon_pile.append(self.stockpile.pop())
            self.talon_pile[-1].front_shown = True
        
        self.move_count += 1

    def swap_talon_to_tableau(self, tableau_pile: list):
        if len(self.talon_pile) == 0: return

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
        if len(self.talon_pile) != 0: self.swap_tableau_to_foundation(self.talon_pile, foundation_pile)

    def swap_foundation_to_tableau(self, foundation_pile: list, tableau_pile: list):
        self.swap_tableau_to_tableau(foundation_pile, tableau_pile, -1)
