from unittest.mock import call, patch

from src.models.nn import NeuralNetwork
from src.objects.bird import Bird


class TestBird:
    MOCK_START_VEL = 0
    MOCK_START_ALIVE = True
    MOCK_START_COUNT = 0

    def test_given_bird_config_when_creating_bird_then_check_bird_has_correct_properties(
        self, test_bird, test_config_bird, test_screen_size
    ):
        assert isinstance(test_bird, Bird)
        assert test_bird.GRAV == test_config_bird["grav"]
        assert test_bird.LIFT == test_config_bird["lift"]
        assert test_bird.MIN_VELOCITY == test_config_bird["min_velocity"]
        assert test_bird.start_y == test_config_bird["y"]
        assert test_bird.velocity == self.MOCK_START_VEL
        assert test_bird.alive == self.MOCK_START_ALIVE
        assert test_bird.count == self.MOCK_START_COUNT
        assert test_bird.screen_width == test_screen_size[0]
        assert test_bird.screen_height == test_screen_size[1]
        assert isinstance(test_bird.nn, NeuralNetwork)

    def test_given_bird_when_resetting_then_check_bird_properties_reset_correctly(self, test_bird, test_config_bird):
        test_bird.update([])
        test_bird.kill()
        test_bird.reset()

        assert test_bird.y == test_config_bird["y"]
        assert test_bird.velocity == 0
        assert test_bird.count == 0
        assert test_bird.alive

    def test_given_bird_when_killing_bird_then_check_bird_not_alive(self, test_bird):
        test_bird.kill()

        assert not test_bird.alive

    @patch("src.objects.bird.pygame.draw.rect")
    def test_given_bird_when_drawing_bird_then_check_bird_drawn(self, mock_draw_rect, test_bird):
        test_bird.draw()

        assert mock_draw_rect.call_count == 1
        assert mock_draw_rect.has_calls(
            call(test_bird.screen, test_bird.color, test_bird),
        )

    def test_given_dead_bird_when_updating_bird_then_check_update_returns_early(self, test_bird):
        test_bird.kill()
        assert test_bird.update([]) is None

    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_not_jumping_then_check_bird_has_correct_velocity(
        self, mock_feedforward, test_bird, test_config_bird
    ):
        mock_feedforward.return_value = [0, 1]

        test_bird.update([])

        assert test_bird.velocity == test_config_bird["grav"]
        assert test_bird.y == test_config_bird["y"] + test_bird.velocity

    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_jumping_then_check_bird_has_correct_velocity(
        self, mock_feedforward, test_bird, test_config_bird
    ):
        mock_feedforward.return_value = [1, 0]

        test_bird.update([])

        assert test_bird.velocity == max(
            test_config_bird["min_velocity"], test_config_bird["grav"] + test_config_bird["lift"]
        )
        assert test_bird.y == test_config_bird["y"] + test_bird.velocity

    @patch("src.objects.bird.Bird.jump")
    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_jumping_then_check_bird_jump_called(self, mock_feedforward, mock_jump, test_bird):
        mock_feedforward.return_value = [1, 0]

        test_bird.update([])

        assert mock_jump.call_count == 1

    @patch("src.objects.bird.Bird.jump")
    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_not_jumping_then_check_bird_jump_not_called(self, mock_feedforward, mock_jump, test_bird):
        mock_feedforward.return_value = [0, 1]

        test_bird.update([])

        assert mock_jump.call_count == 0

    @patch("src.objects.bird.Bird.kill")
    def test_given_bird_offscreen_when_checking_offscreen_then_check_offscreen_is_true(self, mock_kill, test_bird):
        test_bird.y = -1
        assert test_bird.offscreen

        test_bird.y = test_bird.screen_height - test_bird.height + 1
        assert test_bird.offscreen

        test_bird.update([])

        assert mock_kill.call_count == 1

    @patch("src.objects.bird.Bird.kill")
    def test_given_bird_not_offscreen_when_checking_offscreen_then_check_offscreen_is_false(self, mock_kill, test_bird):
        test_bird.y = test_bird.screen_height / 2
        assert not test_bird.offscreen

        test_bird.update([])

        assert mock_kill.call_count == 0

    @patch("src.objects.bird.NeuralNetwork.crossover")
    def test_given_two_test_birds_when_performing_crossover_then_check_bird_nn_crossover_called(
        self, mock_crossover, test_bird
    ):
        test_bird.crossover(test_bird, test_bird, 1)

        assert mock_crossover.call_count == 1
        assert mock_crossover.has_calls(
            call(test_bird.nn, test_bird.nn, 1),
        )

    @patch("src.objects.bird.NeuralNetwork.apply")
    def test_given_bird_when_applying_then_check_bird_nn_apply_called(self, mock_apply, test_bird):
        mock_apply.return_value = [1, 0]

        test_bird.apply()

        assert mock_apply.call_count == 1

    def test_given_mock_count_when_calculating_score_then_check_bird_has_correct_score(self, test_bird):
        mock_count = 3601
        test_bird.count = mock_count

        assert test_bird.score == int(mock_count / 60)
        assert test_bird.fitness == int(mock_count / 60) ** 2

    @patch("src.utils.pipe_utils.get_closest_pipe")
    @patch("src.objects.bird.Bird.collide_with_pipe")
    def test_given_bird_and_pipe_when_colliding_with_pipe_then_check_bird_dies(
        self, mock_collide_pipe, mock_closest_pipe, test_bird, test_pipe
    ):
        mock_collide_pipe.return_value = True
        mock_closest_pipe.return_value = test_pipe

        test_bird.update([test_pipe])
        assert not test_bird.alive

    @patch("src.utils.pipe_utils.get_closest_pipe")
    @patch("src.objects.bird.Bird.collide_with_pipe")
    def test_given_bird_and_pipe_when_not_colliding_with_pipe_then_check_bird_lives(
        self, mock_collide_pipe, mock_closest_pipe, test_bird, test_pipe
    ):
        mock_collide_pipe.return_value = False
        mock_closest_pipe.return_value = test_pipe

        test_bird.update([test_pipe])
        assert test_bird.alive
