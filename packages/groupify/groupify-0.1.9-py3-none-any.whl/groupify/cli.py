import argparse
from .make_random_groups import read_class_list, generate_random_groups, show


def main():
    parser = argparse.ArgumentParser(
        prog="groupify", description="Split a list of names into random groups"
    )
    parser.add_argument(
        "-f", "--file", required=True, help="one‑name‑per‑line input file"
    )
    parser.add_argument(
        "-sz", "--size", type=int, default=4, help="group size (default 4)"
    )

    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        if v.lower() in ("no", "false", "f", "n", "0"):
            return False
        raise argparse.ArgumentTypeError("Boolean value expected.")

    parser.add_argument(
        "--show",
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        help="Show the plot (default: true). Pass --show false to disable.",
    )

    args = parser.parse_args()

    names = read_class_list(args.file)
    groups = generate_random_groups(names, args.size)

    for i, g in enumerate(groups, 1):
        print(f"Group {i}: {', '.join(g)}")

    if args.show:
        show()
