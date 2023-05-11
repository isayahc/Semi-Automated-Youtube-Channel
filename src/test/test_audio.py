import os
import tempfile
import pytest
from pydub import AudioSegment
from pyttsx3 import init
import shutil
from ..audio.concate_audio import (
    get_sorted_audio_files,
    combine_audio_files_directory,
    combine_audio_files_with_random_pause,
)


@pytest.fixture
def audio_files_directory():
    # Create a temporary directory for the audio files
    temp_dir = tempfile.mkdtemp()

    # Create temporary audio files in the directory
    audio_files = ['file1.wav', 'file2.wav', 'file3.wav']
    for audio_file in audio_files:
        file_path = os.path.join(temp_dir, audio_file)
        generate_audio("Sample audio", file_path)  # Generate sample audio using TTS

    yield temp_dir

    # Clean up the temporary directory and files after the test
    for audio_file in audio_files:
        file_path = os.path.join(temp_dir, audio_file)
        os.remove(file_path)
    shutil.rmtree(temp_dir, ignore_errors=True)

def generate_audio(text, output_file):
    engine = init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()

def test_get_sorted_audio_files(audio_files_directory):
    expected_files = [
        os.path.join(audio_files_directory, 'file1.wav'),
        os.path.join(audio_files_directory, 'file2.wav'),
        os.path.join(audio_files_directory, 'file3.wav'),
    ]
    assert get_sorted_audio_files(audio_files_directory) == expected_files


def test_combine_audio_files_directory(audio_files_directory):
    output_file = os.path.join(audio_files_directory, 'combined_audio.wav')
    combined_audio = combine_audio_files_directory(audio_files_directory, output_file)
    assert isinstance(combined_audio, AudioSegment)
    assert os.path.isfile(output_file)


def test_combine_audio_files_with_random_pause(audio_files_directory):
    output_file = os.path.join(audio_files_directory, 'combined_audio.wav')
    combined_audio = combine_audio_files_with_random_pause(audio_files_directory, output_file)
    assert isinstance(combined_audio, AudioSegment)
    assert os.path.isfile(output_file)


# Additional tests can be added as needed
