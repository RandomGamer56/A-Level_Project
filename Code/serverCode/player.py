import pygame

class Player():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)

    def updatePlayer(self,my_dict):
        for key,value in my_dict.items:
            setattr(self, key, value)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def __iter__(self):
        yield "x", self.x
        yield "y", self.y
        yield "height", self.height
        yield "width", self.width
        yield "colour", self.colour
        yield "rect", self.rect
        yield "vel", self.vel
