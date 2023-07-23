from unittest.mock import call, patch

from src.objects.pipe import Pipe


class TestPipe:
    def test_given_pipe_config_when_creating_pipe_then_check_pipe_has_correct_properties(
        self, mock_pipe, mock_config, mock_screen_size
    ):
        assert isinstance(mock_pipe, Pipe)
        assert mock_pipe.width == mock_config.PIPE["width"]
        assert mock_pipe.spacing == mock_config.PIPE["spacing"]
        assert mock_pipe.speed == mock_config.PIPE["speed"]
        assert 0 < mock_pipe.top < mock_screen_size[1]
        assert mock_pipe.bottom == mock_screen_size[1] - (mock_pipe.top + mock_config.PIPE["spacing"])
        assert mock_pipe.x == mock_screen_size[0]
        assert mock_pipe.color == mock_config.PIPE["color"]

    @patch("src.objects.pipe.pygame.draw.rect")
    def test_given_pipe_when_drawing_pipe_then_check_both_pipes_drawn(self, mock_draw_rect, mock_pipe, mock_config):
        mock_draw_rect.return_value = None

        mock_pipe = Pipe.create(mock_config.PIPE, mock_config.PIPE["speed"])
        mock_pipe.draw()

        assert mock_draw_rect.call_count == 2
        assert mock_draw_rect.has_calls(
            call(mock_pipe.screen, mock_pipe.color, mock_pipe.rect_top),
            call(mock_pipe.screen, mock_pipe.color, mock_pipe.rect_bot),
        )

    @patch("src.objects.pipe.pygame.draw.rect")
    def test_given_pipe_when_updating_pipe_then_check_pipe_has_correct_position(
        self, mock_draw_rect, mock_pipe, mock_screen_size, mock_config
    ):
        mock_draw_rect.return_value = None

        mock_pipe.update()

        assert mock_pipe.x == mock_screen_size[0] - mock_config.PIPE["speed"]
        assert mock_draw_rect.called

    def test_given_moving_pipe_when_moved_offscreen_then_check_offscreen_returns_true(
        self, mock_pipe, mock_config, mock_screen_size
    ):
        num_update = int((mock_screen_size[0] + mock_config.PIPE["width"]) / mock_config.PIPE["speed"])

        for _ in range(num_update + 1):
            mock_pipe.update()

        assert mock_pipe.offscreen
