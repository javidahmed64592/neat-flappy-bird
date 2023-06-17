import numpy as np
from typing import List
from models.matrix import Matrix
from models.activation_functions import activation_functions


class Layer:
    """
    This class creates a layer which can be used in neural networks. Each layer is made up of
    nodes. They also have a weights matrix and a bias matrix for the feedforward algorithm.
    Each node is mapped through an activation function.

    The crossover() method mixes the weights and biases of two neural networks with a chance for
    any given value to be chosen at random, determined by the mutation rate. The apply() method
    overwrites the weights and biases with the newly calculated ones.
    """

    def __init__(
        self,
        name: str,
        num_nodes: int,
        activation: str = "linear",
        weights_range: List[float] = [-1, 1],
        bias_range: List[float] = [-1, 1],
    ):
        """
        Create a new layer with the following properties.

        Parameters:
            name (str): Name of layer
            num_nodes (int): Number of nodes
            activation (str): Activation function to use
            weights_range (List[float]): Range to use for elements random weights matrix
            bias_range (List[float]): Range to use for elements random bias matrix
        """
        self.name = name
        self.num_nodes = num_nodes
        self.activation = activation_functions[activation]
        self.weights_range = weights_range
        self.bias_range = bias_range

    @classmethod
    def input_layer(cls, name: str, values: np.ndarray, activation: str) -> "Layer":
        """
        Generate input layer with list of values.

        Parameters:
            name (str): Name of layer
            values (List[float]): Values to assign to nodes
            activation (str): Activation function to use

        Returns:
            (Layer): Layer with assigned node values
        """
        layer = cls(name, len(values), activation)
        layer.set_values(values)
        return layer

    def generate_weights(self, cols: int) -> None:
        """
        Generate random weights and bias matrices using given ranges. The number of columns in the
        weights matrix must equal the number of rows in the previous layer's weights matrix.

        Parameters:
            cols (int): Number of columns for weights matrix
        """
        self.weights = Matrix.random_matrix(self.num_nodes, cols, self.weights_range[0], self.weights_range[1])
        self.bias = Matrix.random_matrix(self.num_nodes, 1, self.bias_range[0], self.bias_range[1])

    def set_values(self, values: np.ndarray) -> None:
        """
        Set node values.

        Parameters:
            values (List[float]): Values to assign to nodes
        """
        self.values = Matrix.column_matrix(values)
        self.values = Matrix.map(self.values, self.activation)

    def feedforward(self, values: np.ndarray) -> None:
        """
        Calculate node values using the feedforward algorithm.

        M = Values
        W = Weights
        B = Bias
        N = Number of nodes

        Feedforward: M_(i) = W_(i) x M_(i-1) + B_(i)
        Shape: (N_(i), 1) = (N_(i), N_(i-1)) x (N_(i-1), 1) + (N_(i), 1)

        Parameters:
            values (np.ndarray): Node values from previous layer
        """
        self.values = self.weights * Matrix.column_matrix(values) + self.bias
        self.values = Matrix.map(self.values, self.activation)

    def crossover(self, layer: "Layer", other_layer: "Layer", mutation_rate: float) -> None:
        """
        Generate new weights and bias matrices using two layers.

        Parameters:
            layer (Layer): Layer to use for crossover
            other_layer (Layer): Other layer to use
            mutation_rate (float): Probability for random mutation, range [0, 1]
        """
        self.new_weights = Matrix.crossover(
            layer.weights,
            other_layer.weights,
            mutation_rate,
            self.weights_range[0],
            self.weights_range[1],
        )

        self.new_bias = Matrix.crossover(
            layer.bias,
            other_layer.bias,
            mutation_rate,
            self.bias_range[0],
            self.bias_range[1],
        )

    def apply(self) -> None:
        """
        Overwrite weights and bias matrices with new values.
        """
        self.weights = self.new_weights
        self.bias = self.new_bias
