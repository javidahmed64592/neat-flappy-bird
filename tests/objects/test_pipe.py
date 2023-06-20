from unittest.mock import patch, call
from src.objects.pipe import Pipe


class TestPipe:
    MOCK_SCREEN_SIZE = [700, 700]
    MOCK_CONFIG_PIPE = {"width": 50, "spacing": 200}
    MOCK_SPEED = 3.5
    MOCK_TOP = 200

    @patch("src.objects.pipe.np.random.uniform")
    @patch("src.objects.pipe.pygame.display.get_surface")
    def test_create_pipe(self, mock_get_surface, mock_rand_uniform):
        mock_get_surface.return_value.get_size.return_value = self.MOCK_SCREEN_SIZE
        mock_rand_uniform.return_value = self.MOCK_TOP

        mock_pipe = Pipe.create(self.MOCK_CONFIG_PIPE, self.MOCK_SPEED)

        assert isinstance(mock_pipe, Pipe)
        assert mock_pipe.width == self.MOCK_CONFIG_PIPE["width"]
        assert mock_pipe.spacing == self.MOCK_CONFIG_PIPE["spacing"]
        assert mock_pipe.speed == self.MOCK_SPEED
        assert mock_pipe.top == self.MOCK_TOP
        assert mock_pipe.bottom == self.MOCK_SCREEN_SIZE[1] - (self.MOCK_TOP + self.MOCK_CONFIG_PIPE["spacing"])
        assert mock_pipe.x == self.MOCK_SCREEN_SIZE[0]
        assert mock_pipe.color == (0, 255, 0)

    @patch("src.objects.pipe.pygame.draw.rect")
    @patch("src.objects.pipe.pygame.display.get_surface")
    def test_draw_pipe(self, mock_get_surface, mock_draw_rect):
        mock_get_surface.return_value.get_size.return_value = self.MOCK_SCREEN_SIZE
        mock_draw_rect.return_value = None

        mock_pipe = Pipe.create(self.MOCK_CONFIG_PIPE, self.MOCK_SPEED)
        mock_pipe.draw()

        assert mock_draw_rect.call_count == 2
        assert mock_draw_rect.has_calls(
            call(mock_pipe.screen, mock_pipe.color, mock_pipe.rect_top),
            call(mock_pipe.screen, mock_pipe.color, mock_pipe.rect_bot),
        )

    @patch("src.objects.pipe.pygame.draw.rect")
    @patch("src.objects.pipe.pygame.display.get_surface")
    def test_update_moving_pipe(self, mock_get_surface, mock_draw_rect):
        mock_get_surface.return_value.get_size.return_value = self.MOCK_SCREEN_SIZE
        mock_draw_rect.return_value = None

        mock_pipe = Pipe.create(self.MOCK_CONFIG_PIPE, self.MOCK_SPEED)
        mock_pipe.update()

        assert mock_pipe.x == self.MOCK_SCREEN_SIZE[0] - self.MOCK_SPEED
        assert mock_draw_rect.called

    @patch("src.objects.pipe.pygame.draw.rect")
    @patch("src.objects.pipe.pygame.display.get_surface")
    def test_pipe_offscreen(self, mock_get_surface, mock_draw_rect):
        mock_get_surface.return_value.get_size.return_value = self.MOCK_SCREEN_SIZE
        mock_draw_rect.return_value = None

        mock_pipe = Pipe.create(self.MOCK_CONFIG_PIPE, self.MOCK_SPEED)

        num_update = int((self.MOCK_SCREEN_SIZE[0] + self.MOCK_CONFIG_PIPE["width"]) / self.MOCK_SPEED)

        for _ in range(num_update + 1):
            mock_pipe.update()

        print(f"x = {mock_pipe.x}")
        assert mock_pipe.offscreen
