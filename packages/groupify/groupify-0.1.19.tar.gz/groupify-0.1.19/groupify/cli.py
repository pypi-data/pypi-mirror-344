import argparse
from tabulate import tabulate
from .make_random_groups import (
    read_class_list,
    generate_random_groups,
    visualize_groups,
    show,
    remove_names,
)


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
        "--names",
        metavar="N",
        type=str,
        nargs="+",
        help="Names to remove from class list. Separate names with spaces. Such as: Mary Christian Gunnar",
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

    if args.names:
        names = remove_names(names, args.names)

    groups = generate_random_groups(names, args.size)

    group_table = [[f"{i}", ", ".join(g)] for i, g in enumerate(groups, 1)]
    print(tabulate(group_table, headers=["Group", "Members"], tablefmt="grid"))

    if args.show:
        fig, ax = visualize_groups(groups)
        show()
