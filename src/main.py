from queue import Queue
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
        self.command_stream = Queue()
        self.lock = Lock()
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


class Player:
    def __init__(self, command_stream):
        self.command_stream = command_stream
        self.notes = []
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }

    def on_tick(self, time):
        self.poll_commands(time)

        # audio thread
        mixed_output = 0
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
    def poll_commands(self, time):
        while not self.command_stream.empty():
            self.process_command(
                self.command_stream.get(),
                time
            )

    def process_command(self, command, time):
        for action, note_id in command.items():
            self.actions[action](note_id, time)

    # ----------------
    # Callback Methods
    # ----------------
    def on_press(self, note_id, time):
        for note in self.notes:
            if note.idz == note_id:
                note.on_press(time)
                break
        else:
            self.notes.append(Note(note_id))

    def on_release(self, note_id, time):
        for note in self.notes:
            if note.idz == note_id:
                note.on_release(time)


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
