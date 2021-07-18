"""
==========================================
 Title:  PyPlayer ThreadManager
 Author: @jaquielajoie
 Date:   17 July 2021
 Liscence: Apache 2.0
==========================================
"""

import concurrent.futures
from pyplayer.midointerface import MidiInterface

class ThreadManager:

    def __init__(self): # *args, **kwargs
        self.interaces = []

    def configure_midi_interfaces(self, midi_config):

        interfaces = []
        for conf in midi_config:
            mi = MidiInterface()
            print(conf[0])
            mi.config_tracks(filepath=conf[0])
            mi.set_nlen(nlen=conf[1])
            """
            Change channel_number to track number to be selected (of midi file)
            """
            # mi.set_tempo(bpm=120)
            # mi.shift_pitch(semitones=0)
            # mi.shift_velocity(vel=0)
            # mi.remix_track(nlen=4, iters=10000)
            interfaces.append(mi)

        return interfaces

    def start(self, midi_config):

        self.interfaces = self.configure_midi_interfaces(midi_config)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # submit starts the function
            midi_io = [executor.submit(interface.remix_track, 1000) for interface in self.interfaces]

    def raise_exception(self):
        pass
