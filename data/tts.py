import edge_tts
import pygame as pg
import asyncio
import os


class TTS:
    def __init__(
        self,
        voice_config: dict = {
            "voice": "en-US-GuyNeural",
            "rate": "+20%",
            "volume": "+10%",
            "pitch": "+0Hz",
        }
    ) -> None:
        pg.mixer.init()
        self.voice = voice_config

    async def _async_speak(
        self,
        text: str,
        output: str = "speech.mp3",
    ) -> None:
        communicate = edge_tts.Communicate(
            text,
            voice=self.voice["voice"],
            rate=self.voice["rate"],
            volume=self.voice["volume"],
            pitch=self.voice["pitch"],
        )
        await communicate.save(output)  # Generate audio file

        pg.mixer.music.load(output)
        pg.mixer.music.play()
        audio_clock = pg.time.Clock()
        while pg.mixer.music.get_busy():
            audio_clock.tick(10)
        pg.mixer.music.unload()  # Playing audio file


    def speak(
        self,
        text: str,
        output: str = "speech.mp3",
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
    text = input() or "Greetings, sir!"
    file = "data/assets/audio/_temp_speech.mp3"

    v = TTS()
    v.speak(text, file)
