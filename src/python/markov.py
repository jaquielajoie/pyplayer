from collections import defaultdict
import random

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

def assemble_note_map(nlen, midi_notes):
    """
    Takes in a list of midi notes.
    Creates tuple-keys of nlen. Next note is stored as value.
    Removes all tuple-keys less than nlen.
    Creates a dictionary of tuple-keys: list of values.
    """
    return aggregate_patterns(prune_ngrams(ngram_and_next(make_ngrams(nlen, midi_notes)), nlen))

def random_key(note_map):
    return random.choice(note_map.keys())

def next_note(note_key, note_map):
    # Helper 1: cycle_note
    return random.choice(note_map[note_key])

def trigger_note(play):
    # Helper 2: cycle_note
    # Uses MIDO to trigger notes on the midi bus.
    print(play)
    return play

def update_note(note_key, next_note):
    # Helper 3: cycle_note
    l = list(note_key)
    l.append(next_note)
    return tuple(l[1:])

def cycle_note(note_key, note_map):
    """
    Takes a note in as a key.
    Randomly selects a next note from the note_map via said key.
    Triggers the returned value.
    Returns this choice and note_map(s).
    """
    try:
        play = next_note(note_key, note_map)
    except KeyError as k:
        # Fetch random key, return
	note_key = random_key(note_map)	
	return note_key, note_map
    
    played = trigger_note(play) # send to midi, incorporate timing, pitch, velocity notemaps
    note_key = update_note(note_key, played)
    return note_key, note_map

if __name__ == "__main__":
    nlen = 2
    note_list = [1,2,3,4,5,4,3,2,3,4,4,3,2,2,2,3,1,2,3,5,1,3,2,1] # replace with mido notes...
    note_map = assemble_note_map(nlen, note_list)
    note_key = random_key(note_map)

    for i in range(0, 1000000):
        note_key, note_map = cycle_note(note_key, note_map)
