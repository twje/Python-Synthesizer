from note import Note


class Sequencer:
    def __init__(self, tempo, beats=4, sub_beats=4):
        self.tempo = tempo
        self.beats = beats
        self.sub_beats = sub_beats
        self.beat_time = 60 / (tempo * sub_beats)
        self.total_beats = beats * sub_beats
        self.current_beat = 0
        self.start_time = 0
        self.instruments = {}
        self.notes = []
        self.delete = []

    def tick(self, time):
        elapsed_time = time - self.start_time
        if elapsed_time >= self.beat_time:
            self.start_time = time + (self.beat_time - elapsed_time)
            self.current_beat += 1

            if self.current_beat >= self.total_beats:
                self.current_beat = 0

            for instrument, beat in self.instruments.items():
                if beat[self.current_beat] == "X":
                    note = Note(64, instrument, time, False)
                    self.notes.append(note)

        for note in self.notes:
            note.on_tick(time)
            if note.is_finished():
                self.delete.append(note)

        for note in self.delete:
            self.notes.remove(note)
        self.delete.clear()

        return self.notes

    def add_beat(self, instrument, beat):
        self.instruments[instrument] = beat

    def on_press(self, note_id, time):
        pass

    def on_release(self, note_id, time):
        pass
