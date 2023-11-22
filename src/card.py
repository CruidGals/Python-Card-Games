import pygame
from pygame import Vector2
import os

class Deck:
    def __init__(self) -> None:
        #Initialize all cards in one linese
        self.deck = [Card(rank, suit) for suit in range(13,18) for rank in range(1,14)]
        self.deck_layered_updates = pygame.sprite.LayeredUpdates(self.deck)

class Card(pygame.sprite.Sprite):

    #----constants----#

    #Numbers (Ranks)
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    #Suits
    HEART = 14
    DIAMOND = 15
    CLUB = 16
    SPADE = 17

    def __init__(self, rank, suit, pos=Vector2(0,0)) -> None:
        self.pos = pos
        self.rank = rank
        self.suit = suit
        self._layer = 0

        self.update_image()
        self.image_width, self.image_height = self.image.get_size()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image_width, self.image_height)

    def update_image(self):
        if self.suit == Card.HEART:
            suit_str = 'hearts'
        elif self.suit == Card.DIAMOND:
            suit_str = 'diamonds'
        elif self.suit == Card.CLUB:
            suit_str = 'clubs'
        else:
            suit_str = 'spades' #Makes sure suit_str gets a value no matter what

        if self.rank == Card.ACE:
            rank_str = 'A'
        elif self.rank == Card.TEN:
            rank_str = '10'
        elif self.rank == Card.JACK:
            rank_str = 'J'
        elif self.rank == Card.QUEEN:
            rank_str = 'Q'
        elif self.rank == Card.KING:
            rank_str = 'K'
        else:
            rank_str = '0{}'.format(self.rank)

        self.image = self.image = pygame.image.load(os.path.join('resources', 'cards', 'card_{}_{}.png'.format(suit_str, rank_str))).convert_alpha()
    
    def update_rect(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image_width, self.image_height)

    
