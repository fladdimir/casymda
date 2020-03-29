"""test calculation of coordinates and shortest paths"""
import os

from casymda.blocks.tilemap.coordinates_holder import CoordinatesHolder, delete_cached
import pytest

CSV_FILE = "6x6_ABC.csv"
directory = os.path.dirname(__file__)
csv_path = os.path.join(directory, CSV_FILE)

SCALE = 1


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    delete_cached(csv_path)


def test_nodes_coordinates():
    coordinates_holder = CoordinatesHolder(
        csv_path, scale=SCALE, include_diagonal=False
    )

    # (remember that the center of the tile is the aim)
    x, y = coordinates_holder.get_coords("A")
    assert x == 0 + SCALE / 2
    assert y == 0 + SCALE / 2

    x, y = coordinates_holder.get_coords("B")
    assert x == 5 + SCALE / 2
    assert y == 0 + SCALE / 2

    x, y = coordinates_holder.get_coords("C")
    assert x == 5 + SCALE / 2
    assert y == 5 + SCALE / 2


def test_paths_lengths_steps_A_A():
    coordinates_holder = CoordinatesHolder(csv_path, scale=1, include_diagonal=False)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "A", "A"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 0
    assert steps == 1  # one step to target (which has the same position)


def test_paths_lengths_steps_A_B():
    coordinates_holder = CoordinatesHolder(csv_path, scale=1, include_diagonal=False)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "A", "B"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 5
    assert steps == 5


def test_paths_lengths_steps_A_C():
    coordinates_holder = CoordinatesHolder(csv_path, scale=1, include_diagonal=False)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "A", "C"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 20
    assert steps == 20


def test_paths_lengths_steps_C_B():
    coordinates_holder = CoordinatesHolder(csv_path, scale=1, include_diagonal=False)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "C", "B"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 15
    assert steps == 15
