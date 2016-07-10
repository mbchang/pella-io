from midi_freq import midi_num_to_freq

STYLES = ["JAZZ", "FAST", "SLOW", "STRUM"]

class Note:
	"""A pitch along with its syncopation within the measure."""
	def __init__(self, pitch, style=None):
		self.pitch = pitch
		self.style = style

class Chord:
	"""A 4-note chord to be played."""
	def __init__(self, low, mid, high, highest):
		self.low = Note(low, None)
		self.mid = Note(mid, None)
		self.high = Note(high, None)
		self.highest = Note(highest, None)

	def compute_octave(self):
		# Create the soprano note -- deprecated
		low_freq = midi_num_to_freq[self.low.pitch]
		oct_freq = low_freq * 2
		oct_midi_num = self.compute_midi_num(oct_freq)
		return oct_midi_num

	def compute_midi_num(self, freq):
		closest_note = None
		distance_to_note = None
		for midi_num in midi_num_to_freq:
			distance_to_this_note = abs(freq - midi_num_to_freq[midi_num])
			if not closest_note:
				closest_note = midi_num
				distance_to_note = distance_to_this_note
			elif distance_to_this_note < distance_to_note:
				closest_note = midi_num
				distance_to_note = distance_to_this_note
		return closest_note

	def set_style(note, style):
		assert style in STYLES
		note.style = style

class BeatInterval:
	"""A interval of music separated by beats."""
	def __init__(self, frequency, duration)
		self.frequency = frequency  # float()
		self.duration = duration  # ms