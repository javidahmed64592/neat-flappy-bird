import math


def sigmoid(x: float) -> float:
    """
    Sigmoid activation function.

    Parameters:
        x (float): Element to use

    Returns:
        (float): 1 / (1 + e^(-x))
    """
    return 1 / (1 + math.exp(-x))


def relu(x: float) -> float:
    """
    ReLU activation function.

    Parameters:
        x (float): Element to use

    Returns:
        (float): x if x > 0 else 0
    """
    return x * (x > 0)


def linear(x: float) -> float:
    """
    Linear activation function.

    Parameters:
        x (float): Element to use

    Returns:
        (float): x
    """
    return x


activation_functions = {"linear": linear, "relu": relu, "sigmoid": sigmoid}
