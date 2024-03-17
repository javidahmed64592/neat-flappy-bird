import sys
from typing import Any

import pygame
from pygame.locals import QUIT

from src.ga.ga import Population
from src.objects.bird import Bird
from src.objects.pipe import Pipe


class App:
    """
    This class creates a Pygame instance and runs the application. The screen dimensions are
    defined in the __init__ method, and the pipes are also configured in that method. A population
    is created in the create_population method. Helper methods have been defined to write text
    to the screen to display the game statistics. Calling the run method starts the application.
    """

    pygame.init()
    FramePerSec = pygame.time.Clock()

    def __init__(self, config: Any):
        """
        Configure the game window.

        Parameters:
            config (Any): Dictionary of app configuration
        """
        self.config = config

        self.FONT = pygame.font.SysFont(config.GAME["font"]["font"], config.GAME["font"]["size"])
        self.FPS = config.GAME["fps"]

        self.screen_width = config.GAME["screen"]["width"]
        self.screen_height = config.GAME["screen"]["height"]

        self.display_surf = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.name = config.GAME["name"]
        pygame.display.set_caption(self.name)

        self.count = 0

    @classmethod
    def create_app(cls, config: Any) -> "App":
        """
        Create application and configure population and pipes.

        Parameters:
            config (Dict(str, Any)): Application config
        """
        app = cls(config)
        app.create_population()
        app.create_pipes()
        return app

    def create_population(self) -> None:
        """
        Create the population of members which will learn to play the game. The population size
        corresponds to the number of members in the population, and mutation rate corresponds to
        the probability a member's genes will be mutated.

        The characteristics of each member are also defined. In this case, the Cartesian
        coordinates of the bird's start position are given (x, y), along with its width and height.
        """
        self.birds = []
        for _ in range(self.config.GA["population_size"]):
            self.birds.append(Bird.create(self.config.BIRD, self.config.NN))

        self.population = Population(self.birds, self.config.GA["mutation_rate"])

    def create_pipes(self):
        """
        Create list for pipes and set spawnrate and speed.
        """
        self.pipes = []
        self.pipe_current_spawnrate = self.config.PIPE["start_spawnrate"]
        self.pipe_current_speed = self.config.PIPE["start_speed"]

    def write_text(self, text: str, x: float, y: float) -> None:
        """
        Write text to the screen at the given position.

        Parameters:
            text (str): Text to write
            x (float): x coordinate of text's position
            y (float): y coordinate of text's position
        """
        text_to_write = self.FONT.render(text, False, (255, 255, 255))
        self.display_surf.blit(text_to_write, (x, y))

    def display_stats(self) -> None:
        """
        Display statistics to the screen using the above helper function.

        In this case, the current generation number, the number of birds alive, and the current
        score is displayed on the screen.
        """
        self.write_text(f"Generation: {self.population.generation}", 0, 0)
        self.write_text(
            f"Birds alive: {self.population.num_alive}",
            0,
            self.config.GAME["font"]["size"],
        )
        self.write_text(
            f"Score: {self.population.best_member.score}",
            0,
            self.config.GAME["font"]["size"] * 2,
        )

    def update(self) -> None:
        """
        Perform physics calculations and draw elements to screen.
        """
        if self.population.num_alive == 0 or self.population.best_member.score == self.config.GA["max_score"]:
            self.population.evaluate()
            self.pipes = []
            self.pipe_current_speed = self.config.PIPE["start_speed"]
            self.pipe_current_spawnrate = self.config.PIPE["start_spawnrate"]

        if self.count % int(self.pipe_current_spawnrate) == 0:
            self.pipes.append(Pipe.create(config_pipe=self.config.PIPE, speed=self.pipe_current_speed))
            self.pipe_current_speed = min(
                self.pipe_current_speed + self.config.PIPE["acc_speed"],
                self.config.PIPE["max_speed"],
            )
            self.pipe_current_spawnrate = max(
                self.pipe_current_spawnrate - self.config.PIPE["acc_spawnrate"],
                self.config.PIPE["min_spawnrate"],
            )
            self.count = 1

        for pipe in self.pipes:
            if pipe.offscreen:
                self.pipes.remove(pipe)
            else:
                pipe.update()

        for bird in self.population.population:
            bird.update(self.pipes)

    def run(self) -> None:
        """
        Run the application and handle events.

        In this case, this is where pipes are spawned and the physics for each body is calculated
        and drawn to the screen. If there are no birds left alive, the population is evaluated
        to calculate each members' fitnesses and perform crossover and mutation before resetting
        the game with the new population.
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surf.fill((0, 0, 0))

            self.update()

            # Updating the Pygame window
            self.display_stats()
            pygame.display.update()
            self.FramePerSec.tick(self.FPS)
            self.count += 1
