from erosion import erosion
from terrain import generate_terrain, colormap, get_colormap, get_tile_color, get_biomes
from beach import add_beaches
import matplotlib.pyplot as plt
from PIL import Image
from color import hex_to_rgb
import util

height, width = [128] * 2
heightmap = generate_terrain(width, height, scale=4)
# heightmap = util.fbm((height, width), -2.0)
heightmap = erosion(heightmap)
heightmap = util.gaussian_blur(heightmap, .3)
# heightmap = util.normalize(heightmap, bounds=(0.2, 1))
world = get_biomes(heightmap)
world, beaches_heightmap = add_beaches(world, heightmap)

img = Image.fromarray(get_colormap(world, heightmap))


img.save('map.png')
plt.imsave("heightmap.png", heightmap, cmap="gray")
