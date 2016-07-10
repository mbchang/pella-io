import midi_library

# Make the backgrounds softer than the solo
CHORD_VELOCITY = 75

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
		track = midi_library.Track(tick_relative=False)
		
		# Set up each track
		def keep_events(event):
			on = isinstance(event, midi_library.NoteOnEvent)
			off = isinstance(event, midi_library.NoteOffEvent)
			end = isinstance(event, midi_library.EndOfTrackEvent)
			result = not (on or off or end)
			return result

		events_to_add = filter(keep_events, pattern[0])
		for event in events_to_add:
			track.append(event)
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
	elif note.style == "FAST":
		on = midi_library.NoteOnEvent(
			tick=ticks_timestamp,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure/4, 
			pitch=note.pitch
		)
		on_2 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + measure/4 + 1,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off_2 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 2*measure/4, 
			pitch=note.pitch
		)
		on_3 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 2*measure/4 + 1,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off_3 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 3*measure/4, 
			pitch=note.pitch
		)
		on_4 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 3*measure/4 + 1,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off_4 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure, 
			pitch=note.pitch
		)
		return [on, off, on_2, off_2, on_3, off_3, on_4, off_4]
	elif note.style == "HALF":
		on = midi_library.NoteOnEvent(
			tick=ticks_timestamp,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure/2, 
			pitch=note.pitch
		)
		on_2 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + measure/2 + 1,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off_2 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure, 
			pitch=note.pitch
		)
		return [on, off, on_2, off_2]
	elif note.style =='SYNCO1':
		on = midi_library.NoteOnEvent(
			tick=ticks_timestamp,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure/4, 
			pitch=note.pitch
		)
		on1 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + measure/4 + 1, 
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off1 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 5*measure/8, 
			pitch=note.pitch
		)
		on2 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 5*measure/8 + 1, 
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off2 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 3*measure/4, 
			pitch=note.pitch
		)
		on3 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 3*measure/4+1, 
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off3 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 7*measure/8, 
			pitch=note.pitch
		)
		on4 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 7*measure/8, 
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off4 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure, 
			pitch=note.pitch
		)
		return [on, off, on1, off1, on2, off2, on3, off3, on4, off4]
	elif note.style =='SYNCO2':
		on = midi_library.NoteOnEvent(
			tick=ticks_timestamp,
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 3*measure/8, 
			pitch=note.pitch
		)
		on1 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 3*measure/8 + 1, 
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off1 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + 3*measure/4, 
			pitch=note.pitch
		)
		on2 = midi_library.NoteOnEvent(
			tick=ticks_timestamp + 3*measure/4 + 1, 
			velocity=CHORD_VELOCITY,
			pitch=note.pitch
		)
		off2 = midi_library.NoteOffEvent(
			tick=ticks_timestamp + measure, 
			pitch=note.pitch
		)
		return [on, off, on1, off1, on2, off2]



def write_midifile(midifile, pattern):
	pattern[0].make_ticks_abs()
	pattern.make_ticks_rel()
	midi_library.write_midifile(midifile, pattern)