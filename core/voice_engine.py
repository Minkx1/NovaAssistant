import speech_recognition as sr
import edge_tts
import pygame as pg
import asyncio
import os
import time


class TextToSpeech:
    @staticmethod
    def _playsound(path):
        pg.mixer.music.load(path)
        pg.mixer.music.play()
        audio_clock = pg.time.Clock()
        while pg.mixer.music.get_busy():
            audio_clock.tick(10)
        pg.mixer.music.unload()

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

        TextToSpeech._playsound(output)  # Playing audio file

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
            time.sleep(0.1)  # Wait for file to finish playing
            try:
                os.remove(output)
            except FileNotFoundError:
                pass


class SpeechToText:
    def __init__(
        self,
        recognizer_config: dict = {
            "energy_threshold": 300,
            "dynamic_energy_threshold": True,
            "adjust_for_ambient_noise_duration": 1,
        },
    ) -> None:
        self.recognizer_config = recognizer_config

    def speech_recgonition(self, func):
        """
        Decorator ``speech_recognition`` can be put on function that has exactly 2 arguments and return ``status: int``: \n
        - recognizer: ``speech_recognition.Recognizer`` \n
        - source: ``speech_recognition.Microphone`` \n
        ``status``: 0 for normal status, not 0 for error and finish of the While-cycle.
        """

        def decorator(*args, **kwargs):
            r = sr.Recognizer()

            r.energy_threshold = self.recognizer_config.get("energy_threshold", 300)
            r.dynamic_energy_threshold = self.recognizer_config.get(
                "dynamic_energy_threshold", True
            )

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(
                    source,
                    self.recognizer_config.get("adjust_for_ambient_noise_duration", 1),
                )
                while True:
                    try:
                        status = func(r, source)
                        if status != 0:
                            break

                    except sr.RequestError as e:
                        print("Could not request results; {0}".format(e))
                    except sr.UnknownValueError:
                        pass
                    #     print("Could not understand audio")
                    except sr.WaitTimeoutError:
                        pass
                    except KeyboardInterrupt:
                        print("Program terminated by user.")
                        break

        return decorator


if __name__ == "__main__":
    TTS = TextToSpeech()
    STT = SpeechToText()

    @STT.speech_recgonition
    def test(recognizer: "sr.Recognizer", source: "sr.Microphone") -> int:
        status = 0

        print("Listening...")

        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        text = recognizer.recognize_google(audio)  # type: ignore
        text = text.lower()

        print("You said:", text)
        TTS.speak(f"You said: {text}")

        if "exit" in text:
            print("Exiting program...")
            status = -1

        return status

    test()  # type: ignore
