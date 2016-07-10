import midi_library
from read_midi import read_midi_by_measure
from create_chords import create_chords
from write_midi import write_midifile, write_chords_to_pattern

INPUT_MIDI = 'data/snippet10.mid'
OUTPUT_FILE = 'data/output.mid'

def parse_to_mid(input_file):
	beatIntervals = getBeatIntervals(input_file)
	extension = input_file.split(".")[-1]
	if extension == ".mid":
		return
	pattern = midi_library.Pattern()
	tick = 0
	TICKS_PER_BEAT = pattern.resolution
	BEATS_PER_MIN = 
	track = midi.Track()
	track.make_ticks_abs()
	pattern.append(track)
	for beat in beatIntervals:
		nc = Chord(None, None, None, None)
		pitch = nc.compute_midi_num(beat.frequency)
		duration = 
		on = midi.NoteOnEvent(tick=0, velocity=100, pitch=midi.G_3)



def main(input_midi):
	# Read the input MIDI
	# print midi_library.read_midifile(INPUT_MIDI)
	tick_notes, pattern = read_midi_by_measure(input_midi)
	chords = create_chords(tick_notes)
	write_chords_to_pattern(chords, pattern)
	write_midifile(OUTPUT_FILE, pattern)



main(INPUT_MIDI)