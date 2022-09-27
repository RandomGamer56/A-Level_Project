import os
import sys
import pygame
from pygame.locals import *
from tilesetFunctions import *
from tilesetConstants import *

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
D_GREEN = (0, 150, 0)
GREY = (120, 120, 120)
YELLOW = (240, 230, 140)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

done = False

counter = 0

clock = pygame.time.Clock()

tileset_collect = load_tileset("pipo-map001_at.png", 32, 32)

class TileObject(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        super().__init__()
        self.colour = (255, 255, 255)
        self.image = pygame.Surface([32, 32])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.value = value
        self.multiplyer = 8
        self.update_colour()

    def update_colour(self):
        def update_size(image, multiplyer):
            new_image = pygame.transform.scale(image, (multiplyer, multiplyer))
            return new_image
        # if self.value > 150:
            # self.colour = WHITE
        if self.value > 150:
             # self.colour = GREY
            temp_image = tileset_collect[14]
            temp_postion = self.rect.topleft
            self.image = temp_image[19]
            self.image = update_size(self.image,self.multiplyer)
            self.rect = self.image.get_rect()
            self.rect.topleft = temp_postion
        elif self.value > 120:
             # self.colour = GREY
            temp_image = tileset_collect[6]
            temp_postion = self.rect.topleft
            self.image = temp_image[25]
            self.image = update_size(self.image,self.multiplyer)
            self.rect = self.image.get_rect()
            self.rect.topleft = temp_postion
        elif self.value > 80:
            # self.colour = D_GREEN
            temp_image = tileset_collect[6]
            temp_postion = self.rect.topleft
            self.image = temp_image[7]
            self.image = update_size(self.image,self.multiplyer)
            self.rect = self.image.get_rect()
            self.rect.topleft = temp_postion
        elif self.value > 50:
            # self.colour = GREEN
            temp_image = tileset_collect[6]
            temp_postion = self.rect.topleft
            self.image = temp_image[1]
            self.image = update_size(self.image,self.multiplyer)
            self.rect = self.image.get_rect()
            self.rect.topleft = temp_postion
        elif self.value > 30:
            self.colour = YELLOW
            temp_image = tileset_collect[14]
            temp_postion = self.rect.topleft
            self.image = temp_image[7]
            self.image = update_size(self.image,self.multiplyer)
            self.rect = self.image.get_rect()
            self.rect.topleft = temp_postion
        else:
            # self.colour = BLUE
            temp_image = tileset_collect[14]
            temp_postion = self.rect.topleft
            self.image = temp_image[13]
            self.image = update_size(self.image,self.multiplyer)
            self.rect = self.image.get_rect()
            self.rect.topleft = temp_postion

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # if self.image == tileset_collect[6][1] or \
        #         self.image == tileset_collect[14][7] or \
        #         self.image == tileset_collect[14][13]or \
        #         self.image == tileset_collect[6][25] or \
        #         self.image == tileset_collect[6][7] or \
        #         self.image == tileset_collect[14][19]:
        #     screen.blit(self.image,self.rect.topleft)
        # else:
        #     pygame.draw.rect(screen, self.colour, self.rect, 0)

def drawMap(gameMap):
    global done

    tile_list = []
    multiplyer = 128
    for y in range(0, len(gameMap.map)):
        for x in range(0, len(gameMap.map[y])):
            tile_list.append(TileObject(x * multiplyer, y * multiplyer, gameMap.map[y][x]))
            index = (y * 50) + x
            tile_list[index].multiplyer = multiplyer

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)

        for i in range(0, len(tile_list)):
            tile_list[i].update_colour()
            tile_list[i].draw(screen)

        clock.tick(60)
    pygame.quit()
