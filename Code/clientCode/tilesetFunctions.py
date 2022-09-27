import pygame
import os
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))

def load_tileset(filename, width, height):
    path = os.getcwd()[:-11]
    path = path+"/Graphics/Tileset/"
    finalFile = path+filename
    whole_tileset = pygame.image.load(finalFile).convert()
    whole_tileset_width, whole_tileset_height = whole_tileset.get_size()
    tileset_collect = []
    for tile_x in range(0, whole_tileset_width // width):
        line = []
        for tile_y in range(0, whole_tileset_height // height):
            single_tile = (tile_x * width, tile_y * height, width, height)
            line.append(whole_tileset.subsurface(single_tile))
        tileset_collect.append(line)
    return tileset_collect

def draw_background(screen, tile_img, field_rect):
    counter = 0
    for tile in tile_img:
        counter += 1
        if counter == 3:
            break
        tile_rect = tile.get_rect()
        for y in range(0,400,32):
            for x in range(0,600,32):
                screen.blit(tile, (x, y))


