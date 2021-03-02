from color import interpolate_color
from perlin_noise import PerlinNoiseFactory
import numpy as np
from matplotlib.colors import ListedColormap

WATER = 0
LAND = 1
MOUNTAIN = 2
SNOW = 3
SAND = 4

biomes = {
    WATER: {'from': 0.0, 'to': 0.4, 'color': '#14dcff', 'color_dark': '#0dbddb'},
    LAND: {'from': 0.4, 'to': 0.7, 'color': '#38c21b', 'color_dark': '#28a30f'},
    MOUNTAIN: {'from': 0.7, 'to': 0.90, 'color': '#edd591', 'color_dark': '#e3c05b'},
    SNOW: {'from': 0.90, 'to': 1.0, 'color': '#ffffff', 'color_dark': '#e6e6e6'},
    SAND: {'from': 0.4 - 0.025, 'to': 0.4 + 0.025, 'color': '#e3e3aa', 'color_dark': '#d1d192'},
}

colormap = ListedColormap([b['color'] for b in biomes.values()])


def get_tile_color(type, height):
    biome = biomes[type]

    if biome['from'] != -1:
        intensity = (height - biome['from']) / (biome['to'] - biome['from'])
    else:
        intensity = height

    return interpolate_color(biome['color'], biome['color_dark'], intensity)


def get_biome_from_height(height):
    if height < biomes[WATER]['to']:
        return WATER
    elif height < biomes[LAND]['to']:
        return LAND
    elif height < biomes[MOUNTAIN]['to']:
        return MOUNTAIN
    else:
        return SNOW


get_biomes = np.vectorize(get_biome_from_height)


def generate_terrain(width=256, height=256, octaves=6, scale=0.01):
    PN = PerlinNoiseFactory(2, octaves=octaves)
    noise = np.zeros((height, width))

    for y in range(0, height):
        for x in range(0, width):
            noise[y, x] = PN(x * scale, y * scale)

    noise = (noise - noise.min()) / (noise.max() - noise.min())
    return get_biomes(noise), noise
