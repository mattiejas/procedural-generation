import numpy as np
from terrain import biomes
import terrain
from perlin_noise import PerlinNoiseFactory


def replace_land(world, heightmap, noise, noise_threshold, biome_threshold):
    for y in range(0, world.shape[0]):
        for x in range(0, world.shape[1]):
            if noise[y, x] > noise_threshold and (
                    world[y, x] == terrain.LAND or
                    world[y, x] == terrain.WATER) and (
                    heightmap[y, x] < biomes[terrain.WATER]['to'] + biome_threshold and
                    heightmap[y, x] > biomes[terrain.LAND]['from'] - biome_threshold):
                world[y, x] = terrain.SAND

    return world


def add_beaches(world, heightmap, noise_threshold=0.5, biome_threshold=0.025, octaves=8, scale=0.003):
    PN = PerlinNoiseFactory(2, octaves=octaves)
    height, width = world.shape
    noise = np.zeros((height, width))

    for y in range(0, height):
        for x in range(0, width):
            noise[y, x] = PN(x * scale, y * scale)

    noise = (noise - noise.min()) / (noise.max() - noise.min())
    return replace_land(world, heightmap, noise, noise_threshold, biome_threshold), noise
