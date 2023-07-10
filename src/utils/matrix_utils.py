import numpy as np


def select_gene(element: float, other_element: float, mutation_rate: float, low: float, high: float) -> float:
    """
    Select a gene between two matrices or a random gene.

    Parameters:
        element (ndarray): Matrix to use to generate new matrix
        other_element (ndarray): Matrix to use to generate new matrix
        mutation_rate (float): Probability for element to be random, range [0, 1]
        low (float): Lower limit for random element
        high (float): Upper limit for random element
    """
    rng = np.random.uniform(0, 1)
    if rng < mutation_rate:
        return np.random.uniform(low, high)

    if rng < (0.5 + mutation_rate / 2):
        return element

    return other_element
