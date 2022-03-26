import sys, os
import time
import warnings
import json

warnings.filterwarnings('ignore', '.*-2147417850*', )

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

from orbe.utils import *
from orbe.json_utils import *
from orbe.settings import simulation, visual, COLORS, width, height, situation, update
from orbe.environment import Environment

pygame.font.init()
title_font = pygame.font.Font('assets/fonts/ethnocentric rg.ttf', 60)
font = pygame.font.SysFont('Calibri', 28, True)

screen = pygame.display.set_mode((width(), height()))
pygame.display.set_caption('Orbital Beats')

clock = pygame.time.Clock()


def main():
    main_menu()


def main_menu():
    global screen
    path_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    environment = Environment(time.perf_counter())

    load_scenes_json(environment, 'O')

    buttons = [
        Button(
            'Beats',
            beats_menu, {},
            (0, 100),
            (300, 40),
            (159, 159, 159),
            (210, 210, 210),
            (0, 0, 0),
            (16, 16, 32),
        ),

        Button(
            'Options',
            options_menu, {},
            (0, 40),
            (300, 40),
            (159, 159, 159),
            (210, 210, 210),
            (0, 0, 0),
            (16, 16, 32),
        ),

        Button(
            'Quit',
            quit_all, {},
            (0, -20),
            (300, 40),
            (159, 159, 159),
            (210, 210, 210),
            (0, 0, 0),
            (64, 16, 16),
        ),
    ]

    situation['main_menu'] = True
    while situation['main_menu']:

        events = pygame.event.get()
        if check_quit(events): situation['main_menu'] = False

        update_mouse_position()
        update_mouse_state()
        update_key_state(events)

        screen.fill(COLORS['background'])
        draw_text('   rbital Beats', title_font, (255, 255, 255), screen, *screen_position((0, 220)), 'center')

        check_buttons(buttons, mouse_position['pos'], mouse_click_tracker, screen, font)

        if screen.get_size() != (size := (width(), height())):
            screen = pygame.display.set_mode((size))
            path_surface = pygame.Surface(size, pygame.SRCALPHA)

        update_particles(environment, path_surface)
        draw_beat(environment, screen)

        fade_path_surface(path_surface, 1)
        screen.blit(path_surface, (0,0))

        pygame.display.update()

        clock.tick(60)

    quit_all()


def beats_menu(button):
    global screen
    path_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    environment = Environment(time.perf_counter())

    beats_data = load_json('beats.json')

    buttons = [
        Button(
            'Back',
            back,
            {'situation': situation, 'current': 'beats_menu', 'position': 'topleft'},
            (-width()/2+visual['beats_menu_side_margin'], height()/2-36),
            (100, 60),
        ),
    ]


    beats_buttons = []

    update['beats_buttons'] = True

    def add_beats_list_buttons(buttons):
        all_beats = load_json('beats.json')
        columns = calculate_columns((width(), height()), visual['beats_menu_box_size'], visual['beats_menu_side_margin'])

        for n, beat_name in enumerate(all_beats.keys()):
            beat_dict = all_beats[beat_name]

            column = n % columns['columns']
            row = n // columns['columns']

            button = Button(
                beat_name,
                orbital_beats,
                {'beat': [beat_name], 'position': 'topleft', 'from_beats_menu': True, 'update': update},
                (
                    -width()/2 + visual['beats_menu_side_margin'] + column * (visual['beats_menu_box_size'][0] + columns['distance_between_boxes']),
                    height()/2 - (120 + row * (visual['beats_menu_box_size'][1] + 40)),
                ),
                visual['beats_menu_box_size'],
                primary_text_color=beat_dict[0]['Attractor']['color'],
            )

            buttons.append(button)

    situation['beats_menu'] = True
    while situation['beats_menu']:

        events = pygame.event.get()
        if check_quit(events): situation['beats_menu'] = False

        update_mouse_position()
        update_mouse_state()
        update_key_state(events)

        screen.fill(COLORS['background'])

        if update['beats_buttons']:
            update['beats_buttons'] = False
            beats_buttons = []
            add_beats_list_buttons(beats_buttons)
        
        check_buttons(buttons, mouse_position['pos'], mouse_click_tracker, screen, font)
        check_buttons(beats_buttons, mouse_position['pos'], mouse_click_tracker, screen, font, key_hold_tracker, key_down_tracker, True, update, 'beats_buttons')

        if screen.get_size() != (size := (width(), height())):
            screen = pygame.display.set_mode((size))
            path_surface = pygame.Surface(size, pygame.SRCALPHA)

        fade_path_surface(path_surface, 3)
        screen.blit(path_surface, (0,0))

        draw_beat(environment, screen)

        pygame.display.update()

        clock.tick(60)


def orbital_beats(button):
    global screen
    path_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    environment = Environment(time.perf_counter())

    beats = button.args['beat']
    load_scenes_json(environment, beats)
    if in_and_true('from_beats_menu', button.args):
        button.args['update']['beats_buttons'] = True

    last_frame_time = time.perf_counter()
    situation['in_game'] = True
    while situation['in_game']:

        events = pygame.event.get()
        if check_quit(events): situation['in_game'] = False

        update_mouse_position()
        update_mouse_state()
        update_key_state(events)

        if in_and_true(pygame.K_LCTRL, key_hold_tracker) and in_and_true(pygame.K_s, key_down_tracker):
            save_scene_json(environment)

        screen.fill(COLORS['background'])

        if not simulation['paused']:
            update_particles(environment, path_surface)

        # Restricts frame updates to 60 per second
        if (current_frame_time := time.perf_counter()) - last_frame_time < 1 / 60:
            continue
        last_frame_time = current_frame_time

        # Checks if the current screen size matches the settings
        if screen.get_size() != (size := (width(), height())):
            screen = pygame.display.set_mode((size))
            path_surface = pygame.Surface(size, pygame.SRCALPHA)

        fade_path_surface(path_surface, 1)
        screen.blit(path_surface, (0,0))

        draw_beat(environment, screen)

        pygame.display.update()


def options_menu(button):
    global screen
    path_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    environment = Environment(time.perf_counter())

    options_buttons = [
        Button(
            f'Screen size: {width()}x{height()}',
            increment_screen_size,
            {'visual': visual, 'screen': screen},
            (0, 0),
            (360, 40),
            (159, 159, 159),
            (210, 210, 210),
            (0, 0, 0),
            (16, 16, 32),
        ),

        Button(
            'Back',
            back,
            {'situation': situation, 'current': 'options_menu'},
            (0, -100),
            (300, 40),
        ),
    ]

    situation['options_menu'] = True
    while situation['options_menu']:

        events = pygame.event.get()
        if check_quit(events): situation['options_menu'] = False

        update_mouse_position()
        update_mouse_state()
        update_key_state(events)

        screen.fill(COLORS['background'])

        check_buttons(options_buttons, mouse_position['pos'], mouse_click_tracker, screen, font)

        if screen.get_size() != (size := (width(), height())):
            screen = pygame.display.set_mode((size))
            path_surface = pygame.Surface(size, pygame.SRCALPHA)

        update_particles(environment, path_surface)
        draw_beat(environment, screen)

        fade_path_surface(path_surface, 3)
        screen.blit(path_surface, (0,0))

        pygame.display.update()

        clock.tick(60)

if __name__ == '__main__':
    main()
