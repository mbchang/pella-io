from midi_models import AcappellaMeasure

def chord_from_beat(beat_interval):
	bass, tenor, alto, soprano = beat_interval.frequencies
	am = AcappellaMeasure(bass, tenor, alto, soprano)
	

