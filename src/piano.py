from note import Note


class Piano:
    def __init__(self, instrument):        
        self.instrument = instrument
        self.notes = []
        self.delete = []
        self.playing = []

    def tick(self, time):
        self.playing.clear()
        for note in self.notes:
            note.on_tick(time)
            if note.is_finished():
                self.delete.append(note)
            else:
                self.playing.append(note)

        for note in self.delete:
            self.notes.remove(note)
        self.delete.clear()

        return self.playing

    def on_press(self, index, time):
        for note in self.notes:
            if note.index == index:
                note.on_press(time)
                break
        else:
            note = Note(index, self.instrument, time)
            self.notes.append(note)

    def on_release(self, index, time):
        for note in self.notes:
            if note.index == index:
                note.on_release(time)
