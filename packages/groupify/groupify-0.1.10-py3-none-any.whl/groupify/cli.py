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

    parser.add_argument(
        "--show",
        dest="show",
        action="store_true",
        help="Display the plot (this is the default)",
    )
    parser.add_argument(
        "--no-show", dest="show", action="store_false", help="Do not display the plot"
    )
    parser.set_defaults(show=True)

    args = parser.parse_args()

    names = read_class_list(args.file)
    groups = generate_random_groups(names, args.size)

    for i, g in enumerate(groups, 1):
        print(f"Group {i}: {', '.join(g)}")

    if args.show:
        show()
