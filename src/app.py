import sys
from typing import List
import pygame
from pygame.locals import QUIT
from models.ga import Population
from objects.bird import Bird
from objects.pipe import Pipe
from utils.config_utils import load_configs

config_names = ["game", "ga", "nn", "bird", "pipe"]
config = load_configs(config_names)


class App:
    """
    This class creates a Pygame instance and runs the application. The screen dimensions are
    defined in the __init__ method, and the pipes are also configured in that method. A population
    is created in the create_population method. Helper methods have been defined to write text
    to the screen to display the game statistics. Calling the run method starts the application.
    """

    pygame.init()
    FONT = pygame.font.SysFont(config["game"]["font"]["font"], config["game"]["font"]["size"])
    FPS = config["game"]["fps"]
    FramePerSec = pygame.time.Clock()

    def __init__(self, width: int, height: int, name: str):
        """
        Configure the game window.

        Parameters:
            width (int): Width of game window
            height (int): Height of game window
            name (str): Name of game window
        """
        # Screen configuration
        self.screen_width = width
        self.screen_height = height

        self.display_surf = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(name)

        # Counter to track game time
        self.count = 0

    @classmethod
    def create_app(cls, width: int, height: int, name: str):
        """
        Create application and configure population and pipes.

        Parameters:
            width (int): Width of game window
            height (int): Height of game window
            name (str): Name of game window
        """
        app = cls(width, height, name)
        app.create_population(
            population_size=config["ga"]["population_size"],
            mutation_rate=config["ga"]["mutation_rate"],
        )
        app.create_pipes()
        return app

    def create_population(
        self,
        population_size: int,
        mutation_rate: float,
    ) -> None:
        """
        Create the population of members which will learn to play the game. The population size
        corresponds to the number of members in the population, and mutation rate corresponds to
        the probability a member's genes will be mutated.

        The characteristics of each member are also defined. In this case, the Cartesian
        coordinates of the bird's start position are given (x, y), along with its width and height.

        Parameters:
            population_size (int): Number of members in the population
            mutation_rate (float): Probability for members' genes to mutate, range [0, 1]
        """
        self.birds = []
        for _ in range(population_size):
            self.birds.append(Bird.create(config["bird"], config["nn"]))

        self.population = Population(self.birds, mutation_rate)

    def create_pipes(self):
        """
        Create list for pipes and set spawnrate and speed.
        """
        self.pipes: List[Pipe] = []
        self.pipe_current_spawnrate = config["pipe"]["start_spawnrate"]
        self.pipe_current_speed = config["pipe"]["start_speed"]

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
            config["game"]["font"]["size"],
        )
        self.write_text(
            f"Score: {self.population.best_member.score}",
            0,
            config["game"]["font"]["size"] * 2,
        )

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

            # Game logic goes here
            if self.population.num_alive == 0 or self.population.best_member.score == config["ga"]["max_score"]:
                self.population.evaluate()
                self.pipes = []
                self.pipe_current_speed = config["pipe"]["start_speed"]
                self.pipe_current_spawnrate = config["pipe"]["start_spawnrate"]

            if self.count % int(self.pipe_current_spawnrate) == 0:
                self.pipes.append(Pipe.create(config_pipe=config["pipe"], speed=self.pipe_current_speed))
                self.pipe_current_speed = min(
                    self.pipe_current_speed + config["pipe"]["acc_speed"],
                    config["pipe"]["max_speed"],
                )
                self.pipe_current_spawnrate = max(
                    self.pipe_current_spawnrate - config["pipe"]["acc_spawnrate"],
                    config["pipe"]["min_spawnrate"],
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
    app = App.create_app(
        width=config["game"]["screen"]["width"],
        height=config["game"]["screen"]["height"],
        name=config["game"]["name"],
    )

    app.run()
