from midi_freq import midi_num_to_freq

BASS_CHANNEL = 0
TENOR_CHANNEL = 1
ALTO_CHANNEL = 2
SOPRANO_CHANNEL = 3

class AcappellaMeasure:
	"""Represents a 4-part measure of an a cappella arrangement.
	   All attributes are lists of AcappellaNotes
	"""
	def __init__(self, bass=None, tenor=None, alto=None, soprano=None):
		self.bass = bass
		self.tenor = tenor
		self.alto = alto
		self.soprano = soprano

class AcappellaNote:
	"""Represents a single MIDI note."""
	def __init__(self, freq, duration):
		self.freq = freq
		self.midi_num = None
		self.compute_midi_num()
		self.duration = duration

	def compute_midi_num(self):
		closest_note = None
		distance_to_note = None
		for midi_num in midi_num_to_freq:
			distance_to_this_note = abs(self.freq - midi_num_to_freq[midi_num])
			if not closest_note:
				closest_note = midi_num
				distance_to_note = distance_to_this_note
			elif distance_to_this_note < distance_to_note:
				closest_note = midi_num
				distance_to_note = distance_to_this_note
		self.midi_num = closest_note




