import pygame
import numpy as np
import os, math
from card import Deck, Card
from games.solitaire import Solitaire

class Game:
    def __init__(self, screen_size) -> None:
        self.select_current_game(screen_size)
        self.background_image = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'background', 'grass.jpg')).convert_alpha(), (256, 256)) #Scale to add 8-bit feeling

    def select_current_game(self, screen_size):
        #Will allow selection of a game, right now only contains solitare
        self.selected_game = Solitaire(screen_size)

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

    def select_card(self, pos):
        self.selected_game.select_card(pos)

    def move_card(self, pos):
        self.selected_game.move_card(pos)

    def release_card(self, pos):
        self.selected_game.release_card(pos)

    def draw_elements(self, screen):
        self.draw_background(screen)
        self.selected_game.draw_elements(screen)

def main():
    pygame.init()
    screen_size = (900, 600)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    game = Game(screen_size)

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.select_card(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                game.release_card(event.pos)
            if pygame.mouse.get_pressed()[0]:
                game.move_card(event.pos)

        screen.fill('Teal')
        game.draw_elements(screen)
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()