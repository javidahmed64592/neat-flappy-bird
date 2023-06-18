from src.models.activation_functions import ActivationFunctions  # type: ignore


class TestActivationFunctions:
    def test_linear(self):
        x = 5
        y_expected = 5
        y_actual = ActivationFunctions.linear(x)
        assert y_actual == y_expected

    def test_relu(self):
        x1 = 5
        y1_expected = 5
        y1_actual = ActivationFunctions.relu(x1)
        assert y1_actual == y1_expected

        x2 = -5
        y2_expected = 0
        y2_actual = ActivationFunctions.relu(x2)
        assert y2_actual == y2_expected

    def test_sigmoid(self):
        x = 0
        y_expected = 0.5
        y_actual = ActivationFunctions.sigmoid(x)
        assert y_actual == y_expected

    def test_get_linear_activation_function(self):
        func_name = "linear"
        func = ActivationFunctions.get_activation(func_name)
        x = 1
        y_expected = 1
        y_actual = func(x)
        assert y_actual == y_expected

    def test_get_relu_activation_function(self):
        func_name = "relu"
        func = ActivationFunctions.get_activation(func_name)

        x1 = 5
        y1_expected = 5
        y1_actual = func(x1)
        assert y1_actual == y1_expected

        x2 = -5
        y2_expected = 0
        y2_actual = func(x2)
        assert y2_actual == y2_expected

    def test_get_sigmoid_activation_function(self):
        func_name = "sigmoid"
        func = ActivationFunctions.get_activation(func_name)
        x = 0
        y_expected = 0.5
        y_actual = func(x)
        assert y_actual == y_expected
