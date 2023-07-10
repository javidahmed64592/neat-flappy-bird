from unittest.mock import patch

from src.utils.matrix_utils import generate_number, select_gene


class TestMatrixUtils:
    MOCK_MUTATION_RATE = 0.5
    MOCK_LOW = -1
    MOCK_HIGH = 1
    MOCK_ELEMENT = 3
    MOCK_OTHER_ELEMENT = 5

    def test_given_no_params_when_generating_number_then_check_number_between_zero_and_one(self):
        assert 0 <= generate_number() <= 1

    @patch("src.utils.matrix_utils.generate_number")
    def test_given_rng_less_than_mutation_when_getting_element_then_check_random_element_returned(self, mock_rng):
        mock_rng.return_value = 0.1

        actual_value = select_gene(
            self.MOCK_ELEMENT, self.MOCK_OTHER_ELEMENT, self.MOCK_MUTATION_RATE, self.MOCK_LOW, self.MOCK_HIGH
        )

        assert self.MOCK_LOW <= actual_value <= self.MOCK_HIGH

    @patch("src.utils.matrix_utils.generate_number")
    def test_given_rng_greater_than_mutation_less_than_other_element_rng_when_getting_element_then_check_random_element_returned(  # noqa: E501
        self, mock_rng
    ):
        mock_rng.return_value = self.MOCK_MUTATION_RATE + 0.1

        actual_value = select_gene(
            self.MOCK_ELEMENT, self.MOCK_OTHER_ELEMENT, self.MOCK_MUTATION_RATE, self.MOCK_LOW, self.MOCK_HIGH
        )

        assert actual_value == self.MOCK_ELEMENT

    @patch("src.utils.matrix_utils.generate_number")
    def test_given_rng_greater_than_mutation_greater_than_other_element_rng_when_getting_element_then_check_random_element_returned(  # noqa: E501
        self, mock_rng
    ):
        mock_rng.return_value = self.MOCK_MUTATION_RATE + 0.4

        actual_value = select_gene(
            self.MOCK_ELEMENT, self.MOCK_OTHER_ELEMENT, self.MOCK_MUTATION_RATE, self.MOCK_LOW, self.MOCK_HIGH
        )

        assert actual_value == self.MOCK_OTHER_ELEMENT
