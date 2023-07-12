[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.10/)
[![codecov](https://codecov.io/gh/javidahmed64592/neuroevolution-flappy-bird/branch/main/graph/badge.svg?token=YGPGWHFMMG)](https://codecov.io/gh/javidahmed64592/neuroevolution-flappy-bird)
<!-- omit from toc -->
# Neuroevolution: Flappy Bird
A Pygame simulation of Flappy Bird, played by AI trained using neuroevolution.

<!-- omit from toc -->
## Table of Contents

- [Installing Dependencies](#installing-dependencies)
- [Running the Application](#running-the-application)
- [Configuring the Application](#configuring-the-application)
  - [Game Config](#game-config)
  - [GA Config](#ga-config)
  - [NN Config](#nn-config)
  - [Bird Config](#bird-config)
  - [Pipe Config](#pipe-config)
- [Testing](#testing)
- [Formatting, Type Checking and Linting](#formatting-type-checking-and-linting)

## Installing Dependencies

Install the required dependencies using [pipenv](https://github.com/pypa/pipenv):

    pipenv install
    pipenv install --dev

## Running the Application

Enter the virtual environment with

    pipenv shell

The application can then be started by running

    python main.py

This will open a Pygame window and begin the training. The application can be exited by closing the window.

## Configuring the Application

The application uses `.json` files to configure different aspects of the application.
These files are located in `/src/config`.

### Game Config

Configuring the Pygame window and application settings.

- `name`: Name of window
- `screen`: Pygame screen
  - `width`: Width of Pygame window in pixels
  - `height`: Height of Pygame window in pixels
- `fps`: Frames per second of application
- `font`: Text font
  - `font`: Font type
  - `size`: Font size

### GA Config

Configuring the genetic algorithm.

- `population_size`: Number of members in population
- `mutation_rate`: Probability for members' genes to mutate **[0, 1]**
- `max_score`: Number of seconds before game resets and next generation begins

### NN Config

Configuring the neural network.

- `input_layer`: Input layer of neural network
  - `name`: Name of input layer
  - `num_nodes`: Number of nodes in input layer
  - `activation`: Activation function (**linear**/**relu**/**sigmoid**)
- `output_layer`: Output layer of neural network
  - `name`: Name of output layer
  - `num_nodes`: Number of nodes in output layer
  - `activation`: Activation function (**linear**/**relu**/**sigmoid**)
- `hidden_layers`: List of layers with same properties as above
- `weights_range`: Range for random weights
  - `low`: Lower boundary
  - `high`: Upper boundary
- `bias_range`: Range for random biases
  - `low`: Lower boundary
  - `high`: Upper boundary

### Bird Config

Configuring the birds.

- `x`: x position of bird
- `y`: Starting y position of bird
- `width`: Width of bird
- `height`: Height of bird
- `grav`: Strength of gravity, higher for stronger gravity
- `lift`: Magnitude of bird's jump, lower for bigger jump
- `min_velocity`: Minimum velocity, lower for jumping quicker

### Pipe Config

Configuring the pipes.

- `start_spawnrate`: Rate at which pipes spawn initially, lower for quicker spawns
- `min_spawnrate`: Minimum delay between spawning of pipes
- `acc_spawnrate`: Rate at which spawn delay decreases per pipe
- `start_speed`: Starting speed of pipes
- `max_speed`: Max speed of pipes
- `acc_speed`: Rate at which pipe speed increases per pipe
- `width`: Width of pipes
- `spacing`: Spacing between top and bottom pipes

## Testing

This application uses Pytest for the unit tests.
These tests are located in the `tests` directory.
To run the tests:

    pipenv run test

This will generate code coverage reports in `xml` and `html` formats.

## Formatting, Type Checking and Linting

This application uses a number of tools for code formatting and linting. These tools are configured in `pyproject.toml`, `setup.cfg` and `mypy.ini`.

Black is used as a code formatter:

    black .

isort is used for tidying up imports:

    isort .

Mypy is used as a type checker:

    mypy .

Flake8 is used for linting:

    flake8
