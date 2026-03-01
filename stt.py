import speech_recognition as sr


class STT:
    def __init__(
        self,
        recognizer_config: dict = {
            "energy_threshold": 300,
            "dynamic_energy_threshold": True,
            "adjust_for_ambient_noise_duration": 1,
        },
    ) -> None:
        self.config = recognizer_config

    def recognize_speech(self, func):
        """
        Decorator ``stt`` can be handled on function that has exactly 2 arguments and return ``status: int``: \n
        - recognizer: ``speech_recognition.Recognizer`` \n
        - source: ``speech_recognition.Microphone`` \n
        ``status``: 0 for normal status, not 0 for error and finish of the While-cycle.
        """

        def decorator():
            r = sr.Recognizer()

            r.energy_threshold = self.config.get("energy_threshold", 300)
            r.dynamic_energy_threshold = self.config.get(
                "dynamic_energy_threshold", True
            )

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(
                    source, self.config.get("adjust_for_ambient_noise_duration", 1)
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
    stt = STT()

    @stt.recognize_speech
    def test(recognizer: "sr.Recognizer", source: "sr.Microphone") -> int:
        status = 0

        print("Listening...")

        # recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        text = recognizer.recognize_google(audio)  # type: ignore
        text = text.lower()
        print("You said:", text)

        if "exit" in text:
            print("Exiting program...")
            status = -1

        return status
