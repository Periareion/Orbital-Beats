import pygame

class Environment:

    def __init__(self, start_time):
        self.start_time = start_time
        self.time = start_time
        self.G = 6.6743*10**-11
        
        self.attractors = []
