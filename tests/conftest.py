from unittest.mock import patch

import pygame
import pytest

from src.models.ga import Population
from src.objects.bird import Bird
from src.objects.pipe import Pipe

MOCK_INPUT_LAYER = {"name": "Input", "num_nodes": 5, "activation": "linear"}
MOCK_HIDDEN_LAYER = {"name": "Hidden", "num_nodes": 3, "activation": "relu"}
MOCK_OUPUT_LAYER = {"name": "Output", "num_nodes": 2, "activation": "linear"}


@pytest.fixture
def mock_config_bird():
    return {"x": 30, "y": 400, "width": 40, "height": 40, "grav": 1, "lift": -20, "min_velocity": -10}


@pytest.fixture
def mock_config_nn():
    return {"input_layer": MOCK_INPUT_LAYER, "output_layer": MOCK_OUPUT_LAYER, "hidden_layers": [MOCK_HIDDEN_LAYER]}


@pytest.fixture
def mock_config_pipe():
    return {"width": 50, "spacing": 200, "color": (0, 255, 0)}


@pytest.fixture
def mock_screen_size():
    return (700, 700)


@pytest.fixture
def mock_screen(mock_screen_size):
    return pygame.display.set_mode(mock_screen_size)


@pytest.fixture
def mock_bird(mock_config_bird, mock_config_nn, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        return Bird.create(mock_config_bird, mock_config_nn)


@pytest.fixture
def mock_bird_low_score(mock_config_bird, mock_config_nn, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        bird = Bird.create(mock_config_bird, mock_config_nn)
        bird.count = 100
        return bird


@pytest.fixture
def mock_bird_mid_score(mock_config_bird, mock_config_nn, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        bird = Bird.create(mock_config_bird, mock_config_nn)
        bird.count = 400
        return bird


@pytest.fixture
def mock_bird_high_score(mock_config_bird, mock_config_nn, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        bird = Bird.create(mock_config_bird, mock_config_nn)
        bird.count = 900
        return bird


@pytest.fixture
def mock_pipe(mock_config_pipe, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        yield Pipe.create(mock_config_pipe, 3.5)


@pytest.fixture
def mock_population(mock_bird_low_score, mock_bird_mid_score, mock_bird_high_score):
    return Population([mock_bird_low_score, mock_bird_mid_score, mock_bird_high_score])
