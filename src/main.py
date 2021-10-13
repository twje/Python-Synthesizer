from queue import Queue
from audio import Audio
from visualizer import Visualizer
from player import Player
from pynput import keyboard

audio = Audio(channels=1, rate=44100, chunk=1024)


class Processor:
    NOTE_IDS = [
        "z",  # a
        "s",  # a sharp
        "x",  # b
        "c",  # c
        "f",  # c sharap
        "v",  # d
        "g",  # d sharp
        "b",  # e
        "n",  # f
        "j",  # f sharp
        "m",  #
        "k",
    ]

    def __init__(self):
        self.command_stream = Queue()
        self.time = 0
        self.notes = []

    def on_press(self, key):
        # input thread
        note_id = self.key_to_note_id(key)
        if note_id is not None:
            self.command_stream.put({"on_press": note_id})

    def on_release(self, key):
        # input thread
        note_id = self.key_to_note_id(key)
        if note_id is not None:
            self.command_stream.put({"on_release": note_id})

    def key_to_note_id(self, key):
        char = None
        try:
            if key.char in self.NOTE_IDS:
                char = key.char
        except AttributeError:
            pass

        if char not in self.NOTE_IDS:
            return

        note_id = self.NOTE_IDS.index(char)
        for note in self.notes:
            if note.idz == note_id:
                return note

        return note_id


def create_processor():
    processor = Processor()
    listener = keyboard.Listener(
        on_press=processor.on_press,
        on_release=processor.on_release
    )
    listener.start()  # thibk about exit condition
    return processor


processor = create_processor()
player = Player(processor.command_stream)

visualizer = Visualizer(audio.chunk, audio.channels, scale=4)
with audio.generate(player.on_tick) as stream:
    while stream.is_active():
        if not stream.empty():
            pass
            visualizer.update(stream.get())
