from typing import Any, Dict, List

import numpy as np

from src.models.layer import Layer


class NeuralNetwork:
    """
    This class creates a simple artificial neural network with an input layer, output layer, and
    hidden layers. Each layer can be configured by editing src/config/nn_config.json.

    Initially, the weights and biases of each node in the hidden and output layers are selected at
    random. These are evolved to be more refined for their uses as the neural network trains.

    The feedforward() method uses matrix multiplication and addition to tell each layer how to
    communicate and send information to the next layer. The crossover() method mixes the weights
    and biases of two neural networks with a chance for any given value to be chosen at random,
    determined by the mutation rate. The apply() method overwrites the weights and biases with the
    newly calculated ones.
    """

    def __init__(self, layers: List[Layer]):
        """
        Create a neural network with assigned layers.

        Parameters:
            layers (List[Layer]): Layers of neural network
        """
        self.layers = layers

    @classmethod
    def initialise_neural_network(cls, nn_config: Dict[str, Any]) -> "NeuralNetwork":
        """
        Create a neural network using configuration dictionary.

        Parameters:
            nn_config (Dict[str, Any]): Neural network configuration

        Returns:
            (NeuralNetwork): Neural network with layers from configuration
        """
        layers = [
            Layer.input_layer(
                name=nn_config["input_layer"]["name"],
                values=np.array([0] * nn_config["input_layer"]["num_nodes"]),
                activation=nn_config["input_layer"]["activation"],
            )
        ]

        for layer in nn_config["hidden_layers"]:
            layers.append(
                Layer(
                    name=layer["name"],
                    num_nodes=layer["num_nodes"],
                    activation=layer["activation"],
                )
            )

        layers.append(
            Layer(
                name=nn_config["output_layer"]["name"],
                num_nodes=nn_config["output_layer"]["num_nodes"],
                activation=nn_config["output_layer"]["activation"],
            ),
        )

        for layer_index in range(len(layers)):
            layers[layer_index].generate_weights(layers[layer_index - 1].num_nodes)

        return cls(layers)

    def feedforward(self, input_array: np.ndarray) -> np.ndarray:
        """
        Take a list of input values and pass them through the layers of the neural network to
        calculate a list of outputs.

        Parameters:
            input_array (np.ndarray):

        Returns:
            (List[float]): Output values
        """
        self.layers[0].set_values(input_array)
        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].feedforward((self.layers[layer_index - 1].values).tolist())

        return (self.layers[-1].values).tolist()

    def crossover(self, nn: "NeuralNetwork", other_nn: "NeuralNetwork", mutation_rate: float) -> None:
        """
        Crossover the weights and biases of two neural networks. Each element has a chance to be
        random, determined by mutation_rate.

        Parameters:
            nn (NeuralNetwork): Neural network to use for crossover
            other_nn (NeuralNetwork): Other neural network to use
            mutation_rate (float): Probability for random mutation, range [0, 1]
        """
        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].crossover(nn.layers[layer_index], other_nn.layers[layer_index], mutation_rate)

        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].apply()

    def apply(self) -> None:
        """
        Apply new weights and bias matrices for each layer.
        """
        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].apply()
