"""Read-only native terrain-conveyor model for the reviewed Devon solvers."""

def terrain_conveyors(model):
    width, height = model['width'], model['height']
    data, tags = model['data']['data'], model['terrain']['data']
    result = {}
    for y in range(height):
        for x in range(width):
            tag = 0
            for z in (2, 1, 0):
                value = tags[data[x + width*y + width*height*z]]
                if value:
                    tag = value
                    break
            if tag in (20, 21, 22, 23):
                result[(x, y)] = {20:'down', 21:'left', 22:'right', 23:'up'}[tag]
    return result
