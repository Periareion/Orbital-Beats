
import pygame
from orbe.constants import CONSTS

simulation = {
    'paused': False,
    'FPS': 120,
    'delta_time': 1,
}

visual = {
    'FPS': 60,
    'scale': 1, # meters per pixel
    
    'resolution_index': 2,
    'resolutions': [
        (800,600),
        (960,540),
        (1080,720),
        (1280,720),
        (1366,768),
        (1600,900),
        (1920,1080)
    ],
}

def width():
    return visual['resolutions'][visual['resolution_index']][0]

def height():
    return visual['resolutions'][visual['resolution_index']][1]

COLORS = {
    'background': pygame.Color('#030712'),
    'empty': pygame.Color(0,0,0,0),
}

situation = {}

from orbe.modules import configurator as cfg

import os
os.path.abspath(os.path.join('..', os.getcwd()))

updated_settings = cfg.read_config('config.txt')
cfg.update_dictionaries(updated_settings, [CONSTS, simulation, visual, COLORS])

