import sys, os
import time
import warnings
import json

warnings.filterwarnings('ignore', '.*-2147417850*', )

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

from orbe.utils import *

from orbe.settings import simulation, visual, COLORS, width, height, situation

from orbe.environment import Environment

pygame.font.init()
title_font = pygame.font.Font('assets/fonts/ethnocentric rg.ttf', 60)
font = pygame.font.SysFont('Consolas', 28, True)

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
            (0, 160),
            (300, 40),
            (159, 159, 159),
            (210, 210, 210),
            (0, 0, 0),
            (16, 16, 32),
        ),

        Button(
            'Start',
            orbital_beats, {},
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

        update_mouse_position()
        update_mouse_state()

        events = pygame.event.get()
        if check_quit(events): situation['main_menu'] = False

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

    load_scenes_json(environment, [])

    buttons = [

    ]

    situation['beats_menu'] = True
    while situation['beats_menu']:

        update_mouse_position()
        update_mouse_state()

        events = pygame.event.get()
        if check_quit(events): situation['beats_menu'] = False

        screen.fill(COLORS['background'])
        
        check_buttons(buttons, mouse_position['pos'], mouse_click_tracker, screen, font)

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

    load_scenes_json(environment, ['Space Beet', 'Solway'])

    last_frame_time = time.perf_counter()
    situation['in_game'] = True
    while situation['in_game']:

        update_mouse_position()
        update_mouse_state()

        events = pygame.event.get()
        if check_quit(events): situation['in_game'] = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    save_scene_json(environment)

        screen.fill(COLORS['background'])

        if not simulation['paused']:
            update_particles(environment, path_surface)

        if (current_frame_time := time.perf_counter()) - last_frame_time < 1 / 60:
            continue
        last_frame_time = current_frame_time
        
        if screen.get_size() != (size := (width(), height())):
            screen = pygame.display.set_mode((size))
            path_surface = pygame.Surface(size, pygame.SRCALPHA)

        fade_path_surface(path_surface, 3)
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
            {'situation': situation, 'current': 'in_options'},
            (0, -100),
            (300, 40),
        ),
    ]

    situation['options_menu'] = True
    while situation['options_menu']:

        update_mouse_position()
        update_mouse_state()

        events = pygame.event.get()
        if check_quit(events): situation['options_menu'] = False

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
