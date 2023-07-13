from unittest.mock import call, patch

from src.objects.pipe import Pipe


class TestPipe:
    MOCK_SCREEN_SIZE = [700, 700]
    MOCK_CONFIG_PIPE = {"width": 50, "spacing": 200}
    MOCK_SPEED = 3.5

    def test_given_pipe_config_when_creating_pipe_then_check_pipe_has_correct_properties(
        self, test_pipe, test_config_pipe
    ):
        assert isinstance(test_pipe, Pipe)
        assert test_pipe.width == test_config_pipe["width"]
        assert test_pipe.spacing == test_config_pipe["spacing"]
        assert test_pipe.speed == self.MOCK_SPEED
        assert 0 < test_pipe.top < self.MOCK_SCREEN_SIZE[1]
        assert test_pipe.bottom == self.MOCK_SCREEN_SIZE[1] - (test_pipe.top + test_config_pipe["spacing"])
        assert test_pipe.x == self.MOCK_SCREEN_SIZE[0]
        assert test_pipe.color == test_config_pipe["color"]

    @patch("src.objects.pipe.pygame.draw.rect")
    def test_given_pipe_when_drawing_pipe_then_check_both_pipes_drawn(
        self, mock_draw_rect, test_pipe, test_config_pipe
    ):
        mock_draw_rect.return_value = None

        test_pipe = Pipe.create(test_config_pipe, self.MOCK_SPEED)
        test_pipe.draw()

        assert mock_draw_rect.call_count == 2
        assert mock_draw_rect.has_calls(
            call(test_pipe.screen, test_pipe.color, test_pipe.rect_top),
            call(test_pipe.screen, test_pipe.color, test_pipe.rect_bot),
        )

    @patch("src.objects.pipe.pygame.draw.rect")
    def test_given_pipe_when_updating_pipe_then_check_pipe_has_correct_position(self, mock_draw_rect, test_pipe):
        mock_draw_rect.return_value = None

        test_pipe.update()

        assert test_pipe.x == self.MOCK_SCREEN_SIZE[0] - self.MOCK_SPEED
        assert mock_draw_rect.called

    def test_given_moving_pipe_when_moved_offscreen_then_check_offscreen_returns_true(
        self, test_pipe, test_config_pipe
    ):
        num_update = int((self.MOCK_SCREEN_SIZE[0] + test_config_pipe["width"]) / self.MOCK_SPEED)

        for _ in range(num_update + 1):
            test_pipe.update()

        assert test_pipe.offscreen
