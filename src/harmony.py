from __future__ import print_function
import string
from scipy import stats
import json

# hooktheory actikey: 18c7027351e70830752fd8da22ca0e9b
# ('p', u'{"id":89986,"username":"suryabhupa","activkey":"18c7027351e70830752fd8da22ca0e9b"}')

# for now let's just do major keys

intervals = ['P1','m2','M2','m3','M3','P4','T','P5','m6','M6','m7','M7','P8']
major_intervals = [2,2,1,2,2,2,1]
minor_intervals = [2,1,2,2,1,2,2]

def key_intervals(is_major):
    if is_major: return major_intervals
    else: return minor_intervals

def roman_numerals(is_major):
    if is_major:
        return ['I','ii','iii','IV','V','vi','vii0']
    else:
        return ['i','ii0','III+','iv','V','VI','vii0']

# sharp based
def notes_in_octave(base='C'):
    notes_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    shift = notes_list.index(base)
    notes_list_key = notes_list[shift:] + notes_list[:shift]
    return notes_list_key

# interval is tuple (interval_name, 1 or -1)
def note_given_note_and_interval(note, interval):
    note_idx = notes_list.index(note)
    interval_shift = intervals.index(interval[0])
    return notes_list[note_idx+interval[1]*interval_shift]

def validate_chord(chord):
    return chord in set(["1", "2", "3", "4", "5", "6", "7"])



class Music(object):
    def __init__(self, keyname, chords):
        self.key = Key(keyname)
        self.chords = chords
        self.chord_chord_map = dict(json.loads('{"1": {"1": 0.364, "3": 0.036, "2": 0.061, "5": 0.254, "4": 0.183, "7": 0.003, "6": 0.099}, "3": {"1": 0.05, "3": 0.20299999999999996, "2": 0.082, "5": 0.074, "4": 0.319, "7": 0, "6": 0.272}, "2": {"1": 0.126, "3": 0.087, "2": 0.29200000000000004, "5": 0.156, "4": 0.156, "7": 0.001, "6": 0.182}, "5": {"1": 0.211, "3": 0.039, "2": 0.064, "5": 0.21799999999999997, "4": 0.205, "7": 0.001, "6": 0.262}, "4": {"1": 0.29, "3": 0.044, "2": 0.048, "5": 0.289, "4": 0.2340000000000001, "7": 0.002, "6": 0.093}, "7": {"1": 0.237, "3": 0.036, "2": 0.006, "5": 0.053, "4": 0.041, "7": 0.40900000000000003, "6": 0.218}, "6": {"1": 0.107, "3": 0.06, "2": 0.061, "5": 0.203, "4": 0.233, "7": 0.005, "6": 0.33099999999999996}}'))

    def get_next_chord(self, chord):
        """
        Given a chord, draws a random next chord according to its probability distribution.
        """
        assert validate_chord(chord)

        cond_dist_dict = self.chord_chord_map[chord]
        next_chords = cond_dist_dict.keys()
        next_probs = [cond_dist_dict[next_chord] for next_chord in next_chords]
        cond_dist = stats.rv_discrete(name='cond_dist', values=(next_chords, next_probs))

        return cond_dist.rvs(size=1)

class Key():
    def __init__(self, keyname):
        assert(keyname in self.possible_keys())
        self.keyname = keyname
        self.chromatic = notes_in_octave(string.upper(self.keyname))
        self.intervals = intervals
        self.is_major = keyname[0].isupper()
        self.notes = self.get_scale()
        self.romans = roman_numerals(self.is_major)
        self.chords = self.get_chords_in_key()
        # I actually should just have the key signature.

    def possible_keys(self):
        # minor keys
        lowers = list(string.ascii_lowercase[:7])

        # major keys
        uppers = list(string.ascii_uppercase[:7])

        # natural keys
        naturals = lowers + uppers

        # flats
        flats = [x+'b' for x in naturals]

        # sharps
        sharps = [x+'#' for x in naturals]

        return naturals + flats + sharps

    def get_scale(self):
        octave = notes_in_octave(self.keyname)
        i = 0
        scale = []
        for j in key_intervals(self.is_major):
            scale.append(octave[i])
            i+=j
        return scale

    # list of chords
    def get_chords_in_key(self):
        key_chords = []
        for i, base_note in enumerate(self.get_scale()):
            roman = roman_numerals(self.is_major)[i]
            third_interval = 'M3' if roman[0].isupper() else 'm3'
            third = self.apply_interval(base_note, third_interval)
            fifth_interval = 'P5' if i < 6 else 'T'
            fifth = self.apply_interval(base_note, fifth_interval)
            chord = (base_note, third, fifth)
            key_chords.append(chord)
        return key_chords

    # dimished before augmented
    def apply_interval(self, reference_note, interval):
        shift = self.intervals.index(interval)
        reference_index = self.chromatic.index(reference_note)
        return self.chromatic[(reference_index+shift)%12]

    # output: roman numeral or list of notes
    # assume that the note is in the key
    def c_chord_given_c_note(self, note):
        assert note in self.notes, 'note is not in key!'
        chords = []
        for c in self.chords:
            if note in c:
                chords.append(c)
        return chords



class Chord():
    def __init__(self, notes):
        self.notes = notes
        self.is_major = is_major(notes)

    # position: [0, 1, 2]
    def get_chord_intervals(is_major):
        if is_major:
            return ('M3','m3')
        else:
            return ('m3','M3')

key = Key('E')
print('keyname', key.keyname)
print('chromatic', key.chromatic)
print('intervals', key.intervals)
print('is_major', key.is_major)
print('notes', key.notes)
print('romans', key.romans)
print('chords', key.chords)
for i in ['C#', 'D','E','F#','G','A','B']:
    print('Given',i,key.c_chord_given_c_note(i))
