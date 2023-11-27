import pygame
import numpy as np
import os, math
from card import Deck, Card

class Game:
    def __init__(self, screen_height) -> None:
        self.deck = Deck(screen_height)
        self.random_card = np.random.choice(self.deck.deck)
        self.random_pos = (np.random.randint(0,400), np.random.randint(0,400))
        self.background_image = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'background', 'grass.jpg')).convert_alpha(), (256, 256)) #Scale to add 8-bit feeling

    def draw_background(self, screen):
        screenWidth, screenHeight = screen.get_size()
        imageWidth, imageHeight = self.background_image.get_size()
        
        # Calculate how many tiles we need to draw in x axis and y axis
        tilesX = math.ceil(screenWidth / imageWidth)
        tilesY = math.ceil(screenHeight / imageHeight)
        
        # Loop over both and blit accordingly
        for x in range(tilesX):
            for y in range(tilesY):
                screen.blit(self.background_image, (x * imageWidth, y * imageHeight))

    def draw_elements(self, screen):
        self.draw_background(screen)
        self.random_card.draw_card(screen, self.random_pos)

def main():
    pygame.init()
    screen_size = (1600, 900)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    game = Game(screen_size[1])

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('Teal')
        game.draw_elements(screen)
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()