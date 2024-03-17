from typing import Any, List, Optional, cast

import numpy as np


class Population:
    """
    This class creates a population of members. They each have a fitness which is calculated at the
    end of each generation. This is used to select parents for the next generation, individuals
    with higher fitness scores are more likely to reproduce. Rejection Sampling is used when
    selecting parents. The mutation rate corresponds to the probabilty a member's genes will
    mutate during crossover. The new genes are applied and each member and they are reset to their
    starting conditions ready for the next generation.
    """

    def __init__(self, population: List[Any], mutation_rate: float = 0.05):
        """
        Initialise the population. A list of members is provided along with a mutation rate which
        corresponds to the probability the genes of each member will mutate.

        Parameters:
            population (List(Any)): List of members in the population
            mutation_rate (float): Probability for members' genes to mutate, range [0, 1]
        """
        self.population = population
        self.mutation_rate = mutation_rate
        self.generation = 1

    @property
    def best_member(self) -> Any:
        """
        Return the member with the highest fitness in the population, or return first member if
        there is no best member yet i.e. as soon as application starts.

        Returns:
            best_member (Any): Member with highest fitness or first one in population
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

    @property
    def random_member(self) -> Any:
        """
        Returns a random member from the population.

        Returns:
            (Any): Random member from population
        """
        return self.population[np.random.randint(len(self.population))]

    def evaluate(self) -> None:
        """
        Calculate the fitness of each member in the population. Then, use the fitnesses of each
        member to select parents to pass their genes on to the next generation via crossover and
        mutation. Once the new genetics have been generated for each member, apply them and reset
        them to their starting conditions i.e. reset their positions.
        """
        for member in self.population:
            parentA = self.select_parent(member)
            parentB = self.select_parent(member, parentA)

            member.crossover(parentA, parentB, self.mutation_rate)

        for member in self.population:
            member.apply()
            member.reset()

        self.generation += 1

    def rejection_sampling(self, member: Any) -> bool:
        """
        Use Rejection Sampling to accept or reject a member.

        Parameters:
            member (Any): Member to check against algorithm

        Returns:
            (bool): True if member passes Rejection sampling.
        """
        return cast(bool, np.random.uniform(0, 1) < member.fitness / self.best_member.fitness)

    def select_parent(self, member: Any, other_parent: Optional[Any] = None) -> Any:
        """
        Select a random parent from the population.

        Parameters:
            member (Any): Member of population to select parents for
            other_parent (Optional(Any)): Other parent if selected

        Returns:
            parent(Any): Member of population if passed Rejection Sampling
        """
        while True:
            potential_parent = self.random_member
            if potential_parent != member and potential_parent != other_parent:
                if self.rejection_sampling(potential_parent):
                    return potential_parent
