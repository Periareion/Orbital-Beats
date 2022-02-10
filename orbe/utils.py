
import sys, os

import math
import time
import random
import json
import ast

import numpy as np
import pygame

from orbe.particle import Particle
from orbe.system import System
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


def random_hex(n):
    return hex(random.randint(0,16**n-1)).replace('0x','').zfill(n)
    
    #return [rand for k in range(n) if (rand := random.choice('0123456789abcdef'))].join('')


def pgColor_to_hex(color):
    return '#%02x%02x%02x' % (color.r, color.g, color.b)


def load_json(json_file_name):
    with open(json_file_name) as json_file:
        data = json.load(json_file)
        return data


def dump_json(json_file_name, data):
    with open(json_file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def load_scenes_json(environment, scene_names):

    if isinstance(scene_names, str):
        scene_names = [scene_names]

    if isinstance(scene_names, (list, tuple)):

        for scene_name in scene_names:

            try:
                print(f'Attempting to load scene \'{scene_name}\'')
                scenes = load_json('beats.json')
            except Exception as E:
                print(f'Failed to load scene \'{scene_name}\' ({E})')
                return
            finally:
                pass

            scene = scenes[scene_name]

            for system in scene:
                system_arguments = system['System']
                particles = system['Particles']

                system = System(
                    system_arguments['name'],
                    system_arguments['color'],
                    float(system_arguments['mass']),
                    ast.literal_eval(system_arguments['position'])
                )

                environment.systems.append(system)

                for particle_arguments in particles:

                    particle = Particle(
                        system,
                        particle_arguments['name'],
                        particle_arguments['color'],
                        particle_arguments['secondary'],
                        particle_arguments['sound'],
                        float(particle_arguments['period']),
                        float(particle_arguments['eccentricity']),
                        float(particle_arguments['start']),
                        float(particle_arguments['orientation'])
                    )

                    system.particles.append(particle)

            print(f'Scene \'{scene_name}\' has been loaded successfully!')


def save_scene_json(environment, scene_name=None):
    if scene_name == None:
        scene_name = random_hex(16)

    scene_dict = {scene_name: []}

    for system in environment.systems:
        system_dict = {}

        system_dict["System"] = {
            "name": system.name,
            "color": pgColor_to_hex(system.attractor_color),
            "mass": system.attractor_mass,
            "position": str(tuple(system.attractor_position))
        }

        system_dict["Particles"] = []
        
        for particle in system.particles:
            system_dict["Particles"].append(
                {
                    "name": particle.name, "color": pgColor_to_hex(particle.color), "secondary": particle.secondary_color, "sound": particle.soundfile,
					"period": particle.period, "eccentricity": particle.eccentricity, "start": math.degrees(particle.mean_anomaly_start), "orientation": math.degrees(particle.orientation)
                }
            )

        scene_dict[scene_name].append(system_dict)
    
    try:
        print(f'Loading scene \'{scene_name}\'')
        all_beats = load_json('beats.json')
        new_all_beats = all_beats

        print(f'Updating scene \'{scene_name}\'')
        new_all_beats.update(scene_dict)

        print(f'Attempting to save scene \'{scene_name}\'')
        dump_json('beats.json', new_all_beats)
        
    except Exception as E:
        print(f'Failed to save scene \'{scene_name}\' ({E})')
        print(f'Rewinding beats.json file')
        dump_json('beats.json', all_beats)
        return
    finally:
        print(f'Scene \'{scene_name}\' has been saved successfully!')


def update_particles(environment, path_surface):
    for system in environment.systems:
        for particle in system.particles:

            old_position = particle.position
            particle.update_position(time.perf_counter(), environment.start_time)

            pygame.draw.aaline(path_surface, particle.secondary_color,
                screen_position(old_position),
                screen_position(particle.position))


from pygame import gfxdraw

def draw_beat(environment, screen):

    for system in environment.systems:
        #pygame.draw.circle(screen, system.attractor_color, screen_position(system.attractor_position), 7)
        gfxdraw.aacircle(screen, *[int(x+1) for x in screen_position(system.attractor_position)], 7, system.attractor_color)
        gfxdraw.filled_circle(screen, *[int(x+1) for x in screen_position(system.attractor_position)], 7, system.attractor_color)

        for particle in system.particles:
            #pygame.draw.circle(screen, particle.color, [x+1 for x in screen_position(particle.position)], 4)
            gfxdraw.aacircle(screen, *[int(x+1) for x in screen_position(particle.position)], 4, particle.color)
            gfxdraw.filled_circle(screen, *[int(x+1) for x in screen_position(particle.position)], 4, particle.color)

            if particle.animations:
                frame = particle.animations[0]
                screen.blit(frame, screen_position(particle.position, (-frame.get_width()/2, -frame.get_height()/2)))
                particle.animations.pop(0)

def say_hi():
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

    def __init__(self, text='Hi', function=say_hi, args={}, rect_pos=(0,0), rect_dim=(0,0), primary_text_color=(159,159,159), secondary_text_color=(210,210,210), primary_color=(0,0,0), secondary_color=(16,16,32)):

        self.text = text
        self.function = function
        self.args = args
        self.rect_pos = rect_pos
        self.rect_dim = rect_dim
        self.primary_text_color = primary_text_color
        self.secondary_text_color = secondary_text_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color


def check_buttons(buttons, mouse_pos, mouse_click_tracker, screen, font):
    for button in buttons:
        button.rect = pygame.Rect(*screen_position(button.rect_pos), *button.rect_dim)
        button.rect.center = button.rect.topleft
        
        if button.rect.collidepoint(mouse_pos):
            text_color = button.secondary_text_color
            color = button.secondary_color

            if True in mouse_click_tracker.values():
                button.args.update({'mouse_clicks': mouse_click_tracker})
                return button.function(button)
        else:
            text_color = button.primary_text_color
            color = button.primary_color
        pygame.draw.rect(screen, color, button.rect)
        draw_text(button.text, font, text_color, screen, *button.rect.center, 'center')


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
