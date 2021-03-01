from perlin_noise import PerlinNoiseFactory
import numpy as np
from matplotlib.colors import ListedColormap

OCEAN = -1
WATER = 0
LOWLANDS = 1
LAND = 2
HIGHLANDS = 3
MOUNTAIN = 4
SNOW = 5
# SAND = 3

OCEAN_THRESHOLD = 0.2
WATER_THRESHOLD = 0.4
MOUNTAIN_THRESHOLD = 0.80
SNOW_THRESHOLD = 0.90

biomes = {
    OCEAN: [0, '#0dbddb'],
    WATER: [0.2, '#14dcff'],
    LOWLANDS: [0.4, '#209608'],
    LAND: [0.55, '#29a110'],
    HIGHLANDS: [0.7, '#38c21b'],
    MOUNTAIN: [0.8, '#e6e6e6'],
    SNOW: [0.9, '#fff'],
    # SAND: [0.2, '#ebebae'],
}

colormap = ListedColormap(np.array(list(biomes.values()))[:, 1])


def get_biome_from_height(height):
    if height < biomes[WATER][0]:
        return OCEAN
    elif height < biomes[LOWLANDS][0]:
        return WATER
    elif height < biomes[LAND][0]:
        return LOWLANDS
    elif height < biomes[HIGHLANDS][0]:
        return LAND
    elif height < biomes[MOUNTAIN][0]:
        return HIGHLANDS
    elif height < biomes[SNOW][0]:
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
