
import time
import math
import numpy as np
from scipy.special import jv

import pygame
import pyglet

from orbe.settings import CONSTS

pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

def norm(vector):

    "Norm of 2D vector"

    return (vector[0]**2+vector[1]**2)**0.5


class Particle:

    def __init__(self,
                 system,
                 name: str = 'Bob',
                 color: str = '#ffffff',
                 secondary_color: str = '#ffffff',
                 soundfile = None,
                 period: float = 1,
                 eccentricity: float = 0.3,
                 mean_anomaly_start: float = 0,
                 orientation: float = 0,
                 clockwise = False):

        self.system = system
        self.name = name
        self.color = pygame.Color(color)
        self.secondary_color = secondary_color

        self.soundfile = soundfile
        try:
            self.sound = pyglet.resource.media(self.soundfile, streaming=False)
            self.sound.play()
        except:
            self.sound = None

        self.period = period
        self.eccentricity = eccentricity
        self.orientation = math.radians(orientation)
        self.mean_anomaly_start = math.radians(mean_anomaly_start)
        self.clockwise = clockwise
        self.sgn = 1

        self.poof_images = [pygame.transform.scale(pygame.image.load(f'assets/textures/poof/poof{i}.png'), (24, 24)) for i in range(11)]
        self.animations = []

        self.semi_major_axis = (CONSTS['G'] * system.attractor_mass * (period / (2 * math.pi)) ** 2) ** (1 / 3)
        self.apoapsis = self.semi_major_axis*(1+self.eccentricity)
        self.periapsis = self.semi_major_axis*(1-self.eccentricity)

        self.position = np.array([0, 0], dtype=np.float64)
        self.update_position(0, 0)

    def update_position(self, time, start_time):

        e = self.eccentricity

        mean_anomaly = (1 - 2 * self.clockwise) * 2 * math.pi / self.period * (
                    time - start_time) + self.mean_anomaly_start

        eccentric_anomaly = mean_anomaly + 2 * sum(
            [1 / k * jv(k, k * e) * math.sin(k * mean_anomaly) for k in range(1, 100)])

        true_anomaly = 2 * math.atan2((1 + e) ** 0.5 * math.sin(eccentric_anomaly / 2),
                                      (1 - e) ** 0.5 * math.cos(eccentric_anomaly / 2))
        # 2*math.atan(((1+e)/(1-e))**0.5*math.tan(eccentric_anomaly/2))

        self.new_sgn = math.copysign(1, true_anomaly)
        if self.sgn != self.new_sgn and not not self.sound:
            self.sgn = self.new_sgn
            self.sound.play()
            self.animations.extend(self.poof_images)

        radius = self.semi_major_axis * (1 - e ** 2) / (1 + e * math.cos(true_anomaly))

        self.position = [self.system.attractor_position[0] + radius * math.cos(true_anomaly + self.orientation),
                         self.system.attractor_position[1] + radius * math.sin(true_anomaly + self.orientation)]




        #beta = (1-(1-e**2)**0.5)/e
        #true_anomaly = mean_anomaly + 2*sum([1/s*(jv(s, s*e)+sum([beta**p*(jv(s-p, s*e) + jv(s+p, s*e)) for p in range(1,100)]))*math.sin(s*mean_anomaly) for s in range(1,30)])
        
        #    true_anomaly = mean_anomaly
 
##        if start_at_apoapsis:
##            apoapsis = semi_major_axis*(1+eccentricity)
##            self.position = apoapsis*np.array([math.cos(math.radians(orientation)), math.sin(math.radians(orientation))], dtype=np.float64)
##            velocity_norm = math.sqrt(CONSTS['G']*system_mass*(2/apoapsis-1/semi_major_axis))
##            self.velocity = velocity_norm*np.array([math.cos(math.radians(orientation+90)), math.sin(math.radians(orientation+90))], dtype=np.float64)
##        else:
##            periapsis = semi_major_axis*(1-eccentricity)
##            self.position = periapsis*-np.array([math.cos(math.radians(orientation)), math.sin(math.radians(orientation))], dtype=np.float64)
##            velocity_norm = math.sqrt(CONSTS['G']*system_mass*(2/periapsis-1/semi_major_axis))
##            self.velocity = velocity_norm*-np.array([math.cos(math.radians(orientation+90)), math.sin(math.radians(orientation+90))], dtype=np.float64)

        #self.position = np.array(position, dtype=np.float64)
        #self.velocity = np.array(velocity, dtype=np.float64)

##        print(self.position, self.velocity)
##
##        self.new_position = self.position.copy()
##        self.new_velocity = self.velocity.copy()
##
##        self.last_delta_velocity_sign = self.delta_velocity_sign

##    @property
##    def direction(self):
##
##        "Normalized velocity vector"
##
##        velocity_norm = norm(self.velocity)
##        if velocity_norm == 0:
##            return 0
##        else:
##            return self.velocity / velocity_norm
##
##    @property
##    def delta_velocity_sign(self):
##        return math.copysign(1,norm(self.new_velocity)-norm(self.velocity))
##
##    def acceleration(self, position, systems):
##        acceleration = np.array([0,0], dtype=np.float64)
##
##        for system in systems:
##            distance = system.position - position
##            distance_norm = math.sqrt(distance[0]**2+distance[1]**2)
##            acceleration += CONSTS['G'] * system.mass * distance / distance_norm**3
##
##        return acceleration
##
##    def update_position(self, delta_time, systems):
##        self.new_position = self.position + self.velocity * delta_time + 0.5 * self.acceleration(self.position, systems) * delta_time**2
##
##    def update_velocity(self, delta_time, systems):
##        self.new_velocity = self.velocity + (self.acceleration(self.position, systems) + self.acceleration(self.new_position, systems)) * 0.5 * delta_time
