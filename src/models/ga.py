import numpy as np
from typing import List

from objects.bird import Bird


class Population:
    """
    This class creates a population of members. They each have a fitness which is calculated at the
    end of each generation. This is used to select parents for the next generation, individuals
    with higher fitness scores are more likely to reproduce. Rejection Sampling is used when
    selecting parents. The mutation rate corresponds to the probabilty a member's genes will
    mutate during crossover. The new genes are applied and each member and they are reset to their
    starting conditions ready for the next generation.
    """

    def __init__(self, population: List[Bird], mutation_rate: float = 0.05):
        """
        Initialise the population. A list of members is provided along with a mutation rate which
        corresponds to the probability the genes of each member will mutate.

        Parameters:
            population (List(Bird)): List of members in the population
            mutation_rate (float): Probability for members' genes to mutate, range [0, 1]
        """
        self.population = population
        self.mutation_rate = mutation_rate
        self.generation = 1
        self.max_fitness = 0
        self.max_fitness_history = []

    @property
    def best_member(self) -> Bird:
        """
        Return the member with the highest fitness in the population, or return first member if
        there is no best member yet i.e. as soon as application starts.
        """
        best_member = None
        best_fitness = 0

        for member in self.population:
            if member.fitness > best_fitness:
                best_member = member
                best_fitness = member.fitness

        if best_member is None:
            return self.population[0]

        return best_member

    @property
    def num_alive(self) -> int:
        """
        Return the number of members in the population which are alive.
        """
        num_alive = 0
        for member in self.population:
            num_alive += member.alive

        return num_alive

    @property
    def avg_score(self) -> float:
        """
        Return the average score of the population.
        """
        sum = 0

        for member in self.population:
            sum += member.score

        return sum / len(self.population)

    def num_alive_with_max_score(self, max_score: int) -> int:
        """
        Return number of members that achieved a max score.

        Parameters:
            max_score (int): Threshold for member's score
        """
        sum = 0

        for member in self.population:
            sum += member.score == max_score

        return sum

    def evaluate(self):
        """
        Calculate the fitness of each member in the population. Then, use the fitnesses of each
        member to select parents to pass their genes on to the next generation via crossover and
        mutation. Once the new genetics have been generated for each member, apply them and reset
        them to their starting conditions i.e. reset their positions.
        """
        self.max_fitness = self.best_member.fitness
        self.max_fitness_history.append(self.max_fitness)

        for member in self.population:
            parentA = None
            parentB = None

            while parentA is None:
                potential_parent = self.population[
                    np.random.randint(len(self.population))
                ]
                if potential_parent != member:
                    parentA = self.select_parent(potential_parent)

            while parentB is None:
                potential_parent = self.population[
                    np.random.randint(len(self.population))
                ]
                if potential_parent != parentA and potential_parent != member:
                    parentB = self.select_parent(potential_parent)

            member.crossover(parentA, parentB, self.mutation_rate)

        for member in self.population:
            member.apply()
            member.reset()

        self.generation += 1

    def select_parent(self, parent: Bird) -> Bird:
        """
        Use Rejection Sampling to select a parent.

        Parameters:
            parent (Bird): Member of population, potential parent for child

        Returns:
            parent(Bird): Member of population if passed Rejection Sampling
        """
        if np.random.uniform(0, 1) < parent.fitness / self.max_fitness:
            return parent
        return None
