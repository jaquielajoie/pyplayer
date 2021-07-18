"""
==========================================
 Title:  PyPlayer SleepManager
 Author: @jaquielajoie
 Date:   17 July 2021
 Liscence: Apache 2.0
==========================================
"""

import time

"""
SleepManager is a child of MarkovPlayer
This class quantizes sleep times according to BPM   
"""

class SleepManager:

    def __init__(self, bpm):
        self.bpm = bpm

    def rest(self, duration):
        time.sleep(duration / 480)
