from queue import Queue
import pyaudio
import struct


class Audio:
    def __init__(self, channels, rate, chunk, player):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk        
        self.player = player
        self.amplitude = 2000
        self.time = 0
        self.is_done = False
        self.data = Queue()                
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
        self.player.poll_commands(self.time)

        for index in range(frame_count):
            tick = self.time + index/self.rate
            self.buffer[index] = 0
            for instrument, notes in self.player.tick(tick):
                for note in notes:
                    self.buffer[index] += instrument.sound(tick, note)
            self.buffer[index] = int(self.buffer[index] * self.amplitude)

        self.time += frame_count/self.rate

        return self.serialize_data()

    def serialize_data(self):
        number_of_bytes = str(len(self.buffer))
        data = struct.pack(number_of_bytes + 'h', *self.buffer)
        self.data.put(data)
        status = pyaudio.paComplete if self.is_done == True else pyaudio.paContinue
        return (data, status)

    # ----------
    # Public API
    # ----------
    def stop(self):
        self.audio.terminate()

    def is_active(self):
        return self.stream.is_active()

    def empty(self):
        return self.data.empty()

    def get(self):
        return self.data.get()
