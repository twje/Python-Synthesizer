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
        self.bell = Bell()

    def on_tick(self, time, frame_count, rate, channels):
        print(time, frame_count, rate, channels)
        # audio thread
        self.poll_commands(time)

        frames = []
        for index in range(frame_count):
            a = frame_count / rate
            b = a * index / frame_count
            c = time + b
            mixed_sound = 0
            for note in self.notes:
                mixed_sound += self.bell.sound(note, c)
                if note.is_finished():
                    note.destroy()
                    self.notes.remove(note)
            output = int(mixed_sound) * 2000
            frames.extend([output] * channels)

        return frames

        # mixed_output = 0
        # self.time = time
        # for note in self.notes:
        #     mixed_output += self.bell.sound(note, time)
        #     if note.is_finished():
        #         note.destroy()
        #         self.notes.remove(note)

        # return mixed_output * 1000

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
