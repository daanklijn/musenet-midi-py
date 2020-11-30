from mido import Message, MidiFile, MidiTrack

INSTRUMENTS = ["piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano",
               "piano", "piano", "piano", "piano", "piano",
               "violin", "violin", "cello", "cello", "bass", "bass", "guitar", "guitar",
               "flute", "flute", "clarinet", "clarinet", "trumpet", "trumpet", "harp", "harp"]
VOLUMES = [0, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 80, 0, 80, 0, 80, 0, 80, 0, 80,
           0, 80, 0, 80, 0, 80, 0]
DRUM_VELOCITY = 80
DELAY_MULTIPLIER = 10


def parse_token(token: int):
    if 0 <= token < 3840:
        note = token % 128
        inst_vol_index = token >> 7
        velocity = VOLUMES[inst_vol_index]
        return {"type": "note_on", "note": note, "channel": inst_vol_index, "velocity": velocity}
    elif 3840 <= token < 3968:
        note = token % 128
        return {"type": "note_on", "note": note, "channel": "drum", "velocity": DRUM_VELOCITY}
    elif 3968 <= token < 4096:
        delay = (token % 128) + 1
        return {"type": "wait", "delay": delay}
    elif token == 4096:
        return {"type": "start"}
    else:
        return {"type": "invalid"}


def decode(tokens: str):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    for token in tokens:
        parsed_token = parse_token(int(token))
        if parsed_token['type'] == 'wait':
            message.time = parsed_token['delay'] * DELAY_MULTIPLIER
        else:
            message = Message(**parsed_token)
            track.append(message)
    return midi


def encode(file_path: str):
    mid = MidiFile(file_path)
    return ''.join([1234 for _ in mid])

# with open('abc.mid', 'r') as file:
#     tokens = file.read().split()
#
#
# mid2.save('new_song.mid')
#
# mid = MidiFile('abc2.mid')
# messages1 = [message for message in mid]
# messages2 = [message for message in mid2]
# for i in range(min(len(messages1), len(messages2))):
#     print(f'ORIGINAL: {messages1[i]}')
#     print(f'NEW:      {messages2[i]}')
