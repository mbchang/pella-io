from midiutil.MidiFile3 import MIDIFile

def read_input_information():
	pass


def construct_midi(filename, bpm, trackname, notes):
	# Create a MIDI with one track
	MyMIDI = MIDIFile(1)

	track = 0 
	time = 0
	MyMIDI.addTrackName(track, time, trackname) 
	MyMIDI.addTempo(track, time, bpm)

	TIME_COUNTER = 0

	binfile = open("../output/" + filename, 'wb') 
	MyMIDI.writeFile(binfile) 
	binfile.close()

def _add_measure(notes_for_measure, time_counter, my_midi):
	channel = 0
	for note in notes:
		track = 0 
		pitch = note
		time_offset = time_counter
		duration = 4 
		volume = 100
		my_midi.addNote(track,channel,pitch,time_offset,duration,volume)
		channel += 1
	time_counter += 4
	return time_counter


