from __future__ import print_function
import string
from scipy import stats
import json
import random

# hooktheory actikey: 18c7027351e70830752fd8da22ca0e9b
# ('p', u'{"id":89986,"username":"suryabhupa","activkey":"18c7027351e70830752fd8da22ca0e9b"}')

# for now let's just do major keys

intervals = ['P1','m2','M2','m3','M3','P4','T','P5','m6','M6','m7','M7','P8']
major_intervals = [2,2,1,2,2,2,1]
minor_intervals = [2,1,2,2,1,2,2]
range_names = ['bass', 'tenor', 'alto', 'soprano']

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
    # print(chord)
    return chord in set(["1", "2", "3", "4", "5", "6", "7"])


class Music(object):
    def __init__(self, keyname,seed_notes=None,chords=None):
        self.key = Key(keyname) # Key
        print(self.key)
        print('Dadfja;lsdfjasl;dfjsal;dkfjsdl;fj')
        # self.seed_notes = seed_notes
        # self.chords = chords # Specified chords
        self.chord_chord_map = dict(json.loads('{"1": {"1": 0.364, "3": 0.036, "2": 0.061, "5": 0.254, "4": 0.183, "7": 0.003, "6": 0.099}, "3": {"1": 0.05, "3": 0.20299999999999996, "2": 0.082, "5": 0.074, "4": 0.319, "7": 0, "6": 0.272}, "2": {"1": 0.126, "3": 0.087, "2": 0.29200000000000004, "5": 0.156, "4": 0.156, "7": 0.001, "6": 0.182}, "5": {"1": 0.211, "3": 0.039, "2": 0.064, "5": 0.21799999999999997, "4": 0.205, "7": 0.001, "6": 0.262}, "4": {"1": 0.29, "3": 0.044, "2": 0.048, "5": 0.289, "4": 0.2340000000000001, "7": 0.002, "6": 0.093}, "7": {"1": 0.237, "3": 0.036, "2": 0.006, "5": 0.053, "4": 0.041, "7": 0.40900000000000003, "6": 0.218}, "6": {"1": 0.107, "3": 0.06, "2": 0.061, "5": 0.203, "4": 0.233, "7": 0.005, "6": 0.33099999999999996}}'))
        self.voice = Voice()

    def specified_chord_to_chord(self, spec_chord):
        copy = list(spec_chord[:])
        for i in range(len(copy)):
            copy[i] = copy[i][:-1]

        copy = list(set(copy))
        # print('copy', copy)
        assert len(copy) == 3
        for chord in self.key.chords:
            flag = True
            for c in copy:
                if c not in chord:
                    flag = False
            if flag == True:
                return str(self.key.chords.index(chord)+1)

    def get_next_chord(self, chord):
        """
        Given a chord, draws a random next chord according to its probability distribution.
        """
        chord = self.specified_chord_to_chord(chord)
        assert validate_chord(chord), "not a valid chord!"

        cond_dist_dict = self.chord_chord_map[chord] # Gets list of candidate chords

        # Prepare for the random draw
        next_chords = cond_dist_dict.keys()
        next_probs = [cond_dist_dict[next_chord] for next_chord in next_chords]
        cond_dist = stats.rv_discrete(name='cond_dist', values=(next_chords, next_probs))

        return self.key.chords[cond_dist.rvs(size=1)-1]

    def get_next_chord_conditional(self, chord, note):
        """
        Given a chord, draws a random next chord according to its probability distribution conditioned
        on the proceeding note.
        note here is a note
        """
        chords = self.key.c_chord_given_c_note(note[:-1])
        idxs = []
        for j in range(len(chords)):
            for i in range(len(self.key.chords)):
                if chords[j] == self.key.chords[i]:
                    idxs.append(i)

        idxs = list(set(idxs))

        chord = self.specified_chord_to_chord(chord)
        cond_dist_dict = self.chord_chord_map[chord] # Gets list of candidate chords
        next_chords = sorted(cond_dist_dict.keys())
        next_probs = [cond_dist_dict[next_chord] for next_chord in next_chords]

        true_next_chords = [next_chords[int(i)] for i in idxs]
        true_next_probs = [next_probs[int(i)] for i in idxs]

        allsum = sum(true_next_probs)

        for i in range(len(true_next_probs)):
            true_next_probs[i] = true_next_probs[i] / allsum


        cond_dist = stats.rv_discrete(name='cond_dist', values=(true_next_chords, true_next_probs))
        return self.key.chords[cond_dist.rvs(size=1)-1]


    # abs value
    def cost_function(self, note1, note2):
        octave1 = int(note1[-1])
        octave2 = int(note2[-1])
        letters_to_num = {"C": 1, "C#": 2, "D": 3, "D#": 4, "E": 5, "F": 6, "F#": 7, "G": 8, "G#": 9, "A": 10, "A#": 11, "B": 12}
        return abs((letters_to_num[note1[:-1]] + octave1*12) - (letters_to_num[note2[:-1]] + octave2*12))

    def sort_func(self, note1, note2):
        octave1 = int(note1[-1])
        octave2 = int(note2[-1])
        letters_to_num = {"C": 1, "C#": 2, "D": 3, "D#": 4, "E": 5, "F": 6, "F#": 7, "G": 8, "G#": 9, "A": 10, "A#": 11, "B": 12}
        return ((letters_to_num[note1[:-1]] + octave1*12) - (letters_to_num[note2[:-1]] + octave2*12))


    def filter_bass(enumerations, chord):
        return [c for c in enumerations['bass'] if c[0][0] == chord[0]]

    # chord should be ordered from lowest note to highest note
    def get_specified_chord_from_note_and_chord(self, specified_note, chord, previous_specified_chord=None):
        # 1. enumerate chord
        # 2. compute cost function
        # 2. filter
        # enumerations = {self.voice.specified_chord_given_range_name(chord, range_name)
        #                for range_name in range_names}
        # enumerations = filter_bass(enumerations, chord)
        # # expand enumerations
        # enumerations = [((range_name, chord_note) for chord_note in enumerations[range_name]) for range_name in range_names]
        # enumerations = filter_triad(enumerations, chord)

        assert(len(chord) == 3)
        soprano = specified_note
        bass = self.voice.specified_note_given_note(chord[0], 'bass')
        leftovers = [c for c in chord if c != bass[:-1] and c!= soprano[:-1]]
        if previous_specified_chord == None:
            tenor = self.voice.specified_note_given_note(random.choice(leftovers), 'alto')
            if bass[:-1] != soprano[:-1]:
                alto =  self.voice.specified_note_given_note(random.choice(chord), 'alto')
            else:
                leftovers = [c for c in chord if c != bass[:-1] and c!= soprano[:-1] and c!= tenor[:-1]]
                alto =  self.voice.specified_note_given_note(random.choice(leftovers), 'alto')
        else:
            if bass[:-1] != soprano[:-1]:
                tenor = self.get_closest_specified_note_given_note(previous_specified_chord[1], chord, 'tenor')
                leftovers = [c for c in chord if c != bass[:-1] and c!= soprano[:-1] and c!= tenor[:-1]]
                if len(leftovers) == 0:
                    alto =  self.voice.specified_note_given_note(random.choice(chord), 'alto')
                else:
                    alto = self.voice.specified_note_given_note(random.choice(leftovers), 'alto')
            else:
                if self.get_closest_specified_note_given_note(previous_specified_chord[1], chord, 'tenor')[:-1] != bass[:-1]:
                    tenor = self.get_closest_specified_note_given_note(previous_specified_chord[1], chord, 'tenor')
                else:
                    tenor = self.voice.specified_note_given_note(random.choice(leftovers), 'tenor')
                leftovers = [c for c in chord if c != bass[:-1] and c!= soprano[:-1] and c!= tenor[:-1]]
                if len(leftovers) == 0:
                    alto =  self.voice.specified_note_given_note(random.choice(chord), 'alto')
                else:
                    alto = self.voice.specified_note_given_note(random.choice(leftovers), 'alto')
        return tuple(sorted((bass, tenor, alto, soprano), lambda x,y : self.sort_func(x, y)))


    def get_closest_specified_note_given_note(self, specified_note, chord, range_name):
        # print('specified note', specified_note)
        # print(self.voice.specified_chord_given_range_name(chord, range_name))
        min_cost = float('Inf')
        best_note = None
        for potential_note in self.voice.specified_chord_given_range_name(chord, range_name):
            cost = self.cost_function(potential_note, specified_note)
            if cost < min_cost:
                best_note = potential_note
                min_cost = cost
        return best_note


    def harmonize_one_note(self, seed_notes, num_steps):
        # 1 get_specified_chord_from_note_and_chord(no prev chord)
        # 2 get next chord from specified chord
        # 3 get_specified_chord_from_note_and_chord(prev chord)
        # 4 GOTO 2
        assert len(seed_notes) == 1, "you are likely using the wrong function -- you either have more than one seed note, or an empty seed_notes list"

        chords = []

        seed_note = seed_notes[0]
        specified_chord = self.get_specified_chord_from_note_and_chord(seed_note, random.choice(self.key.c_chord_given_c_note(seed_note[:-1])))
        chords.append(specified_chord)
        for s in range(num_steps):
            next_chord = self.get_next_chord(specified_chord)
            next_specified_note = self.get_closest_specified_note_given_note(specified_chord[-1], next_chord, 'soprano')
            specified_chord = self.get_specified_chord_from_note_and_chord(next_specified_note, next_chord, previous_specified_chord=specified_chord)
            chords.append(specified_chord)
        return chords


    def harmonize_melody(self, seed_notes):
        # 1 get_specified_chord_from_note_and_chord(no prev chord)
        # 2 get possible chords from next note
        # 3 sample from possible chords
        # 4 get_specified_chord_from_note_and_chord(prev chord)
        # 5 GOTO2
        assert len(seed_notes) > 1, "you are likely using the wrong function -- you either have more than one seed note, or an empty seed_notes list"

        chords = []

        seed_note = seed_notes[0]
        specified_chord = self.get_specified_chord_from_note_and_chord(seed_note, random.choice(self.key.c_chord_given_c_note(seed_note[:-1])))
        chords.append(specified_chord)
        for s in range(1,len(seed_notes)):
            next_chord = self.get_next_chord_conditional(specified_chord, seed_notes[s])
            # next_specified_note = self.get_closest_specified_note_given_note(specified_chord[-1], next_chord, 'soprano')
            next_specified_note = seed_notes[s]
            specified_chord = self.get_specified_chord_from_note_and_chord(next_specified_note, next_chord, previous_specified_chord=specified_chord)
            chords.append(specified_chord)
        return chords


