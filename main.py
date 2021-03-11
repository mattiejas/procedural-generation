from erosion import erosion
from terrain import generate_terrain, colormap, get_colormap, get_tile_color, get_biomes
from beach import add_beaches
import matplotlib.pyplot as plt
from PIL import Image
from color import hex_to_rgb
import util
import random

# Seed for map generation
# random.seed("this is a random seed")

height, width = [128] * 2

# Generate terrain
heightmap = generate_terrain(width, height, scale=3)

# Uncomment to apply erosion
heightmap = erosion(heightmap)

# Uncomment to apply gaussian to make terrain smoother, did not look that good
# heightmap = util.gaussian_blur(heightmap, .5)

# Uncomment to normalize heightmap, makes a lot more snow
# heightmap = util.normalize(heightmap, bounds=(0.2, 1))

# Generate biomes based on height
world = get_biomes(heightmap)

# Replace some parts of biomes with beaches
world, beaches_heightmap = add_beaches(world, heightmap)

colored = get_colormap(world, heightmap)
img = Image.fromarray(colored)
img.save('map.png')

plt.imsave("map.pdf", colored)
plt.imsave("heightmap.pdf", heightmap, cmap="gray")
plt.imsave("beaches-heightmap.pdf", beaches_heightmap, cmap="gray")
