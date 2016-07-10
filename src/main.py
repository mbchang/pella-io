"""Main file that processes audio and writes to MIDI.

   Writes MIDI in output folder.
"""

from audio_models import BeatInterval
from construct_midi import construct_midi

def main():
	FILENAME = "output.mid"
	BPM = 120
	TRACKNAME = "Demo"
	# Initialize the MIDI
	# Mocked: beat_intervals
	# Use: beat_intervals = get_beat_intervals(filename)
	lowest_frequency = 261.6255653006
	frequencies = [
		261.6255653006, 329.6275569129,
		391.9954359817, 523.2511306012 
	]
	multiplicity = [1, 1, 1, 1]
	bi = BeatInterval(
		lowest_frequency,
		frequencies,
		multiplicity
	)
	beats = [bi, bi, bi, bi]
	construct_midi(FILENAME, BPM, TRACKNAME, beats)

main()
