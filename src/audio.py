import pyaudio
import struct
from plugin import Plugin


class Audio(Plugin):
    def __init__(self, channels, rate, chunk, player):
        super().__init__()
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.player = player
        self.amplitude = 2000
        self.time = 0
        self.is_done = False
        self.buffer = [0] * self.chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None

    # ------------------------
    # Context Manager Protocol
    # ------------------------
    def __enter__(self):
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=self.chunk,
            output=True,
            stream_callback=self.on_tick,
        )
        self.stream.start_stream()
        return self

    def __exit__(self, type, value, traceback):
        self.stream.stop_stream()
        self.stream.close()

    # -----------------
    # Heartbeat Methods
    # -----------------
    def on_tick(self, in_data, frame_count, time_info, status):
        data = self.convert_data(
            self.player.on_tick(
                self.buffer,
                self.chunk,
                self.rate
            )
        )
        self.prime_plugins(data)

        status = pyaudio.paComplete if self.is_done == True else pyaudio.paContinue
        return (data, status)

    def convert_data(self, data):
        number_of_bytes = str(len(data))
        return struct.pack(number_of_bytes + 'h', *data)

    # ----------
    # Public API
    # ----------
    def stop(self):
        self.audio.terminate()

    def is_active(self):
        return self.stream.is_active()
