# Create mapping from midi number (int) to frequency (float)
import re

infile = open('data/midi_freq_num.txt')

midi_num_to_freq = {}
infile.readline() # Skip Source attribute
for line in infile:
	if line != '':
		components = filter(lambda ele: ele != "", line.strip().split(' '))
		components = filter(
			lambda ele: not re.search('[a-zA-Z]', ele),
			components
		)
		i = 0
		while i < len(components):
			midi_int = int(components[i])
			midi_freq = float(components[i + 1])
			i += 2
			midi_num_to_freq[midi_int] = midi_freq



