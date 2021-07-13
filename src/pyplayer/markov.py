"""
==========================================
 Title:  PyPlayer Markov Chain
 Author: @jaquielajoie
 Date:   9 July 2021
 Liscence: Apache 2.0
==========================================
"""

from collections import defaultdict
import random
import time

def make_ngrams(nlen, notes):
    # Helper 1: assemble_note_map
    return [notes[i:i+nlen+1] for i in range(0,len(notes))]

def ngram_and_next(ngrams):
    # Helper 2: assemble_note_map
    g = []
    for ngram in ngrams:
        next_note = ngram.pop()
        g.append((tuple(ngram), next_note))
    return g

def prune_ngrams(ngrams, nlen):
    # Helper 3: assemble_note_map
    g = []
    for i, ngram in enumerate(ngrams):
        if len(ngram[0]) == nlen:
            g.append(ngrams[i])
    return g

def aggregate_patterns(ngrams):
    # Helper 4: assemble_note_map
    d = {}
    for ngram in ngrams:
        d.setdefault(ngram[0], [])
        d[ngram[0]].append(ngram[1])
    return d

def assemble_note_map(nlen, note_list):
    """
    Takes in a list of midi notes.
    Creates tuple-keys of nlen. Next note is stored as value.
    Removes all tuple-keys less than nlen.
    Creates a dictionary of tuple-keys: list of values.
    """
    return aggregate_patterns(prune_ngrams(ngram_and_next(make_ngrams(nlen, note_list)), nlen))

def random_key(note_map):
    return random.choice(list(note_map.keys()))

def next_note(note_key, note_map):
    # Helper 1: cycle_note
    return random.choice(note_map[note_key])

def trigger_note(play, interface, test=False):
    # Helper 2: cycle_note
    # Uses MIDO to trigger notes on the midi bus.
    if test is False:
        interface.play_note(play)
    return play

def update_note(note_key, next_note):
    # Helper 3: cycle_note
    l = list(note_key)
    l.append(next_note)
    return tuple(l[1:])

def cycle_note(note_key, note_map, midi_port, test=False):
    """
    Takes a note in as a key.
    Randomly selects a next note from the note_map via said key.
    Triggers the returned value.
    Returns this choice and note_map(s).
    """
    try:
        play = next_note(note_key, note_map)
    except KeyError as k:
        note_key = random_key(note_map)
        return note_key, note_map

    played = trigger_note(play, midi_port, test) # send to midi, incorporate timing, pitch, velocity notemaps
    note_key = update_note(note_key, played)
    return note_key, note_map


class MarkovPlayer():
    def __init__(self, nlen, note_list, interface=None, test=False):
        self.nlen = nlen
        self.note_list = note_list
        self.note_map = assemble_note_map(nlen, note_list)
    	# add the note triggering interface
        self.interface = interface
        self.test = test

    def run(self, iters):
        note_map = self.note_map
        note_key = random_key(self.note_map)
        for i in range(0, iters):
            note_key, note_map = cycle_note(note_key, note_map, self.interface, self.test)


if __name__ == "__main__":
    nlen = 2
    note_list = [1,2,3,4,5,6,7,8,9,8,7,6,7,8,7,6,5,4,5,6,7,6,5,4,8,6,6,4,2,1,2,3,54,7,8,431,2,678,7,5,23,1] # replace with mido notes...
    mp = MarkovPlayer(nlen=nlen, note_list=note_list, interface=None)
    mp.run(100000)
