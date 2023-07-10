import numpy as np


def matrix_crossover(
    matrix: np.ndarray,
    other_matrix: np.ndarray,
    mutation_rate: float,
    low: float,
    high: float,
) -> np.ndarray:
    """
    Generate a new matrix by mixing two matrices. Each element in the new matrix is randomly
    selected from the two matrices, but there is also a chance for the element to be random.

    Parameters:
        matrix (ndarray): Matrix to use to generate new matrix
        other_matrix (ndarray): Matrix to use to generate new matrix
        mutation_rate (float): Probability for element to be random, range [0, 1]
        low (float): Lower limit for random element
        high (float): Upper limit for random element

    Returns:
        (ndarray): Mixed matrix from provided matrices
    """
    matrix_elements = matrix.tolist()
    other_matrix_elements = other_matrix.tolist()

    elements = []

    return np.vectorize(select_gene)(mutation_rate, low, high, matrix, other_matrix)

    # for i in range(len(matrix)):
    #     for j in range(len(matrix[i])):
    #         rng = np.random.uniform(0, 1)
    #         self.values = np.vectorize(self.activation)(self.values)
    #         elements.append(
    #             select_gene(rng, mutation_rate, low, high, matrix_elements[i][j], other_matrix_elements[i][j])
    #         )

    # return np.matrix(elements)


def select_gene(mutation_rate, low, high, element, other_element):
    rng = np.random.uniform(0, 1)
    if rng < mutation_rate:
        return np.random.uniform(low, high)

    if rng < (0.5 + mutation_rate / 2):
        return element

    return other_element
