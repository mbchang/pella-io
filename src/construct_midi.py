from midiutil.MidiFile3 import MIDIFile

# Options
FILENAME = 'output.mid'
BPM = 120
TRACKNAME = "Demo"

# Create a MIDI with one track
MyMIDI = MIDIFile(1)

track = 0 
time = 0
MyMIDI.addTrackName(track, time, TRACKNAME) 
MyMIDI.addTempo(track, time, BPM)

TIME_COUNTER = 0

def add_measure(notes, time_counter):
	channel = 0
	for note in notes:
		track = 0 
		pitch = note
		time_offset = time_counter
		duration = 4 
		volume = 100
		MyMIDI.addNote(track,channel,pitch,time_offset,duration,volume)
		channel += 1
	time_counter += 4
	print time_counter
	return time_counter

TIME_COUNTER = add_measure([60, 64, 67, 72], TIME_COUNTER)
TIME_COUNTER = add_measure([60, 64, 67, 72], TIME_COUNTER)
TIME_COUNTER = add_measure([60, 64, 67, 72], TIME_COUNTER)

binfile = open("../output/" + FILENAME, 'wb') 
MyMIDI.writeFile(binfile) 
binfile.close()
