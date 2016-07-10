from midiutil.MidiFile3 import MIDIFile

from construct_chord import chord_from_beat

channel_to_part = {
	"bass": 0,
	"tenor": 1,
	"alto": 2,
	"soprano": 3
}

def construct_midi(filename, bpm, trackname, beat_intervals):
	# Create a MIDI with one track
	MyMIDI = MIDIFile(1)

	track = 0 
	time = 0
	MyMIDI.addTrackName(track, time, trackname) 
	MyMIDI.addTempo(track, time, bpm)

	TIME_COUNTER = 0

	for beat_interval in beat_intervals:
		acappella_measure = chord_from_beat(beat_interval)
		TIME_COUNTER = _add_measure(
			acappella_measure, 
			TIME_COUNTER, 
			MyMIDI
		)

	binfile = open("../output/" + filename, 'wb') 
	MyMIDI.writeFile(binfile) 
	binfile.close()

def _add_measure(acappella_measure, time_counter, my_midi):
	track = 0 
	attrs = ['bass', 'tenor', 'soprano', 'alto']
	for attr in attrs:
		notes = getattr(acappella_measure, attr)
		if not notes:
			print "Warning, not all 4 parts detected"
			continue
		time_offset = time_counter
		for note in notes:
			pitch = note.midi_num
			duration = note.duration
			channel = channel_to_part[attr]
			volume = 100
			my_midi.addNote(track,channel,pitch,time_offset,duration,volume)
			time_offset += duration
	time_counter += 4
	return time_counter

