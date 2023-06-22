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
    "width": 50,
    "spacing": 200,
}

TEST_PIPE_SPEED = 3.5


@pytest.fixture
def test_bird():
    with patch("pygame.display.get_surface", return_value=TEST_SCREEN):
        yield Bird.create(TEST_CONFIG_BIRD, TEST_CONFIG_NN)


@pytest.fixture
def test_pipe():
    with patch("pygame.display.get_surface", return_value=TEST_SCREEN):
        yield Pipe.create(TEST_CONFIG_PIPE, TEST_PIPE_SPEED)
