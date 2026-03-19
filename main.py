import argparse

from generate_rooms import generate_rooms
from matrix2d import print_matrix2d


def main(w: int, h: int, room_count: int, seed: int | None):
    dungeon = generate_rooms(
        w=w,
        h=h,
        room_count=room_count,
        seed=seed
        )
    print(f"width={w}, height={h}, room_count={room_count} seed={seed}")
    print_matrix2d(dungeon)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", "-W", type=int, default = 100, help="Map width")
    parser.add_argument("--height", "-H", type=int, default = 100, help="Map height")
    parser.add_argument("--room_count", "-R", type=int, default = 10, help="Room count")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed (optional)")
    return parser.parse_args()


def cli():
    args = parse_args()
    main(args.width,
         args.height,
         args.room_count,
         args.seed)


if __name__ == "__main__":
    cli()