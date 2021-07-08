import os
import mido
import base64
import math
import time
import logging
import threading
from mido import MidiFile
from markov import MarkovPlayer
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

def print_midi(name, track, port):
    logging.info("Thread %s: starting", name)
    for msg in track:
        time.sleep(int((msg.time + name) / 240))# / 480)) #480 is the default ticks per 8th note
        if msg.type != 'unknown_meta':
            print(msg)
            if not msg.is_meta:
                port.send(msg)
        elif hasattr(msg, 'data'):
            print('\nUnknown meta message type: ' + str(msg.type_byte) + '\nmsg data: ' + str(msg.data))
        else:
            print('\nUnknown meta message type: ' + str(msg.type_byte) + '\nNo data associated with unknown meta message')
    logging.info("Thread %s: finishing", name)


class MidiInterface():
    def __init__(self):
        self.port = config_backend()
        self.tracks = None

    def config_tracks(self):
        filepath = input('Enter in the full midi file path: ').rstrip()
        self.tracks = get_tracks(filepath)

    def freeze_messages(self, track):
        frozen = []
        for message in track:
            msg = freeze_message(message)
            frozen.append(msg)
        return frozen

    def play_tracks(self, nlen=None): # nlen not used, just for debugging convience [will delete]
        for i, track in enumerate(midi_interface.tracks):
            print(f"Track {i}: {track.name}")
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
            logging.info('Creating new channel_midi (MidiInterface.play_tracks)')
            channel_midi = threading.Thread(target=print_midi, args=(i, track, midi_interface.port))
            logging.info("play_tracks: before starting thread")
            channel_midi.start()
            logging.info("play_tracks: waiting for the thread to finish")
            logging.info("play_tracks: finised thread")

    def remix_tracks(self, nlen):
        mp = MarkovPlayer(nlen=nlen, note_list=self.freeze_messages(self.tracks[0]))
        mp.run(10000)


if __name__ == "__main__":
    midi_interface = MidiInterface()
    midi_interface.config_tracks()
    midi_interface.play_tracks(nlen=2)
