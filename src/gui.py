"""
==========================================
 Title:  PyPlayer GUI
 Author: @jaquielajoie
 Date:   23 July 2021
 Liscence: Apache 2.0
==========================================
"""
import kivy as kv
from kivy.app import App
from kivy.uix.widget import Widget
from pyplayer.threadmanager import ThreadManager
from pyplayer.threadmanager import ThreadManager
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from pyplayer.midointerface import MidiInterface
import threading
import os

Builder.load_file(os.path.abspath('kivy/design/main.kv'))

# returns a list of MidiInterface(s) based on configuration given
def configure_midi_interfaces(midi_config):

    interfaces = []
    iters = 0

    for conf in midi_config:
        mi = MidiInterface()
        mi.config_tracks(filepath=conf["filepath"])
        mi.set_nlen(nlen=conf["ngram_len"])
        mi.set_tempo(bpm=conf["bpm"])
        mi.shift_velocity(vel=conf["velocity_shift"])
        mi.shift_pitch(semitones=conf["pitch_shift"])
        iters = conf["iters"]

        """
        Change channel_number to track number to be selected (of midi file)
        """
        # mi.set_tempo(bpm=120)
        # mi.shift_pitch(semitones=0)
        # mi.shift_velocity(vel=0)
        # mi.remix_track(nlen=4, iters=10000)
        interfaces.append(mi)

    return interfaces, iters

# main kivy app
class AppContainer(Widget):

    def selected(self, filename):

        try:
            print(filename[0].split('/')[:-1])
            self.ids.midifile_label.text = filename[0]
            self.ids.midifile_label.color = (0, 1, 0, 0.65)


        except Exception as e:
            self.ids.midifile_label.text = "No file selected, cannot start!"
            print(f"Error on select... {e}")

    def slide_velocity(self, *args):

        font_size = int(args[1]) / 2
        color_intensity = abs(int(args[1]) / 100)

        if int(args[1]) > 0:
            color = (0, 0.65 + color_intensity, 0, 0.76 + color_intensity)
        elif int(args[1]) < 0:
            color = (0.65 + color_intensity, 0, 0, 0.76 + color_intensity)
        else:
            color = (0.65, 0.65, 0.65, 0.85 + color_intensity)

        self.ids.velocity_slider_out.text = str(int(args[1]))
        self.ids.velocity_slider_out.font_size = str(abs(font_size) + 16)
        self.ids.velocity_slider_out.color = color

    def slide_bpm(self, *args):

        font_size = int(args[1]) / 20

        color_intensity = int(args[1]) / 1000
        color = (0.65 + color_intensity, 0.65 + color_intensity, \
            0.65 + color_intensity, 0.76 + color_intensity)

        self.ids.bpm_slider_out.text = str(int(args[1]))
        self.ids.bpm_slider_out.font_size = str(font_size + 16)
        self.ids.bpm_slider_out.color = color

    def slide_ngram(self, *args):

        font_size = int(args[1])
        color_intensity = int(args[1]) / 100

        color = (0.65 + color_intensity, 0.65 + color_intensity, \
            0.65 + color_intensity, 0.84 + color_intensity)

        self.ids.ngram_slider_out.text = str(int(args[1]))
        self.ids.ngram_slider_out.font_size = str(font_size + 16)
        self.ids.ngram_slider_out.color = color


    def slide_pitch(self, *args):

        font_size = int(args[1])
        color_intensity = abs(int(args[1]) / 100)

        if int(args[1]) > 0:
            color = (0, 0.65 + color_intensity, 0, 0.85 + color_intensity)
        elif int(args[1]) < 0:
            color = (0.65 + color_intensity, 0, 0, 0.85 + color_intensity)
        else:
            color = (0.65, 0.65, 0.65, 0.85 + color_intensity)

        self.ids.pitch_slider_out.text = str(int(args[1]))
        self.ids.pitch_slider_out.font_size = str(abs(font_size) + 16)
        self.ids.pitch_slider_out.color = color

    def validate_int(self):

        raw = self.ids.iters_input.text

        try:
            val = int(raw)

            if isinstance(val, int) and val > 0:
                self.ids.iters_valid_label.text = f'Program will generate {str(val)} note(s).'
                self.ids.iters_valid_label.color = (0, 1, 0, 0.65)
                self.iters = val

            else:
                self.ids.iters_valid_label.text = f'Invalid Iteration #: {str(val)}'
                self.ids.iters_valid_label.color = (1, 0, 0, 0.65)

        except ValueError as v:
            self.ids.iters_valid_label.text = str(v)
            self.ids.iters_valid_label.color = (1, 0, 0, 0.65)
            print(v)

    def start_press(self):

        if self.ids.midifile_label.text != "No file selected, cannot start!":

            filepath = self.ids.midifile_label.text
            ngram_len = int(self.ids.ngram_slider_out.text)
            pitch_shift = int(self.ids.pitch_slider_out.text)
            velocity_shift = int(self.ids.velocity_slider_out.text)
            bpm = int(self.ids.bpm_slider_out.text)
            iters = int(self.iters)

            try:
                raw = self.ids.iters_input.text
                iters = int(raw)

                """
                Test input
                """
                conf = {
                    "filepath": filepath,
                    "ngram_len": ngram_len,
                    "pitch_shift": pitch_shift,
                    "velocity_shift": velocity_shift,
                    "bpm": bpm,
                    "iters": iters
                }

                midi_config = [conf] # channel number

                """
                Replacing ThreadManager
                """
                self.interfaces, iters = configure_midi_interfaces(midi_config)

                for interface in self.interfaces:
                    threading.Thread(target=interface.remix_track, kwargs={"iters": iters}).start()

            except ValueError as v:
                print(v)
                quit()
        else:
            print(f"You need to select a file!")


    def end_press(self):
        pass
        # self.mi.stop_playing()

    def __init__(self, **kwargs):
        super(AppContainer, self).__init__(**kwargs)

        self.iters = 1
        # self.threadmanager = ThreadManager()
        self.interfaces = []
        # self.mi = MidiInterface() # replace this with ThreadManager


class MarkovApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 0)
        return AppContainer()


if __name__ == "__main__":
    app = MarkovApp().run()
