class BeatInterval:
	"""A interval of music separated by beats."""
	def __init__(self, interval):
		self.interval = interval

class Note:
	"""Represents a musical note."""
	def __init__(self, octave, alph, freq):
		self.octave = octave
		self.alph = alph
		self.freq = freq

class Chord:
	"""Represents a processed chord.
		name: "Cm", "C", etc...
		notes: array[Note]

	"""
	def __init__(self, name, notes):
		self.name = name
		self.notes = notes

class ChordalSong:
	"""Represents the list of chords that form a song.
	   Each chord is of the same timelength (one inter-beat interval)
	"""
	def __init__(self, name, )


