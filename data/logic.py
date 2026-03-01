import os
import json
from pathlib import Path


class Config:
    standart_config = {
        "name": "Nova",
        "voice": {
            "voice": "en-US-GuyNeural",
            "rate": "+20%",
            "volume": "+100%",
            "pitch": "+0Hz",
        },
    }
    standart_dir_name = "NovaAssistant"

    def __init__(self) -> None:
        self.config = {}
        self.home = os.path.join(Path.home(), Config.standart_dir_name)

        self._get_config()

    def _get_config(self):
        # Check if config file exists
        os.makedirs(self.home, exist_ok=True)
        config_path = os.path.join(self.home, "config.json")
        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                json.dump(Config.standart_config, f)

        # reads file
        with open(config_path, "r") as f:
            self.config = json.load(f)
