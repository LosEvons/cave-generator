def xy_to_i(x: int, y: int, width: int) -> int:
    return y * width + x

def i_to_xy(i: int, width: int) -> tuple[int, int]:
    return i % width, i // width