from terrain import generate_terrain, colormap
from beach import add_beaches
import matplotlib.pyplot as plt

world, heightmap = generate_terrain()
world = add_beaches(world, heightmap)

plt.imsave("map.png", world, cmap=colormap)
