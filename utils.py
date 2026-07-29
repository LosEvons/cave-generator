# Converts an (x,y) coordinate to an int index in a one dimensional coordinate system.
def xy_to_i(x: int, y: int, width: int) -> int:
    return y * width + x

# Converts an int index from a one dimensional coordinate system to an (x,y) coordinate.
def i_to_xy(i: int, width: int) -> tuple[int, int]:
    return i % width, i // width
