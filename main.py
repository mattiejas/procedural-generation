from terrain import generate_terrain, colormap
from beach import add_beaches
import matplotlib.pyplot as plt

world, heightmap = generate_terrain()
world, beaches_heightmap = add_beaches(world, heightmap)

plt.imsave("beaches_heightmap.png", beaches_heightmap, cmap="gray")
plt.imsave("map.png", world, cmap=colormap)
