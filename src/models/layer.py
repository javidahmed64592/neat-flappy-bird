import math
from models.matrix import Matrix


class Layer:
    def __init__(
        self,
        name,
        num_nodes,
        values=None,
        activation_function_name="linear",
        weights_range=[-1, 1],
        bias_range=[-1, 1],
    ):
        self.name = name
        self.num_nodes = num_nodes
        self.activation_function_name = activation_function_name
        self.weights_range = weights_range
        self.bias_range = bias_range

        if values:
            self.values = values

    def generate_weights(self, cols):
        self.weights = Matrix.random_matrix(
            self.num_nodes, cols, self.weights_range[0], self.weights_range[1]
        )
        self.bias = Matrix.random_matrix(
            self.num_nodes, 1, self.bias_range[0], self.bias_range[1]
        )

    def set_values(self, values):
        self.values = Matrix.column_matrix(values)

    def feedforward(self, values):
        self.values = self.weights * Matrix.column_matrix(values) + self.bias
        self.values = Matrix.map(self.values, self.activation_function)

    def generate_activation_function(self):
        linear = lambda x: x
        relu = lambda x: x * (x > 0)
        sigmoid = lambda x: (1 / (1 + math.exp(-x)))
        functions = {"linear": linear, "relu": relu, "sigmoid": sigmoid}
        self.activation_function = functions[self.activation_function_name]

    def crossover(self, layer, other_layer, mutation_rate):
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

    def apply(self):
        self.weights = self.new_weights
        self.bias = self.new_bias
