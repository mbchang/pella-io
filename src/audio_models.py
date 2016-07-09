class BeatInterval:
	"""A interval of music separated by beats."""
	def __init__(self, lowest, frequencies, multiplicities):
		self.lowest_frequency = lowest
		self.frequencies = frequencies
		self.multiplicities = multiplicities