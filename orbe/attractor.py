
import pygame
import numpy as np


class Attractor:

    def __init__(self, name, color='#bb2011', mass=10**15, position=[0,0]):
        self.name = name
        self.color = pygame.Color(color)
        self.mass = mass
        self.position = np.array(position, dtype=np.float64)

        self.particles = []