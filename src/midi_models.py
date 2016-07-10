from midi_freq import midi_num_to_freq

BASS_CHANNEL = 0
TENOR_CHANNEL = 1
ALTO_CHANNEL = 2
SOPRANO_CHANNEL = 3

class AcappellaMeasure:
	"""Represents a 4-part measure of an a cappella arrangement.
	   All attributes are lists of AcappellaNotes
	"""
	def __init__(self, bass, tenor, alto, soprano):
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
		for midi_num in midi_num_to_freq:
			if midi_num_to_freq[midi_num] == self.freq:
				self.midi_num = midi_num




