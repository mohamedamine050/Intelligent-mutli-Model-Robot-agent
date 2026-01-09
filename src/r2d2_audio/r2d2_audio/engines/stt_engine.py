import whisper
import pyaudio
import wave

class STTEngine:
    def __init__(self):
        self.model = whisper.load_model("base")

    def record(self, filename="audio.wav", duration=3):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=1024)

        frames = []
        for _ in range(int(16000 / 1024 * duration)):
            frames.append(stream.read(1024))

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(filename, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
        wf.close()

    def transcribe(self):
        self.record()
        result = self.model.transcribe("audio.wav")
        return result["text"].strip()
