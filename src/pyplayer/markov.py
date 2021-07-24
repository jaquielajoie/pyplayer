"""
==========================================
 Title:  PyPlayer MarkovChain
 Author: @jaquielajoie
 Date:   9 July 2021
 Liscence: Apache 2.0
==========================================
"""
from collections import defaultdict
import random

def make_ngrams(nlen, values):
    # Helper 1: assemble_note_map
    return [values[i:i+nlen+1] for i in range(0,len(values))]

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

def assemble_note_map(nlen, midi_list):
    """
    Takes in a list of midi notes.
    Creates tuple-keys of nlen. Next note is stored as value.
    Removes all tuple-keys less than nlen.
    Creates a dictionary of tuple-keys: list of values.
    """
    return aggregate_patterns(prune_ngrams(ngram_and_next(make_ngrams(nlen, midi_list)), nlen))

def random_key(midi_map):
    return random.choice(list(midi_map.keys()))

def next_value(key, midi_map):
    # Helper 1: cycle_note
    return random.choice(midi_map[key])

def trigger_note(play, interface, keycache, sleepmanager, test=False):
    # Send the midi message
    if test is False:
        interface.play_note(play, keycache)
        sleepmanager.rest(duration=play["duration"])
    return play

def update_value(key, next_value):
    # Helper 3: cycle_note
    l = list(key)
    l.append(next_value)
    updated_key = tuple(l[1:])

    return updated_key

def cycle_note(keys, midi_map, interface, keycache, sleepmanager, test=False):
    """
    Takes a note in as a key.
    Randomly selects a next note from the note_map via said key.
    Triggers the returned value.
    Returns this choice and note_map(s).
    """
    try:
        # triggers_durations_map
        note_play = next_value(keys["note_key"], midi_map["notes_map"])
        trigger_play = next_value(keys["trigger_key"], midi_map["triggers_map"])
        duration_play = next_value(keys["duration_key"], midi_map["durations_map"])
    except KeyError as k:
        note_key = random_key(midi_map["notes_map"])
        trigger_key = random_key(midi_map["triggers_map"])
        duration_key = random_key(midi_map["durations_map"])

        keys = {"note_key": note_key, "trigger_key": trigger_key, "duration_key": duration_key}
        return keys, midi_map

    play = {"note": note_play, "trigger": trigger_play, "duration": duration_play}

    try:
        trigger_note(play, interface, keycache, sleepmanager, test)

    except Exception as e:
        print(e)
        quit()

    note_key = update_value(keys["note_key"], note_play)
    trigger_key = update_value(keys["trigger_key"], trigger_play)
    duration_key = update_value(keys["duration_key"], duration_play)

    keys = {"note_key": note_key, "trigger_key": trigger_key, "duration_key": duration_key}

    return keys, midi_map


class MarkovPlayer():
    def __init__(self, nlen, midi_list, interface=None, test=False):
        self.nlen = nlen

        notes_map = assemble_note_map(nlen, midi_list["notes"])
        triggers_map = assemble_note_map(nlen, midi_list["triggers"]) # Need to tie duration & trigger into one map
        durations_map = assemble_note_map(nlen, midi_list["durations"])

        self.midi_map = {
            "notes_map": notes_map,
            "triggers_map": triggers_map,
            "durations_map": durations_map
        }
    	# add the note triggering interface
        self.interface = interface
        self.test = test
        self.is_playing = False

    def run(self, iters, keycache, sleepmanager):
        """
        interface:
            ticks per beat based on BPM

        Keycache:
            pressed notes
                elasped time from press
            track running time
            track measures

        Current bugs:
            Running through iterations too quickly
                Handle time.sleep(N) more gracefully
                Quantize this to BPM or ticks
            Add debugging tool to CMD line/GUI (key press)

        Minimum sleep times:
            note_off    10 or 0 (if elapsed time for note > 10)
            note_on     0

        Handling Notes:
            track note, time_pressed, polyphony
            if note_on
                handle_note_on
                    add note, duration
            if note_off
                handle_note_off
                    remove either
                        note value (if currently pressed)
                        OR longest elasped note value
                            THEN handle_note_on
            if exceeds polyphony
                handle_note_off
        """
        midi_map = self.midi_map
        note_key = random_key(self.midi_map["notes_map"])
        trigger_key = random_key(self.midi_map["triggers_map"])
        duration_key = random_key(self.midi_map["durations_map"])
        self.is_playing = True

        keys = {"note_key": note_key, "trigger_key": trigger_key, "duration_key": duration_key}

        for i in range(0, iters):
            if self.is_playing:
                keys, midi_map = cycle_note(keys, midi_map, self.interface, keycache, sleepmanager, self.test)

    def stop(self):
        # signal is sent from GUI > MidiInterface > mp.iters
        self.is_playing = False

if __name__ == "__main__":
    nlen = 2
    note_list = [1,2,3,4,5,6,7,8,9,8,7,6,7,8,7,6,5,4,5,6,7,6,5,4,8,6,6,4,2,1,2,3,54,7,8,431,2,678,7,5,23,1] # replace with mido notes...
    mp = MarkovPlayer(nlen=nlen, note_list=note_list, interface=None)
    mp.run(100000)
