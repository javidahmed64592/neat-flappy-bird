from dotenv import load_dotenv

from src.app import App
from src.utils.config_utils import get_config_module

load_dotenv()

config = get_config_module()

if __name__ == "__main__":
    app = App.create_app(config)
    app.run()
