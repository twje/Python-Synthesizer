from queue import Queue
from pynput import keyboard


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
        self.event_bus = Queue()
        self.time = 0
        self.notes = []
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def start(self):
        self.listener.start()

    def on_press(self, key):
        # input thread
        note_id = self.key_to_note_id(key)
        if note_id is not None:
            self.event_bus.put({"on_press": note_id})

    def on_release(self, key):
        # input thread
        note_id = self.key_to_note_id(key)
        if note_id is not None:
            self.event_bus.put({"on_release": note_id})

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
