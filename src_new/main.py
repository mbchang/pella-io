import midi_library
from read_midi import read_midi_by_measure
from create_chords import create_chords
from write_midi import write_midifile, write_chords_to_pattern

INPUT_MIDI = 'data/snippet2.mid'
OUTPUT_FILE = 'data/output.mid'


def main(input_midi):
	# Read the input MIDI
	tick_notes, pattern = read_midi_by_measure(input_midi)
	chords = create_chords(tick_notes)
	write_chords_to_pattern(chords, pattern)
	write_midifile(OUTPUT_FILE, pattern)


main(INPUT_MIDI)