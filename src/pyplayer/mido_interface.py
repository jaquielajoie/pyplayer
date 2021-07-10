"""
==========================================
 Title:  PyPlayer MidiInterface
 Author: @jaquielajoie
 Date:   9 July 2021
 Liscence: Apache 2.0
==========================================
"""

import os
import mido
import base64
import math
import time
import logging
import threading
from mido import MidiFile
from pyplayer.markov import MarkovPlayer
from mido import bpm2tempo
from mido.frozen import freeze_message

def config_backend(port_string='IAC Driver Bus 1'):
    mido.set_backend('mido.backends.rtmidi')
    port = mido.open_output(port_string)
    return port

def config_hyperparams():
    pass

def get_tracks(filepath):
    midi = MidiFile(filepath)
    return midi.tracks

def log(name, track, interface):
    logging.info("Thread %s: starting", name)
    for msg in track:
        time.sleep(int((msg.time + name) / 240))# / 480)) #480 is the default ticks per 8th note
        if msg.type != 'unknown_meta':
            print(msg)
            if not msg.is_meta:
                interface.port.play_note(msg)
        elif hasattr(msg, 'data'):
            print('\nUnknown meta message type: ' + str(msg.type_byte) + '\nmsg data: ' + str(msg.data))
        else:
            print('\nUnknown meta message type: ' + str(msg.type_byte) + '\nNo data associated with unknown meta message')
    logging.info("Thread %s: finishing", name)


class MidiInterface():
    def __init__(self):
        self.port = config_backend()
        self.tracks = None
        self.bpm = 120
        self.bpm_scale = 4
        self.semitones = 0
        self.vel = 0

    def config_tracks(self):
        filepath = input('Enter in the full midi file path: ').rstrip()
        self.tracks = get_tracks(filepath)

    def set_tempo(self, bpm):
        self.bpm = bpm

    def shift_pitch(self, semitones):
        self.semitones = semitones

    def shift_velocity(self, vel):
        self.vel = vel

    def freeze_messages(self, track):
        frozen = []
        for m in track:
            if m.type in ['note_on', 'note_off']:
                m.velocity = abs(m.velocity + self.vel) % 127 # add floor
                m.note = abs(m.note + self.semitones) % 127 # maybe this should be handled better...
                msg = freeze_message(m)
                frozen.append(msg)
        return frozen

    def play_note(self, msg):
        if msg.is_meta:
            return

        sleep = int(msg.time * self.bpm_scale // self.bpm )
        time.sleep(sleep)
        self.port.send(msg)

        print(msg)

        return msg

    def play_tracks(self, nlen=None): # nlen not used, just for debugging convience [will delete]
        for i, track in enumerate(midi_interface.tracks):
            print(f"Track {i}: {track.name}")
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
            logging.info('Creating new channel_midi (MidiInterface.play_tracks)')
            channel_midi = threading.Thread(target=log, args=(i, track, midi_interface.port))
            logging.info("play_tracks: before starting thread")
            channel_midi.start()
            logging.info("play_tracks: waiting for the thread to finish")
            logging.info("play_tracks: finised thread")

    def remix_tracks(self, nlen, iters):
        mp = MarkovPlayer(nlen=nlen, note_list=self.freeze_messages(self.tracks[0]), interface=self)
        mp.run(iters)

if __name__ == "__main__":
    midi_interface = MidiInterface()
    midi_interface.config_tracks()
    midi_interface.remix_tracks(nlen=4)
