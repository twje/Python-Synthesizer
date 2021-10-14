from audio_processor import AudioProcessor
from input_processor import InputProcessor


def create_audio_processor():
    processor = InputProcessor()
    processor.start()
    return AudioProcessor(processor.event_bus)
