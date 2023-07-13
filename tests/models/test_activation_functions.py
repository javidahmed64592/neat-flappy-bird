from src.models.activation_functions import ActivationFunctions


class TestActivationFunctions:
    def test_given_linear_activation_when_calculating_output_then_check_output_is_correct(self):
        x = 5
        y_expected = 5
        y_actual = ActivationFunctions.linear(x)
        assert y_actual == y_expected

    def test_given_relu_activation_when_calculating_output_then_check_output_is_correct(self):
        x1 = 5
        y1_expected = 5
        y1_actual = ActivationFunctions.relu(x1)
        assert y1_actual == y1_expected

        x2 = -5
        y2_expected = 0
        y2_actual = ActivationFunctions.relu(x2)
        assert y2_actual == y2_expected

    def test_given_sigmoid_activation_when_calculating_output_then_check_output_is_correct(self):
        x = 0
        y_expected = 0.5
        y_actual = ActivationFunctions.sigmoid(x)
        assert y_actual == y_expected

    def test_given_linear_activation_when_getting_activation_function_then_check_output_is_correct(self):
        func_name = "linear"
        func = ActivationFunctions.get_activation(func_name)
        x = 1
        y_expected = 1
        y_actual = func(x)
        assert y_actual == y_expected

    def test_given_relu_activation_when_getting_activation_function_then_check_output_is_correct(self):
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

    def test_given_sigmoid_activation_when_getting_activation_function_then_check_output_is_correct(self):
        func_name = "sigmoid"
        func = ActivationFunctions.get_activation(func_name)
        x = 0
        y_expected = 0.5
        y_actual = func(x)
        assert y_actual == y_expected
