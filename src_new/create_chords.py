import random

from models import Chord

from harmony import Music

CHORD_RHYTHMS = ["SLOW", "HALF", "FAST", "SYNCO1", "SYNCO2"]

def create_chords(input_notes):
	chords = []
	first_notes = []
	for index, measure in enumerate(input_notes):
		if measure == []:
			# Extend the previous note
			if first_notes != []:
				first_notes.append(first_notes[-1])
			else:
				first_notes.append(60) # placeholder
		else:
			first_notes.append(measure[0])
	print first_notes
	first_letters = [int_to_letter(note) for note in first_notes]
	key = first_letters[0][:-1]

	print first_letters, key 
	m = Music("C")
	harmonies = m.harmonize_melody(first_letters)

	for harmony in harmonies:
		low, mid, high, highest = harmony
		new_chord = Chord(
			MidiStringToInt(low), 
			MidiStringToInt(mid), 
			MidiStringToInt(high), 
			MidiStringToInt(highest)
		)

		rhythm = random.choice(CHORD_RHYTHMS)
		print rhythm

		new_chord.low.style = rhythm
		new_chord.mid.style = rhythm
		new_chord.high.style = rhythm
		new_chord.highest.style = rhythm
		chords.append(new_chord)

	print chords
	print chords[0].low.pitch
	return chords

# http://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python
#Input is string in the form C#4, Db4, or F3. If your implementation doesn't use the hyphen, 
#just replace the line :
#    letter = midstr.split('-')[0].upper()
#with:
#    letter = midstr[:-1]
def MidiStringToInt(midstr):
    Notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
    answer = 0
    i = 0
    #Note
    letter = midstr[:-1]
    for note in Notes:
        for form in note:
            if letter.upper() == form:
                answer = i
                break;
        i += 1
    #Octave
    answer += (int(midstr[-1]))*12
    return answer

def int_to_letter(midi_int):
	int_to_letter_dict = {}
	notes = [["C"],["C#"],["D"],["D#"],["E"],["F"],["F#"],["G"],["G#"],["A"],["A#"],["B"]]
	for i in range(9):
		for note in notes:
			for element in note:
				note_letter = element + str(i)
				note_integer = MidiStringToInt(note_letter)
				int_to_letter_dict[note_integer] = note_letter
	return int_to_letter_dict[midi_int]

