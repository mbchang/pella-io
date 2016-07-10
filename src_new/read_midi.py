import midi_library

def read_midi_by_measure(input_filename):
	pattern = midi_library.read_midifile(input_filename)
	if len(pattern) == 2:
		# Merge the tracks - sometimes, the input MIDI has two tracks
		del pattern[0][-1]  # remove the EndOfTrackEvent
		for event in pattern[1]:
			pattern[0].append(event)
		del pattern[1]
	pattern.make_ticks_abs()
	track = pattern[0]
	
	time_sig_event = filter(
		lambda x: isinstance(x, midi_library.TimeSignatureEvent),
		track
	)[0]
	time_sig_event.set_denominator(4)

	BEATS_PER_MEASURE = time_sig_event.get_numerator()
	TEMPO = filter(
		lambda x: isinstance(x, midi_library.SetTempoEvent),
		track
	)[0].get_bpm()

	TICKS_PER_MEASURE = BEATS_PER_MEASURE * pattern.resolution

	END_TICK = track[-1].tick

	tick_notes = [[] for i in range(END_TICK/TICKS_PER_MEASURE + 1)]
	for event in track:
		if isinstance(event, midi_library.NoteEvent):
			index = event.tick/TICKS_PER_MEASURE
			if event.data[1] != 0: # if volume is nonzero
				note_value = event.data[0] # pitch
			tick_notes[index].append(note_value)

	return tick_notes, pattern