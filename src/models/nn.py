from models.matrix import Matrix
from models.layer import Layer


class NeuralNetwork:
    def __init__(self, nn_config):
        self.layers = [
            Layer(
                name=nn_config["input_layer"]["name"],
                num_nodes=nn_config["input_layer"]["num_nodes"],
                activation_function_name=nn_config["input_layer"][
                    "activation_function"
                ],
            )
        ]

        for layer in nn_config["hidden_layers"]:
            self.layers.append(
                Layer(
                    name=layer["name"],
                    num_nodes=layer["num_nodes"],
                    activation_function_name=layer["activation_function"],
                )
            )

        self.layers.append(
            Layer(
                name=nn_config["output_layer"]["name"],
                num_nodes=nn_config["output_layer"]["num_nodes"],
                activation_function_name=nn_config["output_layer"][
                    "activation_function"
                ],
            ),
        )

        for layer_index in range(len(self.layers)):
            self.layers[layer_index].generate_activation_function()
            self.layers[layer_index].generate_weights(
                self.layers[layer_index - 1].num_nodes
            )

    def feedforward(self, input_array):
        self.layers[0].set_values(input_array)
        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].feedforward(
                Matrix.to_array(self.layers[layer_index - 1].values)
            )

        return Matrix.to_array(self.layers[-1].values)

    def crossover(self, nn, other_nn, mutation_rate):
        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].crossover(
                nn.layers[layer_index], other_nn.layers[layer_index], mutation_rate
            )

        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].apply()

    def apply(self):
        for layer_index in range(1, len(self.layers)):
            self.layers[layer_index].apply()
