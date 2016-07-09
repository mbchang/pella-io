BASS_CHANNEL = 0
TENOR_CHANNEL = 1
ALTO_CHANNEL = 2
SOPRANO_CHANNEL = 3

class AcappellaMeasure:
	"""Represents a 4-part measure of an a cappella arrangement."""
	def __init__(self, bass, tenor, alto, soprano):
		self.bass = bass
		self.tenor = tenor
		self.alto = alto
		self.soprano = soprano
