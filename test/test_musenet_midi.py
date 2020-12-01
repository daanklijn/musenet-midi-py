import pytest
from mido import MidiFile

from musenet_midi_py import encode, decode


class TestMusenetMidi:
    def test_encode(self):
        assert True

    def test_decode(self):
        with open('encoded.txt') as file:
            tokens = file.read()
        decoded_midi = decode(tokens)
        original_midi = MidiFile('decoded.mid')
        assert decoded_midi == original_midi

