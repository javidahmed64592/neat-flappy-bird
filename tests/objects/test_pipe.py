from unittest.mock import patch, call
from src.objects.pipe import Pipe


class TestPipe:
    MOCK_SCREEN_SIZE = [700, 700]
    MOCK_CONFIG_PIPE = {"width": 50, "spacing": 200}
    MOCK_SPEED = 3.5

    def test_create_pipe(self, test_pipe):
        assert isinstance(test_pipe, Pipe)
        assert test_pipe.width == self.MOCK_CONFIG_PIPE["width"]
        assert test_pipe.spacing == self.MOCK_CONFIG_PIPE["spacing"]
        assert test_pipe.speed == self.MOCK_SPEED
        assert 0 < test_pipe.top < self.MOCK_SCREEN_SIZE[1]
        assert test_pipe.bottom == self.MOCK_SCREEN_SIZE[1] - (test_pipe.top + self.MOCK_CONFIG_PIPE["spacing"])
        assert test_pipe.x == self.MOCK_SCREEN_SIZE[0]
        assert test_pipe.color == (0, 255, 0)

    @patch("src.objects.pipe.pygame.draw.rect")
    def test_draw_pipe(self, mock_draw_rect, test_pipe):
        mock_draw_rect.return_value = None

        test_pipe = Pipe.create(self.MOCK_CONFIG_PIPE, self.MOCK_SPEED)
        test_pipe.draw()

        assert mock_draw_rect.call_count == 2
        assert mock_draw_rect.has_calls(
            call(test_pipe.screen, test_pipe.color, test_pipe.rect_top),
            call(test_pipe.screen, test_pipe.color, test_pipe.rect_bot),
        )

    @patch("src.objects.pipe.pygame.draw.rect")
    def test_update_moving_pipe(self, mock_draw_rect, test_pipe):
        mock_draw_rect.return_value = None

        test_pipe.update()

        assert test_pipe.x == self.MOCK_SCREEN_SIZE[0] - self.MOCK_SPEED
        assert mock_draw_rect.called

    def test_pipe_offscreen(self, test_pipe):
        num_update = int((self.MOCK_SCREEN_SIZE[0] + self.MOCK_CONFIG_PIPE["width"]) / self.MOCK_SPEED)

        for _ in range(num_update + 1):
            test_pipe.update()

        assert test_pipe.offscreen
