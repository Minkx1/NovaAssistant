from core.voice_engine import SpeechToText, TextToSpeech
import core.logic as logic
import core.config as config
from rich import print
import threading

if __name__ == "__main__":
    Config = config.Config()
    Logic = logic.Logic(Config)
    STT, TTS = SpeechToText(Config.config.get("recognizer_config", {})), TextToSpeech(
        Config.get("voice")
    )

    greet = Logic.execute_command("greeting", "")
    Logic.print(greet)
    TTS.speak(greet)

    # print(Logic.recognize_command("nova hi"))

    @STT.speech_recgonition
    def listen(recognizer, source) -> int:
        status = 0

        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        cmd = recognizer.recognize_google(audio)  # type: ignore

        print(f"[cyan bold][You][/cyan bold]: {cmd}")
        cmd = cmd.lower()

        cmd_key = Logic.recognize_command(cmd)
        if cmd_key:
            result = Logic.execute_command(cmd_key, cmd)

            Logic.print(result)
            TTS.speak(result)

        if not Config.get("active", True):
            status = -1

        return status

    assistant_thread = threading.Thread(target=listen, daemon=True)
    assistant_thread.start()

    # for not closing main thread
    try:
        from time import sleep
        while assistant_thread.is_alive():
            sleep(0.1)
    except KeyboardInterrupt:
        pass
