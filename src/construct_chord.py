from midi_models import AcappellaMeasure, AcappellaNote

def chord_from_beat(beat_interval):
	BEATS_PER_MEASURE = 4
	parts = []
	for i in range(len(beat_interval.frequencies)):
		freq = beat_interval.frequencies[i]
		mult = beat_interval.multiplicities[i]
		notes = []
		for i in range(mult):
			notes.append(AcappellaNote(freq, int(BEATS_PER_MEASURE/mult)))
		parts.append(notes)
	am = AcappellaMeasure(*parts)
	return am 


