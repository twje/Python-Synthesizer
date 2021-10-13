from instrument import Bell
from note import Note


class Player:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.notes = []
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }
        self.time = 0
        self.bell = Bell()

    def on_tick(self, buffer, frame_count, rate, channels):
        self.poll_commands(self.time)

        frames = []
        for index in range(frame_count):
            tick = self.time + index/rate
            buffer[index] = self.sound(tick)

        self.time += frame_count/rate
        return frames

    def sound(self, tick):
        # audio thread
        mixed_output = 0
        for note in self.notes:
            mixed_output += self.bell.sound(note, tick)
            if note.is_finished():
                note.destroy()
                self.notes.remove(note)

        return int(mixed_output * 1000)

    # --------------
    # Helper Methods
    # --------------
    def poll_commands(self, time):
        while not self.event_bus.empty():
            self.process_command(
                self.event_bus.get(),
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
