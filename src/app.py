import sys
import os
import json
import pygame
from pygame.locals import *

with open(
    os.path.join(os.path.dirname(__file__), "config", "config.json"), "r"
) as file:
    data = json.load(file)

with open(
    os.path.join(os.path.dirname(__file__), "config", "layers.json"), "r"
) as file:
    nn_data = json.load(file)

from models.ga import Population

from objects.bird import Bird
from objects.pipe import Pipe


avg_score_history = []
num_alive_at_max = []


class App:
    """
    This class creates a Pygame instance and runs the application. The screen dimensions are
    defined in the __init__ method, and the pipes are also configured in that method. A population
    is created in the create_population method. Helper methods have been defined to write text
    to the screen to display the game statistics. Calling the run method starts the application.
    """

    pygame.init()
    FONT = pygame.font.SysFont(data["font"]["font"], data["font"]["size"])
    FPS = data["fps"]
    FramePerSec = pygame.time.Clock()

    def __init__(self, width: int, height: int, name: str):
        """
        Configure the game window and the pipes.

        Parameters:
            width (int): Width of game window
            height (int): Height of game window
            name (str): Name of game window
        """
        # Screen configuration
        self.screen_width = width
        self.screen_height = height

        self.display_surf = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption(name)

        # Counter to track game time
        self.count = 0

        # Pipe configuration
        self.pipes = []
        self.pipe_current_spawnrate = data["pipe"]["start_spawnrate"]
        self.pipe_current_speed = data["pipe"]["start_speed"]

    def create_population(
        self,
        population_size: int,
        mutation_rate: float,
        x: float,
        y: float,
        width: float = 40,
        height: float = 40,
    ):
        """
        Create the population of members which will learn to play the game. The population size
        corresponds to the number of members in the population, and mutation rate corresponds to
        the probability a member's genes will be mutated.

        The characteristics of each member are also defined. In this case, the Cartesian
        coordinates of the bird's start position are given (x, y), along with its width and height.

        Parameters:
            population_size (int): Number of members in the population
            mutation_rate (float): Probability for members' genes to mutate, range [0, 1]
            x (float): x coordinate of bird's start position
            y (float): y coordinate of bird's start position
            width (float): Width of bird
            height (float): Height of bird
        """
        # Bird configuration
        self.birds = []
        for _ in range(population_size):
            self.birds.append(Bird(x, y, width, height))

        self.population = Population(self.birds, mutation_rate)

    def write_text(self, text: str, x: float, y: float):
        """
        Write text to the screen at the given position.

        Parameters:
            text (str): Text to write
            x (float): x coordinate of text's position
            y (float): y coordinate of text's position
        """
        text_to_write = self.FONT.render(text, False, (255, 255, 255))
        self.display_surf.blit(text_to_write, (x, y))

    def display_stats(self):
        """
        Display statistics to the screen using the above helper function.

        In this case, the current generation number, the number of birds alive, and the current
        score is displayed on the screen.
        """
        self.write_text(f"Generation: {self.population.generation}", 0, 0)
        self.write_text(
            f"Birds alive: {self.population.num_alive}", 0, data["font"]["size"]
        )
        self.write_text(
            f"Score: {self.population.best_member.score}", 0, data["font"]["size"] * 2
        )

    def run(self):
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

            # Game logic goes here
            if (
                self.population.num_alive == 0
                or self.population.best_member.score == data["max_score"]
            ):
                avg_score_history.append(self.population.avg_score)
                num_alive_at_max.append(
                    self.population.num_alive_with_max_score(data["max_score"])
                )

                self.population.evaluate()
                self.pipes = []
                self.pipe_current_speed = data["pipe"]["start_speed"]
                self.pipe_current_spawnrate = data["pipe"]["start_spawnrate"]

            if self.count % int(self.pipe_current_spawnrate) == 0:
                self.pipes.append(
                    Pipe(spacing=data["pipe"]["spacing"], speed=self.pipe_current_speed)
                )
                self.pipe_current_speed = min(
                    self.pipe_current_speed + data["pipe"]["acc_speed"],
                    data["pipe"]["max_speed"],
                )
                self.pipe_current_spawnrate = max(
                    self.pipe_current_spawnrate - data["pipe"]["acc_spawnrate"],
                    data["pipe"]["min_spawnrate"],
                )
                self.count = 1

            for pipe in self.pipes:
                if pipe.offscreen:
                    self.pipes.remove(pipe)
                else:
                    pipe.update()

            for bird in self.population.population:
                bird.update(self.pipes)

            # Updating the Pygame window
            self.display_stats()
            pygame.display.update()
            self.FramePerSec.tick(self.FPS)
            self.count += 1


if __name__ == "__main__":
    app = App(
        width=data["screen"]["width"],
        height=data["screen"]["height"],
        name=data["name"],
    )
    app.create_population(
        population_size=data["population_size"],
        mutation_rate=data["mutation_rate"],
        x=data["bird"]["x"],
        y=data["bird"]["y"],
    )
    app.run()
