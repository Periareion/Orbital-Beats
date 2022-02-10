
import pygame
import numpy as np


class System:

    def __init__(self, name, color='#bb2011', mass=10**15, position=[0,0]):
        self.name = name
        self.attractor_color = pygame.Color(color)
        self.attractor_mass = mass
        self.attractor_position = np.array(position, dtype=np.float64)

        self.particles = []