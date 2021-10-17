from collections import defaultdict


class AudioProcessor:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }
        self.applitude = 2000
        self.time = 0
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)

    def on_tick(self, buffer, frame_count, rate, channels):
        # runs in audio thread
        self.poll_commands(self.time)

        for index in range(frame_count):
            tick = self.time + index/rate
            buffer[index] = 0
            for instrument, notes in self.tick(tick):
                for note in notes:
                    buffer[index] += instrument.sound(tick, note)
            buffer[index] = int(buffer[index] * self.applitude)

        self.time += frame_count/rate

    def tick(self, time):
        composition = defaultdict(list)
        for strategy in self.tracks:
            instrument, notes = strategy.tick(time)
            composition[instrument].extend(notes)

        for instruemnt, notes in composition.items():
            yield instruemnt, notes

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
        for track in self.tracks:
            track.on_press(note_id, time)

    def on_release(self, note_id, time):
        for track in self.tracks:
            track.on_release(note_id, time)
