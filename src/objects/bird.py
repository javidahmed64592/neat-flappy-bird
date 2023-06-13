from __main__ import data, nn_data
import numpy as np
from typing import List
import pygame

from objects.pipe import Pipe

from models.nn import NeuralNetwork


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

    GRAV = data["bird"]["grav"]
    LIFT = data["bird"]["lift"]
    MIN_VELOCITY = data["bird"]["min_velocity"]

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialise bird with a starting position, a width and a height.

        Parameters:
            x (float): x coordinate of bird's start position
            y (float): y coordinate of bird's start position
            width (float): Width of bird
            height (float): Height of bird
        """
        self.screen = pygame.display.get_surface()
        self.width = width
        self.height = height
        self.x = x
        self.start_y = y
        self.y = y
        self.velocity = 0
        self.alive = True
        self.count = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = tuple(np.random.randint(low=0, high=256, size=(1, 3)))

        self.screen_width = self.screen.get_size()[0]
        self.screen_height = self.screen.get_size()[1]

        self.nn = NeuralNetwork(
            nn_data["layers"],
        )

    def reset(self):
        """
        Reset bird's position, velocity and alive state to starting conditions.
        """
        self.y = self.start_y
        self.velocity = 0
        self.count = 0
        self.alive = True

    def kill(self):
        """
        Set bird's alive state to false.
        """
        self.alive = False

    def draw(self):
        """
        Draw bird on the display.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)

    def jump(self):
        """
        Make bird 'jump' by accelerating upwards.
        """
        self.velocity += self.LIFT

    def update(self, pipes: List[Pipe]):
        """
        Perform physics calculations on bird, check for collisions with pipe and update bird
        accordingly.

        Parameters:
            pipes (List(Pipe)): List of pipes currently on the display
        """
        if not self.alive:
            return

        if self.y > self.screen_height - self.height or self.y < 0:
            self.kill()
            return

        inputs = [
            self.y / self.screen_height,
            self.velocity / self.MIN_VELOCITY,
            0,
            0,
            0,
        ]

        nearest_pipe = Pipe.get_closest_pipe(pipes, self.x)
        if nearest_pipe is not None:
            if self.rect.colliderect(nearest_pipe.rect_top) or self.rect.colliderect(
                nearest_pipe.rect_bot
            ):
                self.kill()
                return
            else:
                inputs[2] = nearest_pipe.top / self.screen_height
                inputs[3] = nearest_pipe.bottom / self.screen_height
                inputs[4] = nearest_pipe.x / self.screen_width

        output = self.nn.feedforward(inputs)

        if output[0] > output[1]:
            self.jump()

        self.velocity += self.GRAV
        self.velocity = max(self.velocity, self.MIN_VELOCITY)
        self.y += self.velocity

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()
        self.count += 1

    def crossover(self, parentA: "Bird", parentB: "Bird", mutation_rate: float):
        """
        Crossover the brains of two birds to mix their neural network weights and biases.

        Parameters:
            parentA (Bird): First bird to use for crossover
            parentB (Bird): Second bird to use for crossover
            mutation_rate (float): Probability for bird's genes to mutate, range [0, 1]
        """
        self.nn.crossover(parentA.nn, parentB.nn, mutation_rate)

    def apply(self):
        """
        Overwrite bird's brain with new brain generated from crossover.
        """
        self.nn.apply()

    @property
    def score(self) -> int:
        """
        Return the bird's count after normalisation.
        """
        return int(self.count / 60)

    @property
    def fitness(self) -> int:
        """
        Return the square of bird's score.
        """
        return (self.score) ** 2
