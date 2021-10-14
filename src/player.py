from collections import defaultdict


class Player:
    def __init__(self):
        self.tracks = []

    def tick(self, time):
        composition = defaultdict(list)
        for strategy in self.tracks:
            instrument, notes = strategy.tick(time)
            composition[instrument].extend(notes)

        for instruemnt, notes in composition.items():
            yield instruemnt, notes

    def on_press(self, note_id, time):
        for strategy in self.tracks:
            strategy.on_press(note_id, time)

    def on_release(self, note_id, time):
        for strategy in self.tracks:
            strategy.on_release(note_id, time)
