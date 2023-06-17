import math
from typing import Any


class ActivationFunctions:
    @staticmethod
    def get_activation(name: str) -> Any:
        """
        Return activation function from name.

        Parameters:
            name (str): Name of activation function

        Returns:
            (Any): Activation function
        """
        activation_functions = {
            "linear": ActivationFunctions.linear,
            "relu": ActivationFunctions.relu,
            "sigmoid": ActivationFunctions.sigmoid,
        }
        return activation_functions[name]

    @staticmethod
    def sigmoid(x: float) -> float:
        """
        Sigmoid activation function.

        Parameters:
            x (float): Element to use

        Returns:
            (float): 1 / (1 + e^(-x))
        """
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def relu(x: float) -> float:
        """
        ReLU activation function.

        Parameters:
            x (float): Element to use

        Returns:
            (float): x if x > 0 else 0
        """
        return x * (x > 0)

    @staticmethod
    def linear(x: float) -> float:
        """
        Linear activation function.

        Parameters:
            x (float): Element to use

        Returns:
            (float): x
        """
        return x
