from pathlib import Path
from unittest.mock import call, patch

from src.utils.config_utils import get_config_module, load_configs, load_json, parse_configs


class TestConfigUtils:
    TEST_JSON_FILE = Path("test_config.json")
    TEST_JSON_DATA = {"test": "data"}

    @patch("src.utils.config_utils.import_module")
    def test_given_settings_module_when_getting_config_module_then_check_config_gets_returned(self, mock_import_module):
        mock_settings_module = "src.config.test"
        get_config_module(mock_settings_module)
        assert mock_import_module.has_calls(call(mock_settings_module))

    @patch("src.utils.config_utils.import_module")
    @patch("src.utils.config_utils.os")
    def test_given_no_settings_module_when_getting_config_module_then_check_config_gets_returned(
        self, mock_os, mock_import_module
    ):
        mock_settings_module = "src.config.test"
        mock_os.return_value.environ.return_value.get.return_value = mock_settings_module
        get_config_module()
        assert mock_import_module.has_calls(call(mock_settings_module))

    def test_given_test_config_when_parsing_config_then_check_config_is_correct(self):
        test_names = ["name1", "name2", "name3"]
        test_vals = [{"val1": 1, "val2": 1}, {"val1": 2, "val2": 2}, {"val1": 3, "val2": 3}]

        parsed_configs_expected = {
            "name1": {"val1": 1, "val2": 1},
            "name2": {"val1": 2, "val2": 2},
            "name3": {"val1": 3, "val2": 3},
        }
        parsed_configs_actual = parse_configs(test_names, test_vals)

        assert parsed_configs_actual == parsed_configs_expected

    @patch("src.utils.config_utils.open")
    @patch("src.utils.config_utils.json.load")
    def test_given_test_json_when_loading_json_then_check_json_gets_loaded(self, mock_json_load, mock_open):
        mock_json_load.return_value = self.TEST_JSON_DATA

        data_actual = load_json(self.TEST_JSON_FILE)

        mock_open.assert_called_with(self.TEST_JSON_FILE, "r")
        assert data_actual == self.TEST_JSON_DATA

    @patch("src.utils.config_utils.load_json")
    def test_given_test_configs_when_loading_configs_then_check_configs_loaded_correctly(self, mock_load_json):
        mock_load_json.return_value = self.TEST_JSON_DATA
        test_config_names = ["config1", "config2", "config3"]

        configs_expected = {
            "config1": self.TEST_JSON_DATA,
            "config2": self.TEST_JSON_DATA,
            "config3": self.TEST_JSON_DATA,
        }
        configs_actual = load_configs(test_config_names)

        assert configs_actual == configs_expected
