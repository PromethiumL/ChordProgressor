# Chord Progressor
> NOTE: WIP refactorization: 
> - README is not updated yet.
> - Chord symbol parser needs to be replaced with an external one.
> - Chord voicing expansion algorithm needs to be improved.
> - Unused functions aren't fully removed yet.

A simple musical program to connect the chords, and play the progression instantly.

## Requirements

It's a python program, and the module `pygame` is required so that you can hear the chords played. 

## Usage

Demo:

```bash
pip install -r requirements.txt  # pygame
python progressor.py   # play the giant steps progression
```

The basic class in the module `music`is `Note`. Then comes the `Chord`.
Here are some functions you can use easily.

```python

import music
import playsound as ps

n = music.Note('C')	# Create a note by name, the default octave is '4'
n2 = music.Note(39)	# You can also give the octave, or it's index:
n3 = music.Note('Eb', octave=2) 
			# But avoid setting the 'name' and 'index' at the same time
n.show_info()		# Print note1's information

ps.play(note1, duration=2)	# Play it

n.increment()			# Make it one semitone higher
n.increment(7)		# Make it a perfect fifth higher
n.decrement()			# One semitone Lower
n.decrement(7)		# P5 lower
n.move_by_one_octave_upward()			# 8va
n.move_by_one_octave_downward()		# 8vb
n.show_info()		# Show the details again

# Chords

c = music.Chord('C^9') 	# Create a chord by name
c2 = music.Chord('Db^7')	# Another one

c2.connect_to(c)		# Connect 'c2' to 'c' , in order to make the progression smooth

# Play


# Use the function 'play()' in the module 'playsound' to play the notes or chords.

ps.play(n) 			# Directly play it until the sound files stop
ps.play([n] * 3, duration=1)	# Set each note's duration to 1 second.

ps.play(c)			# Play the chord
ps.play(c, interval=0.07)	# Set the interval between notes to 0.07s, like 'arpeggio'
ps.play([c, c2], interval=0.1, duration=1) # Play the chords. 1s for each chord.

```

You can add your own chord types in the file 'music.py', just by giving the interval (note  interval) in the dict.

## Known issues

There are also some unexpected problems when connecting the chords. Improving the algorithm.
