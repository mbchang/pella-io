from models import Chord

def create_chords(input_notes):
	chords = []
	for measure in input_notes:
		if measure == []:
			chords.append(None)
		else:
			# TODO: complete
			new_chord = Chord(52, 54, 60)
			new_chord.low.style = "SLOW"
			new_chord.mid.style = "SLOW"
			new_chord.high.style = "SLOW"
			new_chord.highest.style = "SLOW"
			chords.append(new_chord)
	return chords
