from queue import Queue
import pyaudio
import struct
from instrument import Bell


class Audio:
    def __init__(self, channels, rate, chunk):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.oscillator = None

    def generate(self, callback):
        return self.Oscillator(
            self.channels,
            self.rate,
            self.chunk,
            callback
        )

    class Oscillator:
        def __init__(self, channels, rate, chunk, callback):
            self.channels = channels
            self.rate = rate
            self.chunk = chunk
            self.callback = callback
            self.data = Queue()
            self.time = 0
            self.done = False
            self.bell = Bell()

            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk,
                output=True,
                stream_callback=self,
            )
            self.stream.start_stream()

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

        def __call__(self, *args, **kwgs):
            # runs in audio thread
            frames = self.callback(
                args[1],
                self.rate,
                self.channels
            )
            number_of_bytes = str(len(frames))
            data = struct.pack(number_of_bytes + 'h', *frames)
            self.data.put(data)
            status = pyaudio.paComplete if self.done == True else pyaudio.paContinue
            return (data, status)

        def foo(self, c, notes):
            # audio thread
            mixed_output = 0
            for note in notes:
                mixed_output += self.bell.sound(note, c)
                if note.is_finished():
                    note.destroy()
                    notes.remove(note)

            return int(mixed_output * 1000)

        def is_active(self):
            return self.stream.is_active()

        def empty(self):
            return self.data.empty()

        def get(self):
            return self.data.get()
