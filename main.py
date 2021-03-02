from terrain import generate_terrain, colormap, get_tile_color
from beach import add_beaches
import matplotlib.pyplot as plt
from PIL import Image
from color import hex_to_rgb

height, width = 256, 256
world, heightmap = generate_terrain(width, height, scale=0.0125)
world, beaches_heightmap = add_beaches(world, heightmap)

img = Image.new('RGB', (width, height))
for y in range(height):
    for x in range(width):
        color = hex_to_rgb(get_tile_color(world[y, x], heightmap[y, x]))
        img.putpixel((x, y), tuple(color))

img.save('map.png')
