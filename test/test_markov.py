"""
==========================================
 Title:  PyPlayer TestMarkov
 Author: @jaquielajoie
 Date:   9 July 2021
 Liscence: Apache 2.0
==========================================
"""

import unittest
import pyplayer.markov as mk


class TestMarkov(unittest.TestCase):
    # def assemble_note_map(nlen, midi_notes):
    def test_assemble_note_map(self):
        nlen = 2
        note_list = [1,2,3,4,5,6,7,8,6,5,4,2,3,4,1]
        comparison = {
                        (1, 2): [3],
                        (2, 3): [4, 4],
                        (3, 4): [5, 1],
                        (4, 5): [6],
                        (5, 6): [7],
                        (6, 7): [8],
                        (7, 8): [6],
                        (8, 6): [5],
                        (6, 5): [4],
                        (5, 4): [2],
                        (4, 2): [3]
                    }

        result = mk.assemble_note_map(nlen, note_list)
        self.assertEqual(result, comparison)

    # def cycle_note(note_key, note_map, midi_port):
    def test_cycle_note(self):
        nlen = 2
        note_list = [1,2,3,4,5,6,7,8,6,5,4,2,3,4,1]

        note_key = (1,2)
        note_map = mk.assemble_note_map(nlen, note_list)
        midi_port = 'IAC Driver Bus 1'

        note_key, note_map = mk.cycle_note(note_key, note_map, midi_port, test=True)
        self.assertEqual(note_key, (2,3))

    # class MarkovPlayer():
    #    def run(self, iters):
    def test_markov_player_run(self):
        try:
            nlen = 2
            note_list = [1,2,3,4,5,6,7,8,9,8,7,6,7,8,7,6,5,4,5,6,7,6,5,4,8,6,6,4,2,1,2,3,54,7,8,431,2,678,7,5,23,1] # replace with mido notes...
            midi_port = 'IAC Driver Bus 1'

            mp = mk.MarkovPlayer(nlen=nlen, note_list=note_list, interface=None, test=True)
            mp.run(1000)
            assert True
        except Exception as e:
            print(e)
            assert False
