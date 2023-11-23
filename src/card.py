import pygame
from pygame import Vector2
import os

class Deck:
    def __init__(self) -> None:
        #Initialize all cards in one linese
        self.deck = [PlayingCard(rank, suit) for suit in range(13,18) for rank in range(1,14)]

class Card(pygame.sprite.Sprite):
    def __init__(self, pos=Vector2(0,0), image=None) -> None:
        self.pos = pos
        self.image = image

        self._layer = 0

    def scale_image(self, scale):
        image_width, image_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (scale * image_width, scale * image_height))

class PlayingCard(Card):

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
        super(PlayingCard, self).__init__(pos)
        self.rank = rank
        self.suit = suit
        self.image = self.get_image()

        self.scale_image(4)

    def get_image(self):
        if self.suit == PlayingCard.HEART:
            suit_str = 'hearts'
        elif self.suit == PlayingCard.DIAMOND:
            suit_str = 'diamonds'
        elif self.suit == PlayingCard.CLUB:
            suit_str = 'clubs'
        else:
            suit_str = 'spades' #Makes sure suit_str gets a value no matter what

        if self.rank == PlayingCard.ACE:
            rank_str = 'A'
        elif self.rank == PlayingCard.TEN:
            rank_str = '10'
        elif self.rank == PlayingCard.JACK:
            rank_str = 'J'
        elif self.rank == PlayingCard.QUEEN:
            rank_str = 'Q'
        elif self.rank == PlayingCard.KING:
            rank_str = 'K'
        else:
            rank_str = '0{}'.format(self.rank)

        return pygame.image.load(os.path.join('resources', 'cards', 'card_{}_{}.png'.format(suit_str, rank_str))).convert_alpha()
