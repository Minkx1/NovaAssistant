import os, json


class Config:
    standart_config = {
        "name": "Nova",
        "user_nickname": "Sir",
        "sleep": False,
        "active": True,
        "voice": {
            "voice": "en-US-GuyNeural",
            "rate": "+20%",
            "volume": "+100%",
            "pitch": "+0Hz",
        },
        "recognizer_config": {
            "energy_threshold": 300,
            "dynamic_energy_threshold": True,
            "adjust_for_ambient_noise_duration": 1,
        },
    }
    standart_keywords = {
        "greeting": {
            "ask": ["Hello", "Hi", "Wassup", "Whats Up"],
            "answer": [
                "Greetings, {user_nickname}!",
                "Welcome back, {user_nickname}.",
                "I am glad to assist you, {user_nickname}.",
            ],
        },
        "kill": {
            "ask": ["Good bye", "Bye", "Exit", "Quit"],
            "answer": [
                "Good bye, {user_nickname}.",
                "Have a great day, {user_nickname}.",
            ],
        },
        "sleep_mode_on": {
            "ask": ["Good Night", "Go to sleep", "Sleep mode"],
            "answer": ["Going to sleep...", "Good night..."],
        },
        "sleep_mode_off": {
            "ask": ["Wake Up"],
            "answer": [
                "Greetings, {user_nickname}!",
                "Welcome back, {user_nickname}.",
                "I am glad to assist you, {user_nickname}.",
            ],
        },
    }

    def __init__(self) -> None:
        self.config = {}
        self.keywords: dict[str, dict] = {}
        self.home: str = os.getcwd()

        self._get_config()
        self._get_keywords()

    def _get_config(self):
        config_path = os.path.join(self.home, "data", "configs", "config.json")
        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                json.dump(Config.standart_config, f)

        with open(config_path, "r") as f:
            self.config = json.load(f)

    def _get_keywords(self):
        keywords_path = os.path.join(self.home, "data", "configs", "keywords.json")
        if not os.path.exists(keywords_path):
            with open(keywords_path, "w") as f:
                json.dump(Config.standart_keywords, f)

        with open(keywords_path, "r") as f:
            self.keywords = json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(
            key, default if default else Config.standart_config.get(key, None)
        )
