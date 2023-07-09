from unittest.mock import patch

import pygame
import pytest

from src.objects.bird import Bird
from src.objects.pipe import Pipe

TEST_INPUT_LAYER = {"name": "Input", "num_nodes": 5, "activation": "linear"}
TEST_HIDDEN_LAYER = {"name": "Hidden", "num_nodes": 3, "activation": "relu"}
TEST_OUPUT_LAYER = {"name": "Output", "num_nodes": 2, "activation": "linear"}


@pytest.fixture
def test_config_bird():
    return {"x": 30, "y": 400, "width": 40, "height": 40, "grav": 1, "lift": -20, "min_velocity": -10}


@pytest.fixture
def test_config_nn():
    return {"input_layer": TEST_INPUT_LAYER, "output_layer": TEST_OUPUT_LAYER, "hidden_layers": [TEST_HIDDEN_LAYER]}


@pytest.fixture
def test_config_pipe():
    return {"width": 50, "spacing": 200, "color": (0, 255, 0)}


@pytest.fixture
def test_screen_size():
    return (700, 700)


@pytest.fixture
def test_screen(test_screen_size):
    return pygame.display.set_mode(test_screen_size)


@pytest.fixture
def test_bird(test_config_bird, test_config_nn, test_screen):
    with patch("pygame.display.get_surface", return_value=test_screen):
        yield Bird.create(test_config_bird, test_config_nn)


@pytest.fixture
def test_pipe(test_config_pipe, test_screen):
    with patch("pygame.display.get_surface", return_value=test_screen):
        yield Pipe.create(test_config_pipe, 3.5)
