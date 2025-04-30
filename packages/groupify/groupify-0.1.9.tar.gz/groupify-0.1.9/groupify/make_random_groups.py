import pathlib
import random
import matplotlib.pyplot as plt
from math import ceil
import seaborn as sns

from typing import List


def read_class_list(filename):
    """Reads a class list from a file and returns a list of names

    Args:
        filename (str): Filename of class list

    Returns:
        List[str]: List of names

    """
    class_list = []
    with open(filename) as f:
        for line in f:
            class_list.append(line.strip())
    return class_list


def remove_names(class_list, names):
    """Removes names from a class list

    Args:
        class_list (List[str]): List of names
        names (List[str]): Names to remove from class list

    Returns:
        List[str]: List of names with names removed
    """

    for name in names:
        try:
            class_list.remove(name)
        except:
            raise ValueError(f"{name} is not in the class list.")
    return class_list


def generate_random_groups(class_list, group_size):
    """Generates random groups from a class list


    Args:
        class_list (List[str]): List of names
        group_size (int): Size of each group

    Returns:
        list[List[str]]: List of groups

    """
    random.seed()

    random.shuffle(class_list)
    num_groups = len(class_list) // group_size

    # If there are more students than there is place for in the set number of groups
    if len(class_list) % group_size != 0:
        num_groups += 1

    # Deler ut elever som en kortstokk
    groups = [[] for _ in range(num_groups)]
    while len(class_list) > 0:
        for group in groups:
            if len(class_list) > 0:
                group.append(class_list.pop())
            else:
                break
    return groups


def create(classlist, absent=None, group_size=4):
    """Creates a set of random groups with a specific group size.

    Args:
        classlist (str or list):
            .txt file with classlist or a list with names.
        absent (list(str)):
            list of absent participants to remove from the classlist
        group_size (int):
            Number of students per group. Default: `4`.
            Must be a number between 1 and 4 (inclusive).

    Returns:
        fig (matplotlib.pyplot.Figure)
        ax (maplotlib.pyplot.Axes)


    """
    if group_size is not None:
        if not (0 < group_size <= 4):
            raise ValueError(
                f"Group size {group_size} must be at least 1 and maximally 4."
            )

    if isinstance(classlist, str):
        class_list = read_class_list(filename=classlist)

    if absent is not None:
        class_list = remove_names(class_list, absent)

    groups = generate_random_groups(class_list, group_size)

    fig, ax = visualize_groups(groups)
    return fig, ax


def visualize_groups(groups):
    # Define the size of the figure
    fig, ax = plt.subplots(figsize=(14, 8))

    # Define the number of rows and columns based on group number
    n_rows = ceil(len(groups) / 2)
    n_cols = 2

    # Define the size of each cell based on number of rows and columns
    cell_size_x = 1.0 / n_cols
    cell_size_y = 1.0 / n_rows

    # Get a color palette
    colors = sns.color_palette("hls", len(groups))
    # colors = sns.color_palette("husl", len(groups))

    # Loop through each group
    for i, group in enumerate(groups):
        # Calculate the row and column number
        row = i // n_cols
        col = i % n_cols

        # Calculate the position of the bottom-left corner of the rectangle
        bottom_left_x = col * cell_size_x
        bottom_left_y = (n_rows - 1 - row) * cell_size_y

        # Create the rectangle
        rectangle = plt.Rectangle(
            (bottom_left_x, bottom_left_y),
            cell_size_x,
            cell_size_y,
            fill=True,
            color=colors[i],
            edgecolor="black",
            lw=2,
            alpha=0.3,
        )
        ax.add_patch(rectangle)

        # Calculate the center position of the rectangle
        center_x = bottom_left_x + cell_size_x / 2
        center_y = bottom_left_y + cell_size_y / 2

        # Add the group number to the center of the rectangle
        ax.text(
            center_x,
            center_y,
            f"{i+1}",
            ha="center",
            va="center",
            fontsize=20,
            bbox=dict(facecolor="white", alpha=0.5),
        )

        # Positions of names in the sub-rectangles of the rectangle
        positions = [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]

        # Add the individuals to the rectangle
        for j, individual in enumerate(group):
            pos_x = positions[j][0] * cell_size_x + bottom_left_x
            pos_y = positions[j][1] * cell_size_y + bottom_left_y
            ax.text(
                pos_x,
                pos_y,
                individual,
                ha="center",
                va="center",
                fontsize=20,
                bbox=dict(facecolor="white", alpha=0.5),
            )

    # Remove the axis
    ax.axis("off")
    group_size = max([len(group) for group in groups])
    # plt.title(f"{group_size}", fontsize=25, weight="bold")

    return fig, ax


def savefig(dirname, fname):
    dir = pathlib.Path(dirname)
    dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{dir}/{fname}")

    return None


def show():
    plt.show()
