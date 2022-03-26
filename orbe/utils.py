
import sys, os

import math
import time
import random
import json
import ast

import numpy as np
import pygame

from orbe.particle import Particle
from orbe.attractor import Attractor
from orbe.environment import Environment

from orbe.settings import visual, width, height


def half_screen():
    return (width()/2, height()/2)


def screen_position(true_position, offset=[0,0], scale=1):
    hs = half_screen()
    return (true_position[0]/scale + hs[0] + offset[0], - true_position[1]/scale + hs[1] + offset[1])


def true_position(screen_position, offset=[0,0], scale=1):
    hs = half_screen()
    return ((screen_position[0] - hs[0] - offset[0])*scale, - (screen_position[1] - hs[1] - offset[1])*scale)


left_click = 0
middle_click = 1
right_click = 2

mouse_hold_tracker = {
    0: False,
    1: False,
    2: False,
}

mouse_click_tracker = {
    0: False,
    1: False,
    2: False,
}

key_hold_tracker = {
    pygame.K_d: False,
    pygame.K_r: False,
    pygame.K_s: False,
    pygame.K_LCTRL: False,
    pygame.K_DELETE: False,
}

key_down_tracker = key_hold_tracker.copy()


def update_mouse_state():
    current = pygame.mouse.get_pressed()

    for n in range(3):
        
        if mouse_hold_tracker[n]:
            mouse_click_tracker[n] = False
        elif current[n]:
            mouse_click_tracker[n] = True

    for n, button_state in enumerate(current):
        mouse_hold_tracker[n] = button_state


mouse_position = {}

def update_mouse_position():
    mouse_position['x'], mouse_position['y'] = mouse_position['pos'] = pygame.mouse.get_pos()


def update_key_state(events):
    for key in key_down_tracker.keys():
        key_down_tracker[key] = False

    for event in events:
        if event.type == pygame.KEYDOWN:
            for key in key_hold_tracker.keys():
                if key == event.key:
                    key_hold_tracker[key] = True
                    key_down_tracker[key] = True
        elif event.type == pygame.KEYUP:
            for key in key_hold_tracker.keys():
                if key == event.key:
                    key_hold_tracker[key] = False


def in_and_true(key, dict):
    if (key in dict) and (dict[key]):
        return True


def random_hex(n):
    return ''.join(random.sample('0123456789abcdef',n))
    #return hex(random.randint(0,16**n-1)).replace('0x','').zfill(n)
    #return ''.join([random.choice('0123456789abcdef')for _ in range(n)])


def pgColor_to_hex(color):
    return '#%02x%02x%02x' % (color.r, color.g, color.b)


def calculate_columns(window_dimensions, box_dimensions, side_margin):
    window_width, window_height = window_dimensions
    box_width, box_height = box_dimensions

    usable_width = window_width - 2 * side_margin
    columns = usable_width // box_width
    try:
        distance_between_boxes = (usable_width - box_width * columns) / (columns - 1)
    except ZeroDivisionError:
        distance_between_boxes = 0

    return {'usable_width': usable_width, 'columns': columns, 'distance_between_boxes': distance_between_boxes}


from orbe.json_utils import *


def update_particles(environment, path_surface):
    for attractor in environment.attractors:
        for particle in attractor.particles:

            old_position = particle.position
            particle.update_position(time.perf_counter(), environment.start_time)

            screen_start = screen_position(old_position)
            screen_end = screen_position(particle.position)

            if sum((x**2 for x in (screen_start[i]-screen_end[i] for i in range(2))))**0.5 < 24:
                pygame.draw.aaline(path_surface, particle.secondary_color,
                    screen_position(old_position),
                    screen_position(particle.position))


from pygame import gfxdraw

