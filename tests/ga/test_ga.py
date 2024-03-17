from unittest.mock import call, patch


class TestGA:
    def test_given_mock_birds_when_creating_population_then_check_population_correct(self, mock_population):
        assert len(mock_population.population) == 3
        assert mock_population.mutation_rate == 0.05
        assert mock_population.generation == 1

    def test_given_population_when_checking_best_member_then_check_correct_bird_returned(
        self, mock_population, mock_bird_high_score
    ):
        assert mock_population.best_member == mock_bird_high_score

    def test_given_population_when_checking_num_alive_then_check_correct_number_returned(self, mock_population):
        assert mock_population.num_alive == 3

    def test_given_population_when_getting_random_member_then_check_member_in_population(self, mock_population):
        assert mock_population.random_member in mock_population.population

    @patch("src.objects.bird.Bird.reset")
    @patch("src.objects.bird.Bird.apply")
    @patch("src.objects.bird.Bird.crossover")
    @patch("src.ga.ga.Population.select_parent")
    def test_given_population_when_evaluating_then_check_birds_evaluated(
        self, mock_select, mock_crossover, mock_apply, mock_reset, mock_population, mock_bird_high_score
    ):
        mock_select.return_value = mock_bird_high_score

        mock_population.evaluate()

        assert mock_population.generation == 2
        assert mock_select.call_count == 6

        for _ in mock_population.population:
            assert mock_crossover.has_calls(
                call(mock_bird_high_score, mock_bird_high_score, mock_population.mutation_rate)
            )

        assert mock_apply.call_count == 3
        assert mock_reset.call_count == 3

    @patch("numpy.random.uniform")
    def test_given_population_when_checking_member_then_check_rejection_sampling_rejects_member(
        self, mock_np_random, mock_population, mock_bird_mid_score
    ):
        mock_np_random.return_value = 1

        assert mock_population.rejection_sampling(mock_bird_mid_score) is False

    @patch("numpy.random.uniform")
    def test_given_population_when_checking_member_then_check_rejection_sampling_accepts_member(
        self, mock_np_random, mock_population, mock_bird_mid_score
    ):
        mock_np_random.return_value = 0

        assert mock_population.rejection_sampling(mock_bird_mid_score) is True

    def test_given_population_when_selecting_parent_then_check_member_in_population(
        self, mock_population, mock_bird_low_score
    ):
        random_parent = mock_population.select_parent(mock_bird_low_score)
        assert random_parent in mock_population.population
        assert random_parent != mock_bird_low_score
