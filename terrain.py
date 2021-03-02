from color import interpolate_color, hex_to_rgb
from perlin_noise import PerlinNoiseFactory
import numpy as np
from matplotlib.colors import ListedColormap

BEACH_BIOME_THRESHOLD = 0.02

WATER = 0
LAND = 1
MOUNTAIN = 2
SNOW = 3
SAND = 4

biomes = {
    WATER: {'from': 0.0, 'to': 0.4, 'color': '#14dcff', 'color_dark': '#0fb4d1'},
    LAND: {'from': 0.4, 'to': 0.7, 'color': '#38c21b', 'color_dark': '#28a30f'},
    MOUNTAIN: {'from': 0.7, 'to': 0.90, 'color': '#c4c284', 'color_dark': '#c2bc1b'},
    SNOW: {'from': 0.90, 'to': 1.0, 'color': '#fafff0', 'color_dark': '#e7f2ce'},
    SAND: {'from': 0.4 - BEACH_BIOME_THRESHOLD, 'to': 0.4 + BEACH_BIOME_THRESHOLD, 'color': '#f2f28d', 'color_dark': '#e8e87b'},
}

colormap = ListedColormap([b['color'] for b in biomes.values()])


def get_tile_color(type, height):
    biome = biomes[type]

    if biome['from'] != -1:
        intensity = (height - biome['from']) / (biome['to'] - biome['from'])
    else:
        intensity = height

    return interpolate_color(biome['color'], biome['color_dark'], intensity)


def get_colormap(world, heightmap):
    colormap = np.zeros((*world.shape, 3))
    for y in range(world.shape[0]):
        for x in range(world.shape[1]):
            colormap[y, x] = list(hex_to_rgb(get_tile_color(world[y, x], heightmap[y, x])))
    return colormap.astype(np.uint8)


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


def generate_terrain(width=256, height=256, octaves=6, scale=0.03):
    PN = PerlinNoiseFactory(2, octaves=octaves)
    noise = np.zeros((height, width))

    for y in range(0, height):
        for x in range(0, width):
            noise[y, x] = PN(x * scale, y * scale)

    return (noise - noise.min()) / (noise.max() - noise.min())
