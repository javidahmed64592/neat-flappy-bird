from unittest.mock import call, patch

from src.models.nn import NeuralNetwork
from src.objects.bird import Bird


class TestBird:
    MOCK_START_VEL = 0
    MOCK_START_ALIVE = True
    MOCK_START_COUNT = 0

    def test_given_bird_config_when_creating_bird_then_check_bird_has_correct_properties(
        self, mock_bird, mock_config_bird, mock_screen_size
    ):
        assert isinstance(mock_bird, Bird)
        assert mock_bird.GRAV == mock_config_bird["grav"]
        assert mock_bird.LIFT == mock_config_bird["lift"]
        assert mock_bird.MIN_VELOCITY == mock_config_bird["min_velocity"]
        assert mock_bird.start_y == mock_config_bird["y"]
        assert mock_bird.velocity == self.MOCK_START_VEL
        assert mock_bird.alive == self.MOCK_START_ALIVE
        assert mock_bird.count == self.MOCK_START_COUNT
        assert mock_bird.screen_width == mock_screen_size[0]
        assert mock_bird.screen_height == mock_screen_size[1]
        assert isinstance(mock_bird.nn, NeuralNetwork)

    def test_given_bird_when_resetting_then_check_bird_properties_reset_correctly(self, mock_bird, mock_config_bird):
        mock_bird.update([])
        mock_bird.kill()
        mock_bird.reset()

        assert mock_bird.y == mock_config_bird["y"]
        assert mock_bird.velocity == 0
        assert mock_bird.count == 0
        assert mock_bird.alive

    def test_given_bird_when_killing_bird_then_check_bird_not_alive(self, mock_bird):
        mock_bird.kill()

        assert not mock_bird.alive

    @patch("src.objects.bird.pygame.draw.rect")
    def test_given_bird_when_drawing_bird_then_check_bird_drawn(self, mock_draw_rect, mock_bird):
        mock_bird.draw()

        assert mock_draw_rect.call_count == 1
        assert mock_draw_rect.has_calls(
            call(mock_bird.screen, mock_bird.color, mock_bird),
        )

    def test_given_dead_bird_when_updating_bird_then_check_update_returns_early(self, mock_bird):
        mock_bird.kill()
        assert mock_bird.update([]) is None

    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_not_jumping_then_check_bird_has_correct_velocity(
        self, mock_feedforward, mock_bird, mock_config_bird
    ):
        mock_feedforward.return_value = [0, 1]

        mock_bird.update([])

        assert mock_bird.velocity == mock_config_bird["grav"]
        assert mock_bird.y == mock_config_bird["y"] + mock_bird.velocity

    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_jumping_then_check_bird_has_correct_velocity(
        self, mock_feedforward, mock_bird, mock_config_bird
    ):
        mock_feedforward.return_value = [1, 0]

        mock_bird.update([])

        assert mock_bird.velocity == max(
            mock_config_bird["min_velocity"], mock_config_bird["grav"] + mock_config_bird["lift"]
        )
        assert mock_bird.y == mock_config_bird["y"] + mock_bird.velocity

    @patch("src.objects.bird.Bird.jump")
    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_jumping_then_check_bird_jump_called(self, mock_feedforward, mock_jump, mock_bird):
        mock_feedforward.return_value = [1, 0]

        mock_bird.update([])

        assert mock_jump.call_count == 1

    @patch("src.objects.bird.Bird.jump")
    @patch("src.objects.bird.NeuralNetwork.feedforward")
    def test_given_bird_when_not_jumping_then_check_bird_jump_not_called(self, mock_feedforward, mock_jump, mock_bird):
        mock_feedforward.return_value = [0, 1]

        mock_bird.update([])

        assert mock_jump.call_count == 0

    @patch("src.objects.bird.Bird.kill")
    def test_given_bird_offscreen_when_checking_offscreen_then_check_offscreen_is_true(self, mock_kill, mock_bird):
        mock_bird.y = -1
        assert mock_bird.offscreen

        mock_bird.y = mock_bird.screen_height - mock_bird.height + 1
        assert mock_bird.offscreen

        mock_bird.update([])

        assert mock_kill.call_count == 1

    @patch("src.objects.bird.Bird.kill")
    def test_given_bird_not_offscreen_when_checking_offscreen_then_check_offscreen_is_false(self, mock_kill, mock_bird):
        mock_bird.y = mock_bird.screen_height / 2
        assert not mock_bird.offscreen

        mock_bird.update([])

        assert mock_kill.call_count == 0

    @patch("src.objects.bird.NeuralNetwork.crossover")
    def test_given_two_mock_birds_when_performing_crossover_then_check_bird_nn_crossover_called(
        self, mock_crossover, mock_bird
    ):
        mock_bird.crossover(mock_bird, mock_bird, 1)

        assert mock_crossover.call_count == 1
        assert mock_crossover.has_calls(
            call(mock_bird.nn, mock_bird.nn, 1),
        )

    @patch("src.objects.bird.NeuralNetwork.apply")
    def test_given_bird_when_applying_then_check_bird_nn_apply_called(self, mock_apply, mock_bird):
        mock_apply.return_value = [1, 0]

        mock_bird.apply()

        assert mock_apply.call_count == 1

    def test_given_mock_count_when_calculating_score_then_check_bird_has_correct_score(self, mock_bird):
        mock_count = 3601
        mock_bird.count = mock_count

        assert mock_bird.score == int(mock_count / 60)
        assert mock_bird.fitness == int(mock_count / 60) ** 2

    @patch("src.utils.pipe_utils.get_closest_pipe")
    @patch("src.objects.bird.Bird.collide_with_pipe")
    def test_given_bird_and_pipe_when_colliding_with_pipe_then_check_bird_dies(
        self, mock_collide_pipe, mock_closest_pipe, mock_bird, mock_pipe
    ):
        mock_collide_pipe.return_value = True
        mock_closest_pipe.return_value = mock_pipe

        mock_bird.update([mock_pipe])
        assert not mock_bird.alive

    @patch("src.utils.pipe_utils.get_closest_pipe")
    @patch("src.objects.bird.Bird.collide_with_pipe")
    def test_given_bird_and_pipe_when_not_colliding_with_pipe_then_check_bird_lives(
        self, mock_collide_pipe, mock_closest_pipe, mock_bird, mock_pipe
    ):
        mock_collide_pipe.return_value = False
        mock_closest_pipe.return_value = mock_pipe

        mock_bird.update([mock_pipe])
        assert mock_bird.alive
