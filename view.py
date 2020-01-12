import pygame
import numpy as np

class RectView(object):
    side_length = 90
    radius = 30

    def __init__(self, x, y, val=-1):
        self.x = x
        self.y = y
        self.val = val
        self.center = (x + int(RectView.side_length/2), y + int(RectView.side_length/2))
        self.coordinates = [(x, y), (x + RectView.side_length, y), (x + RectView.side_length, y + RectView.side_length), (x, y + RectView.side_length)]

    def draw(self, screen):
        pygame.draw.polygon(screen, (52, 154, 52), self.coordinates)
        pygame.draw.polygon(screen, (188, 164, 145), self.coordinates, 2)
        if self.val == 0:
            pygame.draw.circle(screen, (255, 255, 255), self.center, RectView.radius)
        elif self.val == 1:
            pygame.draw.circle(screen, (0, 0, 0), self.center, RectView.radius)


    def __repr__(self):
        return f"x: {self.x}  y: {self.y}"