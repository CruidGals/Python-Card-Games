import pygame
from pygame import Vector2
import numpy as np
import os

class Deck:
    def __init__(self) -> None:
        #Initialize all cards in one linese
        self.deck = np.array([PlayingCard(rank, suit) for suit in range(13,18) for rank in range(1,14)])

    def shuffle_deck(self):
        np.random.shuffle(self.deck)

class Card(pygame.sprite.Sprite):
    def __init__(self, pos=Vector2(0,0), front_image=None, back_image=None) -> None:
        self.pos = pos
        self.front_image = front_image
        self.back_image = back_image

        self.front_shown = True

        self._layer = 0
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.front_image.get_size()[0], self.front_image.get_size()[1]) if front_image else None

    def scale_card(self, scale):
        image_width, image_height = self.front_image.get_size()
        self.front_image = pygame.transform.scale(self.front_image, (scale * image_width, scale * image_height))
        self.back_image = pygame.transform.scale(self.back_image, (scale * image_width, scale * image_height))

    def update_rect(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.front_image.get_size()[0], self.front_image.get_size()[1]) if self.front_image else None

    def draw_card(self, screen, pos):
        screen.blit(self.front_image, pos) if self.front_shown else screen.blit(self.back_image, pos)

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
        self.front_image = self.get_image()
        self.back_image = pygame.image.load(os.path.join('resources', 'cards', 'card_back.png')).convert_alpha()

        self.scale_card(4)

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
