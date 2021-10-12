from instrument import Bell
from audio import Audio
from visualizer import Visualizer
from note import Note
from threading import Lock
from pynput import keyboard

audio = Audio(channels=1, rate=44100, chunk=1024)


bell = Bell()


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
        self.lock = Lock()
        self.time = 0
        self.notes = []

    def on_press(self, key):
        # input thread
        with self.lock:
            note = self.get_note(key)
            if note is not None:
                note.on_press(self.time)

    def on_release(self, key):
        # input thread
        with self.lock:
            note = self.get_note(key)
            if note is not None:
                note.on_release(self.time)

    def on_tick(self, time):
        # audio thread
        mixed_output = 0
        with self.lock:
            self.time = time
            for note in self.notes:
                mixed_output += bell.sound(note, time)
                if note.is_finished():
                    note.destroy()
                    self.notes.remove(note)

        return mixed_output * 1000

    # --------------
    # Helper Methods
    # --------------
    def get_note(self, key):
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

        note = Note(note_id)
        self.notes.append(note)

        return note


def create_processor():
    processor = Processor()
    listener = keyboard.Listener(
        on_press=processor.on_press,
        on_release=processor.on_release
    )
    listener.start()  # thibk about exit condition
    return processor


visualizer = Visualizer(audio.chunk, audio.channels, scale=4)
processor = create_processor()
with audio.generate(processor.on_tick) as stream:
    while stream.is_active():
        if not stream.empty():
            pass
            visualizer.update(stream.get())
