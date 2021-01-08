"""test calculation of coordinates and shortest paths"""
import os

import pytest

from casymda.blocks.tilemap.coordinates_holder import CoordinatesHolder, delete_cached

CSV_FILE = "6x6_ABC.csv"
directory = os.path.dirname(__file__)
csv_path = os.path.join(directory, CSV_FILE)

SCALE = 10


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    delete_cached(csv_path)


def test_nodes_coordinates():
    coordinates_holder = CoordinatesHolder(
        csv_path, scale=SCALE, include_diagonal=False
    )

    x, y = coordinates_holder.get_coords("A")
    assert x == 0 + SCALE / 2
    assert y == 0 + SCALE / 2

    x, y = coordinates_holder.get_coords("B")
    assert x == 50 + SCALE / 2
    assert y == 0 + SCALE / 2

    x, y = coordinates_holder.get_coords("C")
    assert x == 50 + SCALE / 2
    assert y == 50 + SCALE / 2


def test_paths_lengths_steps_A_B():
    coordinates_holder = CoordinatesHolder(csv_path, scale=SCALE)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "A", "B"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 50
    assert steps == 5


def test_paths_lengths_steps_A_C():
    coordinates_holder = CoordinatesHolder(csv_path, scale=SCALE)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "A", "C"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 200
    assert steps == 20


def test_paths_lengths_steps_C_B():
    coordinates_holder = CoordinatesHolder(csv_path, scale=SCALE)

    coords_path, length = coordinates_holder.get_path_coords_and_length_from_to(
        "C", "B"
    )
    steps = len(coords_path) - 1  # without starting node
    assert length == 150
    assert steps == 15
