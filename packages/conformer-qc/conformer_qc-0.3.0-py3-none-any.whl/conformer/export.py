#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None
import json
from collections import defaultdict
from itertools import cycle, product
from typing import Iterable

import numpy as np

from conformer.common import PHYSICAL_ATOM, role_to_str
from conformer.spatial import bonding_graph, bonding_radius
from conformer.systems import Atom, NamedSystem, System


def to_xyz_str(sys: System):
    """
    Dumps atom to xyz file with correct metadata
    """
    # Load metadata that can't be represented in XYZ file
    charges = {}
    roles = {}
    coord_strs = []

    # Use 1-based indexing for public-facing code
    for i, a in enumerate(sys, 1):
        if a.charge != 0:
            charges[i] = int(a.charge)
        if a.role != PHYSICAL_ATOM:
            roles[i] = role_to_str(a.role)
        coord_strs.append(
            f"{a.t:<4s}  {a.r[0]:> 17.10f} {a.r[1]:> 17.10f} {a.r[2]:> 17.10f}"
        )

    # Load into JSON serlializable metadata
    meta = {}
    if sys.unit_cell is not None:
        meta["unit_cell"] = list(sys.unit_cell)
    if charges:
        meta["charges"] = charges
    if roles:
        meta["roles"] = roles
    if isinstance(sys, NamedSystem):
        meta["name"] = sys.name
        meta["meta"] = sys.meta

    # Create output
    xyz = [
        str(sys.size),
        json.dumps(meta) if meta else "",
    ]
    xyz.extend(coord_strs)

    return "\n".join(xyz)


# TODO: Choose nicer colors.
# Roughly follows https://en.wikipedia.org/wiki/CPK_coloring
OTHER_COLOR = "pink"
COLORS = defaultdict(lambda: OTHER_COLOR)
COLORS.update(
    {
        "H": "white",
        "C": "dimgray",
        "N": "blue",
        "O": "red",
        "F": "green",
        "Cl": "green",
        "Br": "brown",
        "I": "purple",
        "S": "yellow",
        "P": "orange",
        "B": "tan",
        "Li": "violet",
        "Na": "violet",
        "K": "violet",
        "Rb": "violet",
        "Cs": "violet",
        "Fr": "violet",
        "Be": "darkgreen",
        "Mg": "darkgreen",
        "Ca": "darkgreen",
        "Sr": "darkgreen",
        "Ba": "darkgreen",
        "Ra": "darkgreen",
        "Fe": "darkorange",
        "Ag": "silver",
        "Au": "gold",
        "Ti": "slategray",
        "Cu": "goldenrod",
        "Co": "steelblue",
        "He": "cyan",
        "Ne": "cyan",
        "Ar": "cyan",
        "Kr": "cyan",
        "Xe": "cyan",
    }
)


SELECTION_COLORS = [
    "paleturquoise",
    "pink",
    "palegreen",
    "gold",
    "thistle",
    "lightcoral",
    "sandybrown" # Wow, you've made it this far...
]


def visualize(
    sys: System,
    selection: Iterable[Atom] | list[System] | None=None,
    show_idxs=True,
    size_scale=7.5,
    ghost_alpha=0.4,
    draw_bonds=True,
    view=tuple[int, ...] | str | None, 
    palette=COLORS,
    show=True
):
    """
    Plots the system in a matplot lib window
    """
    if plt is None:
        raise ModuleNotFoundError("Please install Matplotlib to use `visualize`")

    if not isinstance(palette, defaultdict):
        raise ValueError("`palette` must be a `defaultdict`")

    # TODO: Make this easier to integrate with other plots
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Hide background
    ax.set_axis_off()

    # Create a bounding box to keep the 1:1:1 aspect ratio
    geom_mean = sys.r_matrix.mean(axis=0)
    bb_span = np.max(sys.r_matrix.max(axis=0) - sys.r_matrix.min(axis=0)) / 2
    bb_coords = np.zeros((8, 3))

    for i, (dx, dy, dz) in enumerate(
        product(
            [-bb_span, bb_span],
            [-bb_span, bb_span],
            [-bb_span, bb_span],
        )
    ):
        bb_coords[i, :] = geom_mean[0] + dx, geom_mean[1] + dy, geom_mean[2] + dz

    # Create the figure and the axis
    ax.scatter(*bb_coords.T, s=0)

    G = bonding_graph(sys)

    # Plot bonds
    if draw_bonds:
        for u, v in G.edges():
            if not u.is_physical or not v.is_physical:
                continue
            r = np.vstack([u.r, v.r])
            ax.plot(*r.T, c="black", zorder=0.5)

    # Plot atoms
    for i, a in enumerate(sys):
        r = np.reshape(a.r, (3, 1))
        # Make atoms proportional to vDW radii
        s = (bonding_radius(a) * size_scale) ** 2 * np.pi
        alpha = 1.0 if a.is_physical else ghost_alpha
        c = palette[a.t]
        ax.scatter(*r, c=c, s=s, edgecolors="black", alpha=alpha, zorder=50)

    # Plot atom IDs
    if show_idxs:
        for i, a in enumerate(sys):
            ax.text(
                *a.r,
                i,
                None,
                zorder=100,
                horizontalalignment="center",
                verticalalignment="center",
            )

    # Plot the given selection(s)
    if selection:
    # This is a hack to differentiate a list of systems vs a list of atoms
    # Python it not setup to handle this task gracefully
        if isinstance(selection, list) and isinstance(selection[0], System):
            selections = selection
        else:
            selections = [selection] # Assume only a single system was provided

        for color, _selection in zip(cycle(SELECTION_COLORS), selections):
            for a in _selection:
                r = np.reshape(a.r, (3, 1))
                # Make the selection larger than the atom marker
                s = (bonding_radius(a) * size_scale * 3) ** 2 * np.pi
                ax.scatter(*r, c=color, s=s, edgecolors="none", alpha=0.5, zorder=25)

    # Handle camera positioning
    if isinstance(view, tuple):
        if len(view) == 2:
            elev, azim = view
            roll=0
        elif len(view) == 3:
            elev, azim, roll = view
        else:
            raise ValueError("View must provide elev, azim, with an optional roll parameter")

        ax.view_init(elev=elev, azim=azim, roll=roll)
    elif isinstance(view, str):
        # See https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.view_init.html#mpl_toolkits.mplot3d.axes3d.Axes3D.view_init
        vs = view.lower()
        roll = 0
        if vs == "xy":
            elev = 90
            azim = -90
        elif vs == "xz":
            elev = 0
            azim = -90
        elif vs == "yz":
            elev = 0
            azim = 0
        elif vs == "-xy":
            elev = -90
            azim = 90
        elif vs == "-xz":
            elev = 0
            azim = 90
        elif vs == "-yz":
            elev = 0
            azim = 180
        else:
            raise ValueError("Unknow orientation \"{view}\"")
        ax.view_init(elev=elev, azim=azim)

    if show:
        plt.show()

    return fig
