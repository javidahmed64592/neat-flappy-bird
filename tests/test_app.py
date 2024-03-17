from unittest.mock import PropertyMock, call, patch


class TestApp:
    def test_given_mock_config_when_creating_app_then_check_app_properties(self, mock_app, mock_config, mock_screen):
        assert mock_app.FPS == mock_config.GAME["fps"]
        assert mock_app.screen_width == mock_config.GAME["screen"]["width"]
        assert mock_app.screen_height == mock_config.GAME["screen"]["height"]
        assert mock_app.display_surf == mock_screen
        assert mock_app.name == mock_config.GAME["name"]
        assert mock_app.count == 0

        assert len(mock_app.birds) == mock_config.GA["population_size"]
        assert len(mock_app.population.population) == mock_config.GA["population_size"]

        assert len(mock_app.pipes) == 0
        assert mock_app.pipe_current_spawnrate == mock_config.PIPE["start_spawnrate"]
        assert mock_app.pipe_current_speed == mock_config.PIPE["start_speed"]

    @patch("src.app.App.write_text")
    def test_given_mock_app_when_displaying_stats_then_check_correct_text_written(
        self, mock_write_text, mock_app, mock_config
    ):
        mock_app.display_stats()

        assert mock_write_text.has_calls(
            call("Generation: 1", 0, 0),
            call(f"Birds alive: {mock_config.GA['population_size']}", 0, mock_config.GAME["font"]["size"]),
            call("Score: 0", 0, mock_config.GAME["font"]["size"] * 2),
        )

    @patch("src.ga.ga.Population.evaluate")
    def test_given_no_birds_alive_when_updating_and_then_check_population_evaluated(
        self, mock_evaluate, mock_app, mock_config
    ):
        mock_app.count = 1
        with patch("src.ga.ga.Population.num_alive", new_callable=PropertyMock) as mock_num_alive:
            mock_num_alive.return_value = 0
            mock_app.update()
            assert mock_evaluate.call_count == 1
            assert mock_app.pipes == []
            assert mock_app.pipe_current_speed == mock_config.PIPE["start_speed"]
            assert mock_app.pipe_current_spawnrate == mock_config.PIPE["start_spawnrate"]

    @patch("src.ga.ga.Population.evaluate")
    def test_given_max_score_reached_when_updating_then_check_population_evaluated(
        self, mock_evaluate, mock_app, mock_config
    ):
        mock_app.count = 1
        with patch("src.objects.bird.Bird.score", new_callable=PropertyMock) as mock_score:
            mock_score.return_value = mock_config.GA["max_score"]
            mock_app.update()
            assert mock_evaluate.call_count == 1
            assert mock_app.pipes == []
            assert mock_app.pipe_current_speed == mock_config.PIPE["start_speed"]
            assert mock_app.pipe_current_spawnrate == mock_config.PIPE["start_spawnrate"]

    def test_given_time_to_spawn_pipe_when_updating_then_check_pipe_spawns(self, mock_app, mock_config):
        mock_app.count = mock_app.pipe_current_spawnrate

        mock_app.update()

        assert len(mock_app.pipes) == 1
        assert mock_app.pipe_current_speed == mock_config.PIPE["start_speed"] + mock_config.PIPE["acc_speed"]
        assert (
            mock_app.pipe_current_spawnrate == mock_config.PIPE["start_spawnrate"] - mock_config.PIPE["acc_spawnrate"]
        )
        assert mock_app.count == 1
