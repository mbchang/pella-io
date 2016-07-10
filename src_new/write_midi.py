import midi_library

# Make the backgrounds softer than the solo
CHORD_VELOCITY = 60 

def write_chords_to_pattern(chords, pattern):
	ATTRS = ['low', 'mid', 'high', 'highest']

	TICKS_PER_BEAT = pattern.resolution

	time_sig_event = filter(
		lambda x: isinstance(x, midi_library.TimeSignatureEvent),
		pattern[0]
	)[0]
	time_sig_event.set_denominator(4)
	BEATS_PER_MEASURE = time_sig_event.get_numerator()

	TICKS_PER_MEASURE = TICKS_PER_BEAT * BEATS_PER_MEASURE

	for i in range(len(ATTRS)):
		track = midi_library.Track()
		pattern.append(track)

	for index, chord in enumerate(chords):
		# insert notes by measure
		ticks_timestamp = index * TICKS_PER_MEASURE
		if not chord:
			continue
		for attr_ind, attr in enumerate(ATTRS):
			note = getattr(chord, attr)
			events = get_notes_by_style(
				note, 
				ticks_timestamp,
				pattern, 
				TICKS_PER_MEASURE
			)
			track = pattern[attr_ind + 1]
			for event in events:
				track.append(event)

	for track in pattern[1:]:
		last_tick = TICKS_PER_MEASURE*len(chords) + 1
		eot = midi_library.EndOfTrackEvent(tick=last_tick)
		track.append(eot)

	print pattern
	return pattern


def get_notes_by_style(note, ticks_timestamp, pattern, measure):
	if note.style == "SLOW":
		on = midi_library.NoteOnEvent(
			tick=ticks_timestamp,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure, 
			pitch=note.pitch
		)
		return [on, off]
	else:
		return []


def write_midifile(midifile, pattern):
	midi_library.write_midifile(midifile, pattern)