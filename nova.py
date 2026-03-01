import data.tts as TTS
import data.stt as STT
import data.logic as Logic

if __name__ == "__main__":
    tts = TTS.TTS()
    stt = STT.STT()
    
    @stt.recognize_speech
    def listen(recognizer, source) -> int:
        status = 0

        print("Listening...")

        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        text = recognizer.recognize_google(audio) # type: ignore
        text = text.lower()
        
        print("You said:", text)
        tts.speak(f"You said: {text}", "data/assets/audio/_temp.mp3")

        if "exit" in text:
            print("Exiting program...")
            status = -1

        return status
    
    listen()