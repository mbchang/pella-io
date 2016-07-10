"""Main file that processes audio and writes to MIDI.

   Writes MIDI in output folder.
"""

from audio_models import BeatInterval
from construct_midi import construct_midi
from audio_file_converter import getTwinkle

def main():
	FILENAME = "output.mid"
	BPM = 120
	TRACKNAME = "Demo"
	# Initialize the MIDI
	# Mocked: beat_intervals
	# Use: beat_intervals = get_beat_intervals(filename)

	#beats = [bi, bi, bi, bi, bi]
	beatIntervals = getTwinkle()

	construct_midi_from_chords(FILENAME, BPM, TRACKNAME, chords)

main()
