import pytest
from unittest.mock import patch
import pygame
from src.objects.bird import Bird
from src.objects.pipe import Pipe

TEST_SCREEN_SIZE = [700, 700]
TEST_SCREEN = pygame.display.set_mode((TEST_SCREEN_SIZE[0], TEST_SCREEN_SIZE[1]))
TEST_COLOR = (255, 0, 0)
TEST_CONFIG_BIRD = {"x": 30, "y": 400, "width": 40, "height": 40, "grav": 1, "lift": -20, "min_velocity": -10}
TEST_INPUT_LAYER = {"name": "Input", "num_nodes": 5, "activation": "linear"}
TEST_HIDDEN_LAYER = {"name": "Hidden", "num_nodes": 3, "activation": "relu"}
TEST_OUPUT_LAYER = {"name": "Output", "num_nodes": 2, "activation": "linear"}
TEST_CONFIG_NN = {
    "input_layer": TEST_INPUT_LAYER,
    "output_layer": TEST_OUPUT_LAYER,
    "hidden_layers": [TEST_HIDDEN_LAYER],
}
TEST_CONFIG_PIPE = {
    "start_spawnrate": 80.9,
    "min_spawnrate": 35,
    "acc_spawnrate": 0.1,
    "start_speed": 3.5,
    "max_speed": 11,
    "acc_speed": 0.03,
    "width": 50,
    "spacing": 220,
}


@pytest.fixture
def test_bird():
    with patch("pygame.display.get_surface", return_value=TEST_SCREEN):
        yield Bird.create(TEST_CONFIG_BIRD, TEST_CONFIG_NN)


@pytest.fixture
def test_pipe():
    with patch("pygame.display.get_surface", return_value=TEST_SCREEN):
        yield Pipe.create(TEST_CONFIG_PIPE, TEST_CONFIG_PIPE["start_speed"])
