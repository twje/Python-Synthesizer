from queue import Queue
from pynput import keyboard


class InputProcessor:
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

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.time = 0
        self.notes = set()
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
            if note_id not in self.notes:
                self.notes.add(note_id)
                self.event_bus.put({"on_press": note_id})

    def on_release(self, key):
        # input thread
        note_id = self.key_to_note_id(key)
        if note_id is not None:
            self.notes.remove(note_id)
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

        return self.NOTE_IDS.index(char)
