import numpy as np


def generate_number():
    """
    Generate a random number between 0 and 1.
    """
    return np.random.uniform(0, 1)


def select_gene(element: float, other_element: float, mutation_rate: float, low: float, high: float) -> float:
    """
    Select a gene between two matrices or a random gene.

    Parameters:
        element (float): Element to use for selection
        other_element (float): Other element to use for selection
        mutation_rate (float): Probability for element to be random, range [0, 1]
        low (float): Lower limit for random element
        high (float): Upper limit for random element
    """
    if generate_number() < mutation_rate:
        return np.random.uniform(low, high)

    return np.random.choice([element, other_element])
