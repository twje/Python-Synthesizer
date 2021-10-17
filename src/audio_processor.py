from player import Player


class AudioProcessor:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }
        self.player = Player()
        self.applitude = 2000
        self.time = 0

    def add_track(self, track):
        self.player.tracks.append(track)

    def on_tick(self, buffer, frame_count, rate, channels):
        # runs in audio thread
        self.poll_commands(self.time)

        for index in range(frame_count):
            tick = self.time + index/rate
            buffer[index] = 0
            for instrument, notes in self.player.tick(tick):
                for note in notes:
                    buffer[index] += instrument.sound(tick, note)
            buffer[index] = int(buffer[index] * self.applitude)

        self.time += frame_count/rate

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
        self.player.on_press(note_id, time)

    def on_release(self, note_id, time):
        self.player.on_release(note_id, time)
