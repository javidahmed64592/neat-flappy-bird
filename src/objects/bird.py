from typing import Any, Dict, List

import numpy as np
import pygame

from src.models.nn import NeuralNetwork
from src.objects.pipe import Pipe
from src.utils.pipe_utils import get_closest_pipe


class Bird:
    """
    This class creates a bird object which has a starting x and y position. The size of the bird is
    set using the width and height parameters.

    The bird is drawn to the display in the draw() method. The update() method performs physics
    calculations and updates the bird's position, velocity, and alive state accordingly. The bird
    dies if it collides with a pipe.

    The bird is assigned a neural network which acts as its brain and determines when the bird
    should 'jump' based on its current position and the position of the nearest pipe. This brain
    evolves via crossover and mutations. Its fitness value is the square of its score which is
    incremented by 1 each time the update() method is called.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        grav: float,
        lift: float,
        min_velocity: float,
        config_nn: Dict[str, Any],
    ):
        """
        Initialise bird with a starting position, a width and a height.

        Parameters:
            x (float): x coordinate of bird's start position
            y (float): y coordinate of bird's start position
            width (float): Width of bird
            height (float): Height of bird
            config_nn (Dict(str, Any)): Neural network config
        """
        self.x = x
        self.y = y
        self.start_y = y
        self.width = width
        self.height = height
        self.GRAV = grav
        self.LIFT = lift
        self.MIN_VELOCITY = min_velocity
        self.screen = pygame.display.get_surface()
        self.color = tuple(map(tuple, np.random.randint(low=0, high=256, size=(1, 3))))
        self.screen_width = self.screen.get_size()[0]
        self.screen_height = self.screen.get_size()[1]

        self.nn = NeuralNetwork.initialise_neural_network(
            config_nn,
        )

    @classmethod
    def create(cls, config_bird: Dict[str, Any], config_nn: Dict[str, Any]) -> "Bird":
        """
        Create a bird from config files.

        Parameters:
            config_bird (Dict(str, Any)): Bird configuration
            config_nn (Dict(str, Any)): Neural network configuration

        Returns:
            (Bird): Configured bird with neural network
        """
        bird = cls(
            config_bird["x"],
            config_bird["y"],
            config_bird["width"],
            config_bird["height"],
            config_bird["grav"],
            config_bird["lift"],
            config_bird["min_velocity"],
            config_nn,
        )
        bird.velocity = float(0)
        bird.alive = True
        bird.count = 0
        bird.rect = pygame.Rect(config_bird["x"], config_bird["y"], config_bird["width"], config_bird["height"])

        return bird

    def reset(self) -> None:
        """
        Reset bird's position, velocity and alive state to starting conditions.
        """
        self.y = self.start_y
        self.velocity = float(0)
        self.count = 0
        self.alive = True

    def kill(self) -> None:
        """
        Set bird's alive state to false.
        """
        self.alive = False

    def draw(self) -> None:
        """
        Draw bird on the display.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)

    def jump(self) -> None:
        """
        Make bird 'jump' by accelerating upwards.
        """
        self.velocity += self.LIFT

    def update(self, pipes: List[Pipe]) -> None:
        """
        Perform physics calculations on bird, check for collisions with pipe and update bird
        accordingly.

        Parameters:
            pipes (List(Pipe)): List of pipes currently on the display
        """
        if not self.alive:
            return

        if self.offscreen:
            self.kill()
            return

        inputs = [
            self.y / self.screen_height,
            self.velocity / self.MIN_VELOCITY,
            0,
            0,
            0,
        ]

        nearest_pipe = get_closest_pipe(pipes, self.x)
        if nearest_pipe is not None:
            if self.collide_with_pipe(nearest_pipe):
                self.kill()
                return
            else:
                inputs[2] = nearest_pipe.top / self.screen_height
                inputs[3] = nearest_pipe.bottom / self.screen_height
                inputs[4] = nearest_pipe.x / self.screen_width

        output = self.nn.feedforward(np.array(inputs))

        if output[0] > output[1]:
            self.jump()

        self.velocity += self.GRAV
        self.velocity = max(self.velocity, self.MIN_VELOCITY)
        self.y += self.velocity

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()
        self.count += 1

    def collide_with_pipe(self, pipe: Pipe) -> bool:
        """
        Check if bird is colliding with a pipe.

        Parameters:
            pipe (Pipe): Pipe to check collision against

        Returns:
            (bool): Is bird colliding with pipe?
        """
        return self.rect.colliderect(pipe.rect_top) or self.rect.colliderect(pipe.rect_bot)

    def crossover(self, parentA: "Bird", parentB: "Bird", mutation_rate: float) -> None:
        """
        Crossover the brains of two birds to mix their neural network weights and biases.

        Parameters:
            parentA (Bird): First bird to use for crossover
            parentB (Bird): Second bird to use for crossover
            mutation_rate (float): Probability for bird's genes to mutate, range [0, 1]
        """
        self.nn.crossover(parentA.nn, parentB.nn, mutation_rate)

    def apply(self) -> None:
        """
        Overwrite bird's brain with new brain generated from crossover.
        """
        self.nn.apply()

    @property
    def offscreen(self) -> bool:
        """
        Returns if bird is offscreen.

        Returns:
            (bool): Is bird offscreen?
        """
        return self.y > self.screen_height - self.height or self.y < 0

    @property
    def score(self) -> int:
        """
        Return the bird's count after normalisation.

        Returns:
            (int): Bird's count after normalisation
        """
        return int(self.count / 60)

    @property
    def fitness(self) -> int:
        """
        Return the square of bird's score.

        Returns:
            (int): score squared
        """
        return (self.score) ** 2
