import math
import ast
import json
import pygame

from orbe.utils import *


def load_json(json_file_name):
    with open(json_file_name) as json_file:
        data = json.load(json_file)
        return data


def dump_json(json_file_name, data):
    with open(json_file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def json_to_attractor(json_attractor):
    if isinstance(json_attractor['position'], str):
        json_attractor['position'] = list(ast.literal_eval(json_attractor['position']))
        print(json_attractor['position'])

    attractor = Attractor(
        json_attractor['name'],
        json_attractor['color'],
        float(json_attractor['mass']),
        json_attractor['position']
    )
    return attractor

def json_to_particle(json_particle, attractor):
    particle = Particle(
        attractor,
        json_particle['name'],
        json_particle['color'],
        json_particle['secondary'],
        json_particle['sound'],
        float(json_particle['period']),
        float(json_particle['eccentricity']),
        float(json_particle['start']),
        float(json_particle['orientation'])
    )
    return particle

def attractor_to_json(attractor):
    json_attractor = {
        "name": attractor.name,
        "color": pgColor_to_hex(attractor.color),
        "mass": attractor.mass,
        "position": list(attractor.position)
    }
    return json_attractor

def particle_to_json(particle):
    json_particle = {
        "name": particle.name, "color": pgColor_to_hex(particle.color), "secondary": particle.secondary_color,
        "sound": particle.soundfile,
        "period": particle.period, "eccentricity": particle.eccentricity,
        "start": math.degrees(particle.mean_anomaly_start), "orientation": math.degrees(particle.orientation)
    }
    return json_particle

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

            for attractor in scene:
                attractor_arguments = attractor['Attractor']
                particles = attractor['Particles']

                attractor = json_to_attractor(attractor_arguments)

                environment.attractors.append(attractor)
                for particle_arguments in particles:

                    particle = json_to_particle(particle_arguments, attractor)

                    attractor.particles.append(particle)

            print(f'Loaded scene successfully! \'{scene_name}\'')


def save_scene_json(environment, scene_name=None):
    if scene_name == None:
        scene_name = random_hex(16)

    scene_dict = {scene_name: []}

    for attractor in environment.attractors:
        attractor_dict = {}

        attractor_dict["Attractor"] = attractor_to_json(attractor)

        attractor_dict["Particles"] = []
        for particle in attractor.particles:
            json_particle = particle_to_json(particle)
            attractor_dict["Particles"].append(json_particle)

        scene_dict[scene_name].append(attractor_dict)

    try:
        print(f'Loading {"beats.json"}')
        all_beats = load_json("beats.json")
        new_all_beats = all_beats

        print(f'Updating {"beats.json"}')
        new_all_beats.update(scene_dict)

        print(f'Attempting to save scene \'{scene_name}\'')
        dump_json('beats.json', new_all_beats)

    except Exception as E:
        print(f'Failed to save scene \'{scene_name}\' ({E})')
        print(f'Rewinding beats.json file')
        dump_json('beats.json', all_beats)
        return
    print(f'Saved scene successfully! \'{scene_name}\'')


def remove_beat(beat_name):
    all_beats = load_json('beats.json')
    new_beats = all_beats.copy()
    del new_beats[beat_name]

    try:
        dump_json('beats.json', new_beats)
    except Exception as E:
        print(f'There was an exception! ({E})')
        dump_json('beats.json', new_beats)
        return
    print(f'Successfully removed \'{beat_name}\' from beats.json')
