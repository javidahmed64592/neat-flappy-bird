from .defaults import *  # noqa: F401, F403

GAME = {
    "name": "Flappy Bird with Neuroevolution",
    "screen": {"width": 700, "height": 700},
    "fps": 60,
    "font": {"font": "freesansbold.ttf", "size": 28},
}

GA = {"population_size": 10, "mutation_rate": 0.05, "max_score": 100}

NN = {
    "input_layer": {"name": "Input", "num_nodes": 5, "activation": "linear"},
    "output_layer": {"name": "Output", "num_nodes": 2, "activation": "linear"},
    "hidden_layers": [{"name": "Hidden", "num_nodes": 3, "activation": "relu"}],
}

BIRD = {"x": 30, "y": 400, "width": 40, "height": 40, "grav": 1, "lift": -20, "min_velocity": -10}

PIPE = {
    "width": 50,
    "spacing": 200,
    "color": (0, 255, 0),
    "speed": 3.5,
    "start_speed": 3.5,
    "start_spawnrate": 90,
    "acc_speed": 0.03,
    "min_spawnrate": 35,
    "acc_spawnrate": 0.1,
    "start_speed": 3.5,
    "max_speed": 11,
}
