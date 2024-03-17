from unittest.mock import patch

import pygame
import pytest
from dotenv import load_dotenv

from src.app import App
from src.ga.ga import Population
from src.objects.bird import Bird
from src.objects.pipe import Pipe
from src.utils.config_utils import get_config_module

load_dotenv()

config = get_config_module("src.config.test")


@pytest.fixture
def mock_config():
    return config


@pytest.fixture
def mock_screen_size():
    return (700, 700)


@pytest.fixture
def mock_screen(mock_screen_size):
    return pygame.display.set_mode(mock_screen_size)


@pytest.fixture
def mock_bird(mock_config):
    return Bird.create(mock_config.BIRD, mock_config.NN)


@pytest.fixture
def mock_bird_low_score(mock_config, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        bird = Bird.create(mock_config.BIRD, mock_config.NN)
        bird.count = 100
        return bird


@pytest.fixture
def mock_bird_mid_score(mock_config, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        bird = Bird.create(mock_config.BIRD, mock_config.NN)
        bird.count = 400
        return bird


@pytest.fixture
def mock_bird_high_score(mock_config, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        bird = Bird.create(mock_config.BIRD, mock_config.NN)
        bird.count = 900
        return bird


@pytest.fixture
def mock_pipe(mock_config, mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        return Pipe.create(mock_config.PIPE, 3.5)


@pytest.fixture
def mock_population(mock_bird_low_score, mock_bird_mid_score, mock_bird_high_score):
    return Population([mock_bird_low_score, mock_bird_mid_score, mock_bird_high_score])


@pytest.fixture
def mock_app(mock_screen):
    with patch("pygame.display.get_surface", return_value=mock_screen):
        return App.create_app(config)