class Note():
    pass

class SpecifiedNote(Note):
    pass

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


class Voice(object):
    def __init__(self):
        # ranges do not include the top
        self.ranges = {'soprano': ('G4','G5'),
                       'alto': ('C4','C5'),
                       'tenor': ('G3','G4'),
                       'bass': ('G2','G3')}

    # called by the function to enumerate all notes in a a chord for a range
    def specified_note_given_note(self, note, range_name):
        assert range_name in self.ranges.keys()
        if self.ranges[range_name][0][0] != 'C' and any([prefix in note for prefix in ['C','D','E','F']]):
            octave = str(int(self.ranges[range_name][0][-1])+1)
        else:
            octave = self.ranges[range_name][0][-1]
        return note+octave

    def specified_chord_given_range_name(self, chord, range_name):
        specified_chord = []
        for c in chord:
            specified_chord.append(self.specified_note_given_note(c, range_name))
        return tuple(specified_chord)  # do we want to tuple this?


class Chord():
    def __init(self, notes):
        self.notes = notes

class SpecifiedChord(Chord):
    def __init__(self, notes):
        self.notes = notes
        self.is_major = is_major(notes)

    # position: [0, 1, 2]
    def get_chord_intervals(is_major):
        if is_major:
            return ('M3','m3')
        else:
            return ('m3','M3')


