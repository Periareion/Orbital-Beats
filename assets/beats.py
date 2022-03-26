from orbe.attractor import Attractor
from orbe.particle import Particle

# Attractor(name, color, mass, position)
# Particle(name, primary_color, secondary_color, soundfile, period, eccentricity, mean_anomaly_start, azimuth)


O = [
    (
        Attractor('O', '#1540aa', 5*10**15, [-300, 210]),

        [
            Particle('1', '#ffffff', '#ffffff', None, 2, 0.3, 0, 270),
            Particle('2', '#ffffff', '#ffffff', None, 2, 0.3, 180, 270),
        ],
    ),
]

solway = [
    (
        Attractor('O', '#1540aa', 5*10**15, [-300, 210]),

        [
            Particle('1', '#777777', '#ffffff', 'space_beet/hihat C.wav', 2, 0.3, -0, 270),
            Particle('1', '#7700cc', '#ffffff', 'assets/sounds/bum2.wav', 2, 0.3, -0, 270),
            Particle('2', '#777777', '#ffffff', 'space_beet/hihat O.wav', 2, 0.3, -45, 270),
            Particle('3', '#777777', '#ffffff', 'space_beet/hihat C.wav', 2, 0.3, -90, 270),
            Particle('4', '#777777', '#ffffff', 'space_beet/hihat O.wav', 2, 0.3, -135, 270),
            Particle('4', '#7700cc', '#ffffff', 'assets/sounds/bam2.wav', 2, 0.3, -135, 270),
            Particle('5', '#ffffff', '#ffffff', 'space_beet/kick.wav', 2, 0.3, -225, 270),
            Particle('5', '#ffffff', '#ffffff', 'space_beet/hihat C.wav', 2, 0.3, -225, 270),
            Particle('6', '#ffffff', '#ffffff', 'space_beet/kick.wav', 2, 0.3, -247.5, 270),
            Particle('7', '#ffffff', '#ffffff', 'space_beet/snare.wav', 2, 0.3, -270, 270),
        ],
    ),
]

space_beet = [
    (
        Attractor('John', '#88328a', 5*10**16, [-160,-160]),

        [
            Particle('snare', '#cc4ccf', '#cc4ccf', 'space_beet/snare.wav', 3, 0.7, 90, 310),
            Particle('snare', '#cc4ccf', '#cc4ccf', 'space_beet/snare.wav', 3, 0.7, 270, 310),

            Particle('kick', '#f79cad', '#f79cad', 'space_beet/kick.wav', 3, 0.4, 0, 310),
            Particle('kick', '#f79cad', '#f79cad', 'space_beet/kick.wav', 3, 0.4, 10/32*360, 310),
            Particle('kick', '#f79cad', '#f79cad', 'space_beet/kick.wav', 3, 0.4, 20/32*360, 310),
        ],
    ),

    (
        Attractor('Nate', '#9c7e27', 10**16, [160,-160]),

        [
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 0, 240),
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 45, 240),
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 90, 240),
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 135, 240),
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 180, 240),
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 225, 240),
            Particle('hihat C', '#bd992f', '#bd992f', 'space_beet/hihat C.wav', 3, 0.6, 270, 240),

            Particle('hihat O', '#8d692f', '#7d592f', 'space_beet/hihat O.wav', 3, 0.6, 315, -65),
        ],
    ),
]

"""
    test = [
        Particle('d2', '#ff6611', '#ff2288', 'ambient_snare.wav', main_attractor, 1.5, 0.6, 0, 220, True),
        Particle('d1', '#ff6611', '#ff6611', 'acoustic_snare.wav', main_attractor, 1.5, 0.6, -90, 220, True),
        Particle('b1', '#2277ee', '#223388', '909sd.wav', main_attractor, 1.5, 0.5, 180, 20),
        Particle('b2', '#2277ee', '#223388', '909sd.wav', main_attractor, 1.5, 0.5, 225, 25),
        Particle('b3', '#2277ee', '#223388', '909sd.wav', main_attractor, 1.5, 0.5, 270, 30),

        Particle('m', '#aa33ee', '#dd55ee', 'm1.wav', main_attractor, 3, 0.7, 0, 160),
        Particle('m', '#aa33ee', '#dd55ee', 'm1.wav', main_attractor, 3, 0.7, 90, 160),
        Particle('M', '#551177', '#551177', 'm2.wav', main_attractor, 3, 0.7, 180, 160),
        Particle('M', '#551177', '#551177', 'm2.wav', main_attractor, 3, 0.7, 270, 160),
    ]
"""

# Particle('Snare', '#c2114c', '#c2114c', '909sd.wav', space.attractors[0], 1.5, 0.5, 0, 270),
# Particle('Snare', '#5924e0', '#5924e0', '909sd.wav', space.attractors[0], 1.5, 0.5, 180, 270),
# Particle('Snare', '#24e06c', '#24e06c', 'ec-sn004.wav', space.attractors[0], 1.5, 0.7, 90, 0),
# Particle('Snare', '#248fe0', '#248fe0', 'acoustic_snare.wav', space.attractors[0], 1.5, 0.7, 270, 180),

# Particle('Snare', '#333333', '#555555', 'acoustic_snare.wav', space.attractors[1], 3, 0.6, 180, 180),
# Particle('Snare', '#333333', '#555555', 'acoustic_snare.wav', space.attractors[1], 3, 0.6, 0, 180),
# Particle('Snare', '#ff4433', '#ff55ff', 'acoustic_snare.wav', space.attractors[2], 3, 0, 0, 180),
