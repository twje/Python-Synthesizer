from instrument import Bell
from note import Note


class Player:
    def __init__(self, command_stream):
        self.command_stream = command_stream
        self.notes = []
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }

        # temp
        self.frame_count = 1024
        self.rate = 44100
        self.channels = 1
        self.bell = Bell()

    def play(self, time):
        self.poll_commands(time)
        mixed_output = 0
        for note in self.notes:
            mixed_output += self.bell.sound(note, time)
            if note.is_finished():
                note.destroy()
                self.notes.remove(note)

        return int(mixed_output) * 2000

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