# key = Key('D')
# print('keyname', key.keyname)
# print('chromatic', key.chromatic)
# print('intervals', key.intervals)
# print('is_major', key.is_major)
# print('notes', key.notes)
# print('romans', key.romans)
# print('chords', key.chords)
# for i in ['C#', 'D','E','F#','G','A','B']:
#     print('Given',i,key.c_chord_given_c_note(i))



# keyname D
# chromatic ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#']
# intervals ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'T', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']
# is_major True
# notes ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']
# romans ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii0']
# chords [('D', 'F#', 'A'), ('E', 'G', 'B'), ('F#', 'A', 'C#'), ('G', 'B', 'D'), ('A', 'C#', 'E'), ('B', 'D', 'F#'), ('C#', 'E', 'G')]
# Given C# [('F#', 'A', 'C#'), ('A', 'C#', 'E'), ('C#', 'E', 'G')]
# Given D [('D', 'F#', 'A'), ('G', 'B', 'D'), ('B', 'D', 'F#')]
# Given E [('E', 'G', 'B'), ('A', 'C#', 'E'), ('C#', 'E', 'G')]
# Given F# [('D', 'F#', 'A'), ('F#', 'A', 'C#'), ('B', 'D', 'F#')]
# Given G [('E', 'G', 'B'), ('G', 'B', 'D'), ('C#', 'E', 'G')]
# Given A [('D', 'F#', 'A'), ('F#', 'A', 'C#'), ('A', 'C#', 'E')]
# Given B [('E', 'G', 'B'), ('G', 'B', 'D'), ('B', 'D', 'F#')]

# v = Voice()
# for range_name in v.ranges:
#     print('\n')
#     print(range_name)
#     for i in ['C#', 'D','E','F#','G','A','B']:
#         print(i, v.specified_note_given_note(i, range_name))


# m = Music("D", [])
# out = m.get_next_chord_conditional("1", "A")
# print(out)

# m = Music("C")
# print(m.get_specified_chord_from_note_and_chord("F#4", ('D', 'F#', 'A'), previous_specified_chord=None))
# print(m.harmonize_one_note([m.seed_notes[0]+'4'], 1000))
# print(m.harmonize_melody(["A4", "E4", "G4", "B4", "A4", "F4","G4"]))
