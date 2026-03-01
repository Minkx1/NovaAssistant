import stt as stt
import logic as logic

if __name__ == "__main__":
    Config = logic.Config()
    Logic = logic.NovaLogic(Config)
    Listener = stt.STT(Config.config.get("recognizer_config", {}))

    Logic._execute_command("greeting", "")

    @Listener.recognize_speech
    def listen(recognizer, source) -> int:
        status = 0

        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        text = recognizer.recognize_google(audio)  # type: ignore
        text = text.lower()

        Logic.execute(text)

        if not Config.get("active", True):
            status = -1

        return status

    listen()  # type: ignore
