import edge_tts
import pygame as pg
import asyncio
import os


def playsound(path):
    pg.mixer.music.load(path)
    pg.mixer.music.play()
    audio_clock = pg.time.Clock()
    while pg.mixer.music.get_busy():
        audio_clock.tick(10)
    pg.mixer.music.unload()


class TTS:
    def __init__(
        self,
        voice_config: dict = {
            "voice": "en-US-GuyNeural",
            "rate": "+20%",
            "volume": "+10%",
            "pitch": "+0Hz",
        },
    ) -> None:
        pg.mixer.init()
        self.voice = voice_config

    async def _async_speak(
        self,
        text: str,
        output: str,
    ) -> None:
        communicate = edge_tts.Communicate(
            text,
            voice=self.voice["voice"],
            rate=self.voice["rate"],
            volume=self.voice["volume"],
            pitch=self.voice["pitch"],
        )
        await communicate.save(output)  # Generate audio file

        playsound(output)  # Playing audio file

    def speak(
        self,
        text: str,
        output: str = "_temp_.mp3",
        save_audio=False,
    ):
        """
        Speaks text with parameteres from ``Speaker``. \n
        Args:
        - ``text``: text that will be spoken. \n
        - ``output``: name of file that will be generated, if you need to save generated file. \n
        - ``save_audio``: put **True** if you want to save that speech.

        """
        asyncio.run(self._async_speak(text, output))
        if not save_audio:
            os.remove(output)


if __name__ == "__main__":
    from logic import Config

    C = Config()
    V = TTS()

    for key in C.keywords.keys():
        os.makedirs(f"data/sfx/{key}/", exist_ok=True)
        for i, phrase in enumerate(C.keywords[key]["answer"]):
            file = f"data/sfx/{key}/{i}.mp3"
            if not os.path.exists(file):
                V.speak(str(phrase).format(**C.config), output=file, save_audio=True)
