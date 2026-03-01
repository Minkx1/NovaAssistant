from tts import TTS, playsound
from rich import print
from rapidfuzz import fuzz, process
import os, json
import random
import importlib


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
    standart_keywords: dict[str, dict] = {
        "greeting": {
            "only_answer": True,
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
        config_path = os.path.join(self.home, "config.json")
        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                json.dump(Config.standart_config, f)

        with open(config_path, "r") as f:
            self.config = json.load(f)

    def _get_keywords(self):
        keywords_path = os.path.join(self.home, "keywords.json")
        if not os.path.exists(keywords_path):
            with open(keywords_path, "w") as f:
                json.dump(Config.standart_keywords, f)

        with open(keywords_path, "r") as f:
            self.keywords = json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(
            key, default if default else Config.standart_config.get(key, None)
        )


class NovaLogic:
    def __init__(self, config_obj: Config) -> None:
        self.Config = config_obj
        self.Speaker = TTS(self.Config.get("voice"))

    def speak(
        self,
        text: str,
        file: str = None,
        output: str = "_temp_.mp3",
        save_audio: bool = False,
    ):
        try:
            if file and os.path.exists(file):
                playsound(file)
            else:
                self.Speaker.speak(text, output, save_audio=save_audio)
        except Exception as e:
            print(f"[red]TTS Error:[/red] {e}")

    def _run_module(self, key, command, result):
        module_path = os.path.join(self.Config.home, "data", "modules", f"{key}.py")
        if not os.path.exists(module_path):
            return

        try:
            spec = importlib.util.spec_from_file_location(key, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "main") and callable(module.main):
                new_config = module.main(self.Config, command, result)
                if new_config:
                    self.Config = new_config
        except Exception as e:
            print(f"[bold red]Module Error ({key}):[/bold red] {e}")

    def _execute_command(self, key, command) -> str:
        d = self.Config.keywords.get(key, {})
        answers = d.get("answer", ["Command is not recognized."])

        res_idx = random.randint(0, len(answers) - 1)
        result = answers[res_idx].format(**self.Config.config)

        sfx_dir = os.path.join(self.Config.home, "data", "sfx", key)
        os.makedirs(sfx_dir, exist_ok=True)
        audio_file = os.path.join(sfx_dir, f"{res_idx}.mp3")

        print(f"[red bold][{self.Config.get('name')}][/red bold]: {result}")

        if os.path.exists(audio_file):
            self.speak(result, file=audio_file)
        else:
            self.speak(result, output=audio_file, save_audio=False)

        self._run_module(key, command, result)

        return result

    def execute(self, command: str) -> int:
        print(f"[cyan bold][You][/cyan bold]: {command}")
        cmd_lower = command.lower().strip()
        name = self.Config.get("name", "Nova").lower()

        if name not in cmd_lower:
            return 0

        clean_command = cmd_lower.replace(name, "").strip()
        if not clean_command:
            return 0

        is_sleeping = self.Config.get("sleep", False)
        best_key = None
        max_score = 0

        for key, data in self.Config.keywords.items():
            if is_sleeping and key != "sleep_mode_off":
                continue
            if data.get("only_answer"):
                continue

            phrases = data.get("ask", [])
            for p in phrases:
                p_lower = p.lower()

                if p_lower in clean_command or clean_command in p_lower:
                    return self._execute_command(key, command)

                score = fuzz.ratio(clean_command, p_lower)
                if score > max_score:
                    max_score = score
                    best_key = key

        if best_key and max_score > 80:
            return self._execute_command(best_key, command)

        print(f"[yellow][{self.Config.get('name')}][/yellow]: Command not recognized.")
        return 0