def draw_beat(environment, screen):

    for attractor in environment.attractors:
        #pygame.draw.circle(screen, attractor.color, screen_position(attractor.position), 7)
        gfxdraw.aacircle(screen, *[int(x+1) for x in screen_position(attractor.position)], 7, attractor.color)
        gfxdraw.filled_circle(screen, *[int(x+1) for x in screen_position(attractor.position)], 7, attractor.color)

        for particle in attractor.particles:
            pygame.draw.circle(screen, particle.color, [x+1 for x in screen_position(particle.position)], 4)
            #gfxdraw.aacircle(screen, *[int(x+1) for x in screen_position(particle.position)], 4, particle.color)
            #gfxdraw.filled_circle(screen, *[int(x+1) for x in screen_position(particle.position)], 4, particle.color)

            if particle.animations:
                frame = particle.animations[0]
                screen.blit(frame, screen_position(particle.position, (-frame.get_width()/2, -frame.get_height()/2)))
                particle.animations.pop(0)

def say_hi(button):
    print("Hi")


def draw_text(text, font, color, surface, x, y, position='center'):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()

    match position:
        case 'center':
            textrect.center = (x, y)
        case 'topleft':
            textrect.topleft = (x, y)

    surface.blit(textobj, textrect)


class Button:

    def __init__(
            self,
            text='Hi',
            function=say_hi,
            args={},
            rect_pos=(0,0),
            rect_dim=(0,0),
            primary_text_color=(159,159,159),
            secondary_text_color=(210,210,210),
            primary_color=(0,0,0),
            secondary_color=(16,16,32)
        ):

        self.default_args = {}

        self.text = text
        self.function = function
        self.args = self.default_args.copy(); self.args.update(args)
        self.rect_pos = rect_pos
        self.rect_dim = rect_dim
        self.primary_text_color = primary_text_color
        self.secondary_text_color = secondary_text_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color


def check_buttons(buttons, mouse_pos, mouse_click_tracker, screen, font, kht={}, kdt={}, allow_delete=False, update={}, name=None):
    _removed_indices = []
    for i in range(len(buttons)):
        button = buttons[i]
        button.rect = pygame.Rect(*screen_position(button.rect_pos), *button.rect_dim)
        if 'position' in button.args.keys():
            if button.args['position'] == 'topleft':
                pass
        else:
            button.rect.center = button.rect.topleft
        
        if button.rect.collidepoint(mouse_pos):
            text_color = button.secondary_text_color
            color = button.secondary_color

            if True in mouse_click_tracker.values():
                button.args.update({'mouse_clicks': mouse_click_tracker})
                return button.function(button)

            elif allow_delete and (in_and_true(pygame.K_LCTRL, kht) and in_and_true(pygame.K_DELETE, kdt)) and (button.text not in ['Space Beet', 'O', 'Solway', 'Solway Firth']):
                _removed_indices.append(i)
                update[name] = True

        else:
            text_color = button.primary_text_color
            color = button.primary_color

        pygame.draw.rect(screen, color, button.rect)
        draw_text(button.text, font, text_color, screen, *button.rect.center, 'center')

    # Reversed so as to not change the indices (they're already sorted)
    for i in reversed(_removed_indices):
        remove_beat(button.text)
        del buttons[i]


def increment_screen_size(button):

    args = button.args
    visual = args['visual']
    
    if args['mouse_clicks'][left_click]:
        visual['resolution_index'] = (visual['resolution_index'] + 1) % len(visual['resolutions'])
    elif args['mouse_clicks'][right_click]:
        visual['resolution_index'] = (visual['resolution_index'] - 1) % len(visual['resolutions'])
    size = width(), height()

    button.text = f'Screen size: {size[0]}x{size[1]}'

k = 0
def fade_path_surface(path_surface, interval):
    global k
    if not (k := k + 1) % interval:
        path_surface.fill(pygame.Color(255, 255, 255, 245), None, pygame.BLEND_RGBA_MULT)


def check_quit(events):
    
    for event in events:

        if event.type == pygame.QUIT:
            quit_all()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True


def back(button):
    button.args['situation'][button.args['current']] = False


def quit_all(button=None):
    pygame.quit()
    sys.exit()

##    cursor = pygame.SYSTEM_CURSOR_HAND
##    cursor = pygame.SYSTEM_CURSOR_ARROW
##    pygame.mouse.set_cursor(cursor)
