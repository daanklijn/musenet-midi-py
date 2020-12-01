from mido import Message, MidiFile, MidiTrack

INSTRUMENTS = ["piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano",
               "piano", "piano", "piano", "piano", "piano",
               "violin", "violin", "cello", "cello", "bass", "bass", "guitar", "guitar",
               "flute", "flute", "clarinet", "clarinet", "trumpet", "trumpet", "harp", "harp"]

TRACK_INDEX = {"piano": 0, "violin": 1, "cello": 2, "bass": 3, "guitar": 4, "flute": 5,
               "clarinet": 6, "trumpet": 7, "harp": 8, "drum": 9}
VOLUMES = [0, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 80, 0, 80, 0, 80, 0, 80, 0, 80,
           0, 80, 0, 80, 0, 80, 0]
DRUM_VELOCITY = 80
DELAY_MULTIPLIER = 10


def parse_token(token: int):
    if 0 <= token < 3840:
        note = token % 128
        inst_vol_index = token >> 7
        velocity = VOLUMES[inst_vol_index]
        instrument = INSTRUMENTS[inst_vol_index]
        track = TRACK_INDEX[instrument]
        return {"type": "note", "note": note, "channel": track, "velocity": velocity}
    elif 3840 <= token < 3968:
        note = token % 128
        return {"type": "note", "note": note, "channel": "drum", "velocity": DRUM_VELOCITY}
    elif 3968 <= token < 4096:
        delay = (token % 128) + 1
        return {"type": "wait", "time": delay}
    elif token == 4096:
        return {"type": "start"}
    else:
        return {"type": "invalid"}


# def decode(tokens: str):
#     midi = MidiFile()
#     track = MidiTrack()
#
#     tracks = {}
#
#     for token in tokens.split(' '):
#         parsed_token = parse_token(int(token))
#         if parsed_token['type'] == 'wait':
#             message.time = parsed_token['time'] * DELAY_MULTIPLIER
#         else:
#             message = Message(**parsed_token)
#             if message.channel in tracks:
#                 tracks[message.channel].append(message)
#             else:
#                 tracks[message.channel] = MidiTrack()
#                 tracks[message.channel].append(message)
#     for channel, track in tracks.items():
#         midi.tracks.append(track)
#
#     return midi


def decode(tokens):
    midi = MidiFile()
    tracks = [MidiTrack() for _ in range(10)]
    delta_times = [0 for _ in range(10)]
    for token in tokens.split():
        parsed = parse_token(int(token))
        type = parsed['type']
        if type == 'note':
            track_index = parsed['channel']
            volume = parsed['velocity']
            delay = delta_times[track_index]
            if delay > 0:
                parsed['time'] = delta_times[track_index] * DELAY_MULTIPLIER
            parsed['channel'] = track_index
            parsed['type'] = "note_on" if volume > 0 else "note_off"
            delta_times[track_index] = 0

            track = tracks[track_index]
            track.append(Message(**parsed))
        elif type == 'wait':
            for j in range(10):
                delta_times[j] += parsed['time']

    non_empty_tracks = [track for track in tracks if len(track) > 2]
    print(tracks)
    midi.tracks.extend(non_empty_tracks)
    return midi



def encode(file_path: str):
    mid = MidiFile(file_path)
    return ''.join([1234 for _ in mid])

with open('encoded2.txt', 'r') as file:
    tokens = file.read()

decoded_midi = decode(tokens)
decoded_midi.save('decoded_yann.mid')
# print(decoded_midi.tracks[1])
# for i in range(10):
#     print(decoded_midi.tracks[1][i])
# original_midi = MidiFile('decoded.mid')
# print(original_midi.tracks[1][2])
# print(decoded_midi.tracks[0][1])
# for i in range(10):
#     print(original_midi.tracks[2][i].channel)
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
