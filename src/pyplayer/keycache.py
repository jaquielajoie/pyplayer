"""
==========================================
 Title:  PyPlayer KeyCache
 Author: @jaquielajoie
 Date:   12 July 2021
 Liscence: Apache 2.0
==========================================

This class limits the number of keys pressed simultaneously
    and fixes on/off sequencing errors.

Class limits the total number of pressed notes at one time

Also determines what channel will receive notes
"""
import mido

class KeyCache:

    def __init__(self, port, polyphony, channel_number):
        self.polyphony = polyphony
        self.port = port
        self.activated_notes = [] # i.e. 55, 64, 38
        self.channel_number = channel_number

    def process(self, msg):
        print(f'activated_notes: {self.activated_notes}')
        if msg.type == 'note_off':

            if msg.note in self.activated_notes:
                # remove from activated_notes
                self.activated_notes.remove(msg.note) # -1 len
                self.trigger_note(msg) # sends a note_off

            else:
                conv_msg = self.convert_note(msg)
                self.activated_notes.append(conv_msg.note) # +1 len
                self.trigger_note(conv_msg) # sends a note_on

        if msg.type == 'note_on':
            self.activated_notes.append(msg.note) # +1 len
            self.trigger_note(msg) # sends a note_on

        """
        FIFO pop of notes if polyphony limit reached
        """
        if len(self.activated_notes) > self.polyphony:
            off_tone = self.activated_notes.pop(0)
            # trigger instantly, time=0
            off_msg = self.tone_to_msg(trigger='note_off', tone=off_tone, time=0)
            self.trigger_note(msg=off_msg)

    def convert_note(self, msg):
        # turn a note_off into a note_on
        print(f'convert_note: {self.channel_number}')

        conv_msg = mido.Message('note_on', channel=self.channel_number, note=msg.note, time=msg.time)
        return conv_msg

    def tone_to_msg(self, trigger, tone, time):
        print(f'tone_to_msg: {self.channel_number}')
        off_msg = mido.Message(trigger, channel=self.channel_number, note=tone, time=time)
        return off_msg

    def trigger_note(self, msg):
        self.port.send(msg)
        print(msg)

    def nuke(self):
        for tone in range(1, 128):
            off_note = self.tone_to_msg('note_off', tone=tone, time=0)
            self.trigger_note(msg=off_note)
