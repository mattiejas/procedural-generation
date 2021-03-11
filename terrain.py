from color import interpolate_color, hex_to_rgb
from perlin_noise import PerlinNoiseFactory
import numpy as np
from matplotlib.colors import ListedColormap

BEACH_BIOME_THRESHOLD_WATERSIDE = 0.01
BEACH_BIOME_THRESHOLD_LANDSIDE = 0.02

# OCEAN = -2
WAVES = -1
WATER = 0
LOWLANDS = 1
LAND = 2
HIGHLANDS = 3
MOUNTAIN = 4
SNOW = 5
SAND = 6

biomes = {
    # OCEAN: {'from': 0.0, 'to': 0.2, 'color': '#2fa6ba', 'color_dark': '#82e4f5'},
    WATER: {'from': 0, 'to': 0.35, 'color': '#82e4f5', 'color_dark': '#158496'},
    WAVES: {'from': 0.35, 'to': 0.4, 'color': '#f0fbfc', 'color_dark': '#88ecfc'},
    LOWLANDS: {'from': 0.4, 'to': 0.5, 'color': '#30b315', 'color_dark': '#28a30f'},
    LAND: {'from': 0.5, 'to': 0.6, 'color': '#3bc91e', 'color_dark': '#33bd17'},
    HIGHLANDS: {'from': 0.6, 'to': 0.7, 'color': '#8bf576', 'color_dark': '#63e349'},
    MOUNTAIN: {'from': 0.7, 'to': 0.80, 'color': '#faf0b1', 'color_dark': '#f5e476'},
    SNOW: {'from': 0.80, 'to': 1.0, 'color': '#ffffff', 'color_dark': '#fffce6'},
    SAND: {'from': 0.4 - BEACH_BIOME_THRESHOLD_WATERSIDE, 'to': 0.4 + BEACH_BIOME_THRESHOLD_LANDSIDE, 'color': '#f7f7c8', 'color_dark': '#dedec5'},
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
    # if height < biomes[OCEAN]['to']:
    #     return OCEAN
    if height < biomes[WATER]['to']:
        return WATER
    elif height < biomes[WAVES]['to']:
        return WAVES
    elif height < biomes[LOWLANDS]['to']:
        return LOWLANDS
    elif height < biomes[LAND]['to']:
        return LAND
    elif height < biomes[HIGHLANDS]['to']:
        return HIGHLANDS
    elif height < biomes[MOUNTAIN]['to']:
        return MOUNTAIN
    else:
        return SNOW


get_biomes = np.vectorize(get_biome_from_height)


def generate_terrain(width=256, height=256, octaves=7, scale=0.03):
    PN = PerlinNoiseFactory(2, octaves=octaves)
    noise = np.zeros((height, width))

    for y in range(0, height):
        for x in range(0, width):
            noise[y, x] = PN(x / width * scale, y / height * scale)

    return (noise - noise.min()) / (noise.max() - noise.min())
