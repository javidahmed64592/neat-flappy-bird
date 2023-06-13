import numpy as np
from typing import List
import pygame


class Pipe:
    """
    This class creates a top pipe and bottom pipe pair which has a width, a spacing between the two
    pipes, and a speed at which to travel across the screen.

    The pipe is drawn to the display in the draw() method. The update() method moves the pipe along
    the screen.

    The pipes have an offscreen property which indicates whether or not the pipes have moved off
    the screen and get destroyed if they have since they are no longer needed. The
    get_closest_pipe() method takes a list of pipe pairs and determines which pipe pair is both
    closest to and in front of the birds on the screen.
    """

    def __init__(self, width: float = 50, spacing: float = 200, speed: float = 3.5):
        """
        Initialise a pipe pair with a width, spacing and speed.

        Parameters:
            width (float): Width of the top and bottom pipes
            spacing (float): Space between top and bottom pipe
            speed (float): Speed at which the pipes move across the screen
        """
        self.screen = pygame.display.get_surface()
        self.spacing = spacing
        self.top = np.random.uniform(
            (1 / 5) * (self.screen.get_size()[1] - self.spacing),
            (4 / 5) * (self.screen.get_size()[1] - self.spacing),
        )
        self.bottom = self.screen.get_size()[1] - (self.top + self.spacing)
        self.x = self.screen.get_size()[0]
        self.width = width
        self.speed = speed
        self.rect_top = pygame.Rect(self.x, 0, self.width, self.top)
        self.rect_bot = pygame.Rect(
            self.x, self.top + self.spacing, self.width, self.bottom
        )
        self.color = (0, 255, 0)

    def draw(self):
        """
        Draw the pipes on the display.
        """
        pygame.draw.rect(self.screen, self.color, self.rect_top)
        pygame.draw.rect(self.screen, self.color, self.rect_bot)

    def update(self):
        """
        Move the pipes along the screen.
        """
        self.x -= self.speed

        self.rect_top = pygame.Rect(self.x, 0, self.width, self.top)
        self.rect_bot = pygame.Rect(
            self.x, self.top + self.spacing, self.width, self.bottom
        )

        self.draw()

    @property
    def offscreen(self) -> bool:
        """
        Return whether or not the pipes have moved off the screen.
        """
        return self.x < -self.width

    @staticmethod
    def get_closest_pipe(pipes: List["Pipe"], bird_pos_x: float) -> "Pipe":
        """
        Determine which pipe pair is closest to and in front of the birds.

        Parameters:
            pipes (List(Pipe)): List of pipe pairs currently on screen
            bird_pos_x (float): x position of the birds

        Returns:
            closest (Pipe): Pipe closest to the birds
        """
        dist = np.inf
        closest = None

        for pipe in pipes:
            pipe_dist = pipe.x + pipe.width - bird_pos_x
            if 0 < pipe_dist < dist:
                dist = pipe_dist
                closest = pipe

        return closest
