from unittest.mock import patch
from pathlib import Path
from src.utils.config_utils import get_wd, get_config_folder, parse_configs, load_json, load_configs  # type: ignore


class TestActivationFunctions:
    TEST_WD = Path("/path/to/wd")
    TEST_JSON_FILE = "test_config.json"
    TEST_JSON_DATA = {"test": "data"}

    @patch("src.utils.config_utils.os.path.realpath")
    def test_get_wd(self, mock_realpath):
        mock_realpath.return_value = self.TEST_WD / "utils"
        path_expected = Path(self.TEST_WD)
        path_actual = get_wd()

        assert path_actual == path_expected

    @patch("src.utils.config_utils.get_wd")
    def test_get_config_folder(self, mock_get_wd):
        mock_get_wd.return_value = self.TEST_WD
        path_expected = Path.joinpath(self.TEST_WD, "config")
        path_actual = get_config_folder()

        assert path_actual == path_expected

    def test_parse_configs(self):
        test_names = ["name1", "name2", "name3"]
        test_vals = ["val1", "val2", "val3"]

        parsed_configs_expected = {"name1": "val1", "name2": "val2", "name3": "val3"}
        parsed_configs_actual = parse_configs(test_names, test_vals)

        assert parsed_configs_actual == parsed_configs_expected

    @patch("src.utils.config_utils.open")
    @patch("src.utils.config_utils.json.load")
    def test_load_json(self, mock_json_load, mock_open):
        mock_json_load.return_value = self.TEST_JSON_DATA

        data_actual = load_json(self.TEST_JSON_FILE)

        mock_open.assert_called_with(self.TEST_JSON_FILE, "r")
        assert data_actual == self.TEST_JSON_DATA

    @patch("src.utils.config_utils.load_json")
    def test_load_configs(self, mock_load_json):
        mock_load_json.return_value = self.TEST_JSON_DATA
        test_config_names = ["config1", "config2", "config3"]

        configs_expected = {
            "config1": self.TEST_JSON_DATA,
            "config2": self.TEST_JSON_DATA,
            "config3": self.TEST_JSON_DATA,
        }
        configs_actual = load_configs(test_config_names)

        assert configs_actual == configs_expected
