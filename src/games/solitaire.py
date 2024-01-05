import pygame
import os
from card import *

'''
TODO Stub:
    - When picking a card, use the "in" operator to detect which pile it is in.
'''

class Solitaire:
    def __init__(self, screen_size) -> None:
        self.logic = SolitaireGameLogic()

        self._center = (screen_size[0]/2, screen_size[1]/2)

        scale = min(screen_size[0]/7, screen_size[1]/5.5)
        self.logic.deck.resize_all_cards(scale)

        self.update_all_card_positions()
        self.setup_collision_rects()

        #For moving card
        self._selected_card = None
        self._selected_pile = None
        self._previous_pos = None
    
    # Should only be called on mouse clicked
    def select_card(self, pos):
        for card in self.logic.deck.deck:
            if card.rect.collidepoint(pos):
                if card.front_shown: 
                    self._selected_card = card
                break
        
        for collision_rect in self.all_collision_rects():
            if collision_rect.collidepoint(pos):
                self._selected_pile = self.pile_from_collision_rect(collision_rect)
    
    # Should only be called on mouse held
    def move_card(self, pos):
        if self._selected_card == None: return

        delta = [pos[0] - self._previous_pos[0], pos[1] - self._previous_pos[1]] if self._previous_pos != None else [0,0]
        self._selected_card.update_rect([self._selected_card.pos[0] + delta[0], self._selected_card.pos[1] + delta[1]])
        self._previous_pos = pos[:]
    
    # Should only be called on mouse release
    def release_card(self, pos):
        if self._selected_pile == None: return

        target_pile = None
        
        for collision_rect in self.all_collision_rects():
            if collision_rect.collidepoint(pos):

                if self._selected_card == None: #Semi-guard clause
                    if self._selected_pile is self.logic.stockpile: # if the pile is stockpile
                        target_pile = self.logic.talon_pile
                        self.logic.swap_stockpile_to_talon()

                        if len(self.logic.talon_pile) != 0: 
                            self._selected_card = self.logic.talon_pile[-1]
                        else:
                            self.group_from_pile(self.logic.talon_pile).empty()
                            self.group_from_pile(self.logic.stockpile).add(self.logic.stockpile)
                            self.update_pile_card_positions(self.logic.stockpile[0])

                    break

                if self._selected_pile is self.pile_from_collision_rect(collision_rect): #If origin piles and released piles equal
                    pass #TODO Make automatic card player
                elif collision_rect in self._tableau_pile_collision_rects:
                    target_pile = self.pile_from_collision_rect(collision_rect)

                    if self._selected_pile is self.logic.talon_pile:
                        self.logic.swap_talon_to_tableau(target_pile)
                    elif self._selected_pile in self.logic.tableau:
                        self.logic.swap_tableau_to_tableau(self._selected_pile, target_pile, -1)
                    elif self._selected_pile in self.logic.foundation_piles:
                        self.logic.swap_foundation_to_tableau(self._selected_pile, target_pile)
                
                elif collision_rect in self._foundation_pile_collision_rects:
                    target_pile = self.pile_from_collision_rect(collision_rect)

                    if self._selected_pile in self.logic.tableau:
                        self.logic.swap_tableau_to_foundation(self._selected_pile, target_pile)
                    elif self._selected_pile is self.logic.talon_pile:
                        self.logic.swap_talon_to_foundation(self, target_pile)
                
                break
        
        if self._selected_card: 
            if target_pile and target_pile != self._selected_pile:
                self._selected_card.kill()
                self.group_from_pile(target_pile).add(self._selected_card)
            self.update_pile_card_positions(self._selected_card)

        self._selected_card = None
        self._selected_pile = None
        self._previous_pos = None

    #-----------------Collision Functions-----------------#
    # Will help with accurate detection of tableau pile placement
    # Use index() to correctly match tableau or foundation collision rects with corresponding pile
    def setup_collision_rects(self):
        pos = [self._center[0] - 3.5 * self.logic.deck.card_size, self._center[1] - 2.5 * self.logic.deck.card_size]
        
        self._stockpile_collision_rect = pygame.Rect(pos[0], pos[1], self.logic.deck.card_size, self.logic.deck.card_size)
        pos[0] += self.logic.deck.card_size
        self._talon_collision_rect = pygame.Rect(pos[0], pos[1], self.logic.deck.card_size, self.logic.deck.card_size)
        pos[0] += 2 * self.logic.deck.card_size
        self._foundation_pile_collision_rects = [pygame.Rect(pos[0] + i * self.logic.deck.card_size, pos[1], self.logic.deck.card_size, self.logic.deck.card_size) for i in range(4)]
        pos = [self._center[0] - 3.5 * self.logic.deck.card_size, self._center[1] - 1.25 * self.logic.deck.card_size]
        self._tableau_pile_collision_rects = [pygame.Rect(pos[0] + i * self.logic.deck.card_size, pos[1], self.logic.deck.card_size, self.logic.deck.card_size * 7) for i in range(7)]
    
    def all_collision_rects(self) -> list:
        all_rects = [self._stockpile_collision_rect, self._talon_collision_rect]
        all_rects.extend(self._tableau_pile_collision_rects + self._foundation_pile_collision_rects)

        return all_rects
    
    def pile_from_collision_rect(self, collision_rect):
        if collision_rect not in self.all_collision_rects(): return

        if collision_rect is self._stockpile_collision_rect:
            return self.logic.stockpile
        elif collision_rect is self._talon_collision_rect:
            return self.logic.talon_pile
        elif collision_rect in self._tableau_pile_collision_rects:
            return self.logic.tableau[self._tableau_pile_collision_rects.index(collision_rect)]
        else: #if collision_rect ins foundation piles
            return self.logic.foundation_piles[self._foundation_pile_collision_rects.index(collision_rect)]

    #-----------------Card Position Updating Functions-----------------#
    # Sprites in pygame takes certain x and y positions from its rect to draw the image
    # These functions update the rect with new positions so that the card draws in the correct place

    def update_all_card_positions(self):
        self.setup_layered_groups()

        pos = [self._center[0] - 3.5 * self.logic.deck.card_size, self._center[1] - 2.5 * self.logic.deck.card_size]
        
        self._update_stockpile_cards_pos(pos)
        pos[0] += self.logic.deck.card_size
        self._update_talon_pile_cards_pos(pos)
        pos[0] += 2 * self.logic.deck.card_size
        self._update_placeholder_card_pos(pos)
        self._update_foundation_pile_cards_pos(pos, self.logic.foundation_piles)
        pos = [self._center[0] - 3.5 * self.logic.deck.card_size, self._center[1] - 1.25 * self.logic.deck.card_size]
        self._update_tableau_pile_cards_pos(pos, self.logic.tableau)

    #Updates all card positions in a pile
    def update_pile_card_positions(self, card):
        pile = self.logic.pile_from_card(card)

        pos = [self._center[0] - 3.5 * self.logic.deck.card_size, self._center[1] - 2.5 * self.logic.deck.card_size]

        if pile is self.logic.stockpile:
            self._update_stockpile_cards_pos(pos)
        pos[0] += self.logic.deck.card_size
        if pile is self.logic.talon_pile:
            self._update_talon_pile_cards_pos(pos)
        pos[0] += 2 * self.logic.deck.card_size
        if pile in self.logic.foundation_piles:
            self._update_foundation_pile_cards_pos(pos, [pile])
        pos = [self._center[0] - 3.5 * self.logic.deck.card_size, self._center[1] - 1.25 * self.logic.deck.card_size]
        if pile in self.logic.tableau:
            self._update_tableau_pile_cards_pos(pos, [pile])

    def _update_stockpile_cards_pos(self, pos):
        for card in self.logic.stockpile:
            card.update_rect(pos[:])
    
    def _update_talon_pile_cards_pos(self, pos):
        for card in self.logic.talon_pile:
            card.update_rect(pos[:])
    
    def _update_placeholder_card_pos(self, pos):
        for card in self.placeholder_group.sprites():
            card.update_rect(pos)
            pos[0] += self.logic.deck.card_size
        pos[0] -= 4 * self.logic.deck.card_size #Resets the position

    def _update_foundation_pile_cards_pos(self, pos, target_piles):
        for pile in self.logic.foundation_piles:
            if pile not in target_piles: #Function used to enhance performace (so positions of every card aren't updated)
                pos[0] += self.logic.deck.card_size
                continue

            for card in pile:
                card.update_rect(pos[:])
            pos[0] += self.logic.deck.card_size
        
    def _update_tableau_pile_cards_pos(self, pos, target_piles):
        for pile in self.logic.tableau: #Update positions for cards in tableau piles
            if pile not in target_piles: #Function used to enhance performace (so positions of every card aren't updated)
                pos[0] += self.logic.deck.card_size
                continue

            for card in pile:
                card.update_rect(pos[:])
                pos[1] += self.logic.deck.card_size / 4
            pos = [pos[0] + self.logic.deck.card_size, pos[1] - (len(pile) * (self.logic.deck.card_size / 4))]

    #-----------------Drawing Functions-----------------#

    def setup_layered_groups(self):
        self.groups = [
            pygame.sprite.LayeredUpdates(self.logic.stockpile),
            pygame.sprite.LayeredUpdates(self.logic.talon_pile),
        ] + [pygame.sprite.LayeredUpdates(pile) for pile in self.logic.tableau] \
          + [pygame.sprite.LayeredUpdates(pile) for pile in self.logic.foundation_piles]
        
        self.placeholder_group = pygame.sprite.LayeredUpdates([Card(front_image=pygame.image.load(os.path.join('resources', 'cards', 'card_placeholder.png'))) for i in range(4)])

        for card in self.placeholder_group.sprites():
            card.resize_card(self.logic.deck.card_size)
    
    # The function form get_all_piles() have the same indexing as the groups
    def group_from_pile(self, pile):
        return self.groups[self.logic.get_all_piles().index(pile)]

    def draw_elements(self, screen):
        self.placeholder_group.draw(screen)
        for group in self.groups: group.draw(screen)

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
                else: card.front_shown = True # Corrects error in front_shown property
        
                self.tableau[i-1].append(card)

        #Flip all cards in stockpile
        for card in self.stockpile:
            card.front_shown = False
    
    def get_all_piles(self):
        return [self.stockpile, self.talon_pile] + self.tableau + self.foundation_piles

    #returns piles that has card
    def pile_from_card(self, target_card):
        all_piles = [self.stockpile, self.talon_pile] + self.tableau + self.foundation_piles
        for pile in all_piles:
            for card in pile: 
                if card is target_card: return pile

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
            self.points += 10

        self.move_count += 1

    def swap_talon_to_foundation(self, foundation_pile: list):
        if len(self.talon_pile) != 0: self.swap_tableau_to_foundation(self.talon_pile, foundation_pile)

    def swap_foundation_to_tableau(self, foundation_pile: list, tableau_pile: list):
        self.swap_tableau_to_tableau(foundation_pile, tableau_pile, -1)
