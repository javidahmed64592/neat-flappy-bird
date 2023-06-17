import numpy as np
from typing import List, Optional

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

    @property
    def best_member(self) -> Bird:
        """
        Return the member with the highest fitness in the population, or return first member if
        there is no best member yet i.e. as soon as application starts.

        Returns:
            best_member (Bird): Bird with highest fitness or first one in population
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

        Returns:
            num_alive (int): Number of members alive in population
        """
        num_alive = 0
        for member in self.population:
            num_alive += member.alive

        return num_alive

    def evaluate(self) -> None:
        """
        Calculate the fitness of each member in the population. Then, use the fitnesses of each
        member to select parents to pass their genes on to the next generation via crossover and
        mutation. Once the new genetics have been generated for each member, apply them and reset
        them to their starting conditions i.e. reset their positions.
        """
        self.max_fitness = self.best_member.fitness

        for member in self.population:
            parentA = None
            parentB = None

            while parentA is None:
                potential_parent = self.population[np.random.randint(len(self.population))]
                if potential_parent != member:
                    parentA = self.select_parent(potential_parent)

            while parentB is None:
                potential_parent = self.population[np.random.randint(len(self.population))]
                if potential_parent != parentA and potential_parent != member:
                    parentB = self.select_parent(potential_parent)

            member.crossover(parentA, parentB, self.mutation_rate)

        for member in self.population:
            member.apply()
            member.reset()

        self.generation += 1

    def select_parent(self, parent: Bird) -> Optional[Bird]:
        """
        Use Rejection Sampling to select a parent.

        Parameters:
            parent (Bird): Member of population, potential parent for child

        Returns:
            parent(Optional(Bird)): Member of population if passed Rejection Sampling
        """
        if np.random.uniform(0, 1) < parent.fitness / self.max_fitness:
            return parent
        return None
