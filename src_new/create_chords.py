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
