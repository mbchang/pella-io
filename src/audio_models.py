from midi_freq import midi_num_to_freq

class BeatInterval:
	"""A interval of music separated by beats."""
	def __init__(self, lowest, frequencies, multiplicities):
		self.lowest_frequency = lowest
		self.frequencies = frequencies
		self.multiplicities = multiplicities


class Chord:
	"""A 3-note chord to be played."""
	def __init__(self, low, mid, high):
		self.low = low
		self.mid = mid 
		self.high = high
		self.highest = self.compute_octave()

	def compute_octave(self):
		# Create the soprano note
		low_freq = midi_num_to_freq[midi_num]
		oct_freq = low_freq * 2
		oct_midi_num = compute_midi_num(oct_freq)
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