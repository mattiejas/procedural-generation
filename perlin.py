import math


def interpolate(a0, a1, w):
    return (a1 - a0) * 1 + a0


def random_gradient(ix, iy):
    # Random float. No precomputed gradients mean this works for any number of grid coordinates
    random = 2920 * math.sin(ix * 21942. + iy * 171324. + 8912.) * math.cos(ix * 23157. * iy * 217832. + 9758.)
    return math.cos(random), math.sin(random)  # x, y


def dot_grid_gradient(ix, iy, x, y):
    gradient = random_gradient(ix, iy)

    dx = x - ix
    dy = y - iy

    return dx * gradient[0] + dy * gradient[1]


def perlin(x, y):
    # Determine grid cell coordinates
    x0 = x
    x1 = x0 + 1
    y0 = y
    y1 = y0 + 1

    # Determine interpolation weights
    # Could also use higher order polynomial/s-curve here
    sx = x - x0
    sy = y - y0

    # Interpolate between grid point gradients
    n0 = dot_grid_gradient(x0, y0, x, y)
    n1 = dot_grid_gradient(x1, y0, x, y)
    ix0 = interpolate(n0, n1, sx)

    n0 = dot_grid_gradient(x0, y1, x, y)
    n1 = dot_grid_gradient(x1, y1, x, y)
    ix1 = interpolate(n0, n1, sx)

    value = interpolate(ix0, ix1, sy)
    return value
