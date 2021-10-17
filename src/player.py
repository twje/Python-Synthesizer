from collections import defaultdict


class Player:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.actions = {
            "on_press": self.on_press,
            "on_release": self.on_release,
        }
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)

    def tick(self, time):
        composition = defaultdict(list)
        for strategy in self.tracks:
            instrument, notes = strategy.tick(time)
            composition[instrument].extend(notes)

        for instruemnt, notes in composition.items():
            yield instruemnt, notes

    def poll_commands(self, time):
        while not self.event_bus.empty():
            self.process_command(
                self.event_bus.get(),
                time
            )

    # --------------
    # Helper Methods
    # --------------
    def process_command(self, command, time):
        for action, note_id in command.items():
            self.actions[action](note_id, time)

    def on_press(self, note_id, time):
        for track in self.tracks:
            track.on_press(note_id, time)

    def on_release(self, note_id, time):
        for track in self.tracks:
            track.on_release(note_id, time)
