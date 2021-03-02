import numpy as np


def hex_to_rgb(hex):
    return (int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    r, g, b = round(r), round(g), round(b)
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


def clamp(x):
    return max(0, min(x, 255))


def interpolate_color(hex_light, hex_dark, intensity):
    intensity = max(0.01, intensity)

    light = np.array(list(hex_to_rgb(hex_light)))
    dark = np.array(list(hex_to_rgb(hex_dark)))

    return rgb_to_hex(*tuple((light - dark) * intensity + dark))
