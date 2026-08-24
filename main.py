import argparse

from generate_rooms import generate_rooms
from matrix2d import print_matrix2d


def main(w: int, h: int, room_count: int, seed: int | None, min_size: int, max_size: int):
    """Generate dungeon with given parameters and print."""
    dungeon = generate_rooms(
        w=w,
        h=h,
        room_count=room_count,
        seed=seed,
        min_size=min_size,
        max_size=max_size
        )
    print(f"width={w}, height={h}, room_count={room_count}, seed={seed}, min_size={min_size}, max_size={max_size}")
    print_matrix2d(dungeon)


def parse_args():
    """Parse and return cli arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", "-W", type=int, default = 100, help="Map width")
    parser.add_argument("--height", "-H", type=int, default = 100, help="Map height")
    parser.add_argument("--room_count", "-R", type=int, default = 30, help="Room count")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed (optional)")
    parser.add_argument("--min_size", "-m", type=int, default = 5, help="Minimum size of rooms (optional)")
    parser.add_argument("--max_size", "-M", type=int, default = 20, help="Maximum size of rooms (optional)")
    return parser.parse_args()


def cli():
    """Entry point to parse cli arguments and call main function"""
    args = parse_args()
    main(args.width,
         args.height,
         args.room_count,
         args.seed,
         args.min_size,
         args.max_size)


if __name__ == "__main__":
    cli()