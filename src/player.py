from collections import defaultdict


class Player:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }
        self.tracks = []
        self.time = 0
        self.amplitude = 4000

    def add_track(self, track):
        self.tracks.append(track)

    # --------------
    # Helper Methods
    # --------------
    def on_tick(self, buffer, frame_count, rate):
        self.poll_commands(self.time)

        for index in range(frame_count):
            tick = self.time + index/rate
            buffer[index] = 0
            for track in self.tracks:
                for note in track.tick(tick):
                    buffer[index] += note.play(tick)
            buffer[index] = int(buffer[index] * self.amplitude)

        self.time += frame_count/rate
        return buffer

    def poll_commands(self, time):
        while not self.event_bus.empty():
            self.process_command(
                self.event_bus.get(),
                time
            )

    def process_command(self, command, time):
        for action, note_id in command.items():
            self.actions[action](note_id, time)

    def on_press(self, note_id, time):
        for track in self.tracks:
            track.on_press(note_id, time)

    def on_release(self, note_id, time):
        for track in self.tracks:
            track.on_release(note_id, time)
