from models import Chord

def create_chords(input_notes):
	chords = []
	for index, measure in enumerate(input_notes):
		if measure == []:
			chords.append(None)
		else:
			# TODO: complete
			if index % 2 == 0:
				new_chord = Chord(48, 60, 64, 67)
				new_chord.low.style = "SLOW"
				new_chord.mid.style = "SLOW"
				new_chord.high.style = "SLOW"
				new_chord.highest.style = "SLOW"
				chords.append(new_chord)
			else:
				new_chord = Chord(55, 67, 71, 74)
				new_chord.low.style = "SLOW"
				new_chord.mid.style = "SLOW"
				new_chord.high.style = "SLOW"
				new_chord.highest.style = "FAST"
				chords.append(new_chord)				
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