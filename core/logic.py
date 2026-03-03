from rich import print
from rapidfuzz import fuzz, process
import os
import random
import importlib


class Logic:
    def __init__(self, config_obj) -> None:
        self.Config = config_obj
        self.modules = {}
        self._init_modules()

    def _init_modules(self):
        modules_dir = os.path.join(self.Config.home, "modules")

        if not os.path.exists(modules_dir):
            print(
                f"[bold yellow]Warning:[/bold yellow] Modules directory not found at {modules_dir}"
            )
            return

        for filename in os.listdir(modules_dir):
            if filename.endswith(".py"):
                module_name = filename[:-3]
                module_path = os.path.join(modules_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(
                        module_name, module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    self.modules[module_name] = module
                except Exception as e:
                    print(
                        f"[bold red]Failed to load module {module_name}:[/bold red] {e}"
                    )

        # print(f"[green]Successfully loaded {len(self.modules)} modules.[/green]")

    def run_module(self, key, command):
        """
        Runs module by key - name of module and command - original user command
        """
        module = self.modules.get(key)

        if not module:
            return None

        try:
            if hasattr(module, "main") and callable(module.main):
                result = module.main(self.Config, command)

                if isinstance(result, tuple) and len(result) == 2:
                    new_config, format_data = result
                    if new_config:
                        self.Config = new_config
                    return self.Config, format_data
                else:
                    print(
                        f"[yellow]Module {key} returned unexpected data format.[/yellow]"
                    )
                    return self.Config, {}

        except Exception as e:
            print(f"[bold red]Module Execution Error ({key}):[/bold red] {e}")
            return None

    def execute_command(self, key, command) -> str:
        """
        Executes module from key and returns radnom asnwer from key
        """
        # Getting random answer from keywords
        d = self.Config.keywords.get(key, {})  # type: ignore
        answers = d.get("answer", ["Command is not recognized."])
        res_idx = random.randint(0, len(answers) - 1)
        result = answers[res_idx]

        # formating answer and running module
        format_dict = dict(self.Config.config)  # type: ignore
        module_data = self.run_module(key, command)  # type: ignore
        if module_data:
            format_dict.update(module_data[1] or {})
            result = answers[res_idx].format(**format_dict)
        else:
            print(f"[bold red]Module Error ({key}):[/bold red] file not found.")
        return result

    def recognize_command(self, command: str) -> str:
        """
        Returns ``key of command`` in the keywords.
        """

        cmd_lower = command.lower().strip()
        name = self.Config.get("name", "Nova").lower()  # type: ignore

        if name not in cmd_lower:
            return ""
        clean_command = cmd_lower.replace(name, "").strip()
        if not clean_command:
            return ""

        is_sleeping = self.Config.get("sleep", False)  # type: ignore
        best_key = None
        max_score = 0

        for key, data in self.Config.keywords.items():  # type: ignore
            if is_sleeping and key != "sleep_mode_off":
                continue

            phrases = data.get("ask", [])
            for p in phrases:
                p_lower = p.lower()

                if p_lower in clean_command or clean_command in p_lower:
                    return key

                score = fuzz.ratio(clean_command, p_lower)
                if score > max_score:
                    max_score = score
                    best_key = key

        if best_key and max_score > 80:
            return best_key

        return ""

    def print(self, text: str) -> None:
        print(f"[red bold][{self.Config.get('name')}][/red bold]: {text}")
