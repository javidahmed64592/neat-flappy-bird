from unittest.mock import call, patch


class TestGA:
    def test_given_test_birds_when_creating_population_then_check_population_correct(self, test_population):
        assert len(test_population.population) == 3
        assert test_population.mutation_rate == 0.05
        assert test_population.generation == 1

    def test_given_population_when_checking_best_member_then_check_correct_bird_returned(
        self, test_population, test_bird_high_score
    ):
        assert test_population.best_member == test_bird_high_score

    def test_given_population_when_checking_num_alive_then_check_correct_number_returned(self, test_population):
        assert test_population.num_alive == 3

    def test_given_population_when_getting_random_member_then_check_member_in_population(self, test_population):
        assert test_population.random_member in test_population.population

    @patch("src.objects.bird.Bird.reset")
    @patch("src.objects.bird.Bird.apply")
    @patch("src.objects.bird.Bird.crossover")
    @patch("src.models.ga.Population.select_parent")
    def test_given_population_when_evaluating_then_check_birds_evaluated(
        self, mock_select, mock_crossover, mock_apply, mock_reset, test_population, test_bird_high_score
    ):
        mock_select.return_value = test_bird_high_score

        test_population.evaluate()

        assert test_population.generation == 2
        assert mock_select.call_count == 6

        for _ in test_population.population:
            assert mock_crossover.has_calls(
                call(test_bird_high_score, test_bird_high_score, test_population.mutation_rate)
            )

        assert mock_apply.call_count == 3
        assert mock_reset.call_count == 3

    @patch("numpy.random.uniform")
    def test_given_population_when_checking_member_then_check_rejection_sampling_rejects_member(
        self, mock_np_random, test_population, test_bird_mid_score
    ):
        mock_np_random.return_value = 1

        assert test_population.rejection_sampling(test_bird_mid_score) is False

    @patch("numpy.random.uniform")
    def test_given_population_when_checking_member_then_check_rejection_sampling_accepts_member(
        self, mock_np_random, test_population, test_bird_mid_score
    ):
        mock_np_random.return_value = 0

        assert test_population.rejection_sampling(test_bird_mid_score) is True

    def test_given_population_when_selecting_parent_then_check_member_in_population(
        self, test_population, test_bird_low_score
    ):
        random_parent = test_population.select_parent(test_bird_low_score)
        assert random_parent in test_population.population
        assert random_parent != test_bird_low_score
