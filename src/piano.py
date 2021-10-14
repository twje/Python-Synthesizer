from instrument import Bell
from note import Note


class Piano:
    def __init__(self):
        self.bell = Bell()
        self.notes = []
        self.delete = []
        self.playing = []

    def tick(self, time):
        self.playing.clear()
        for note in self.notes:
            note.envelope.on_tick(time)
            if note.envelope.is_finished():
                self.delete.append(note)
            else:
                self.playing.append(note)

        for note in self.delete:
            self.notes.remove(note)
        self.delete.clear()

        return self.bell, self.playing

    def on_press(self, note_id, time):
        for note in self.notes:
            if note.idz == note_id:
                note.envelope.on_press(time)
                break
        else:
            note = Note(note_id, self.bell.envelope_factory(time))
            self.notes.append(note)

    def on_release(self, note_id, time):
        for note in self.notes:
            if note.idz == note_id:
                note.envelope.on_release(time)
