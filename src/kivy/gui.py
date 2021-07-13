"""
==========================================
 Title:  PyPlayer GUI
 Author: @jaquielajoie
 Date:   10 July 2021
 Liscence: Apache 2.0
==========================================
"""
import kivy as kv
from kivy.app import App
from kivy.uix.widget import Widget
from pyplayer.mido_interface import MidiInterface
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
import os


Builder.load_file(os.path.abspath('design/main.kv'))


class AppContainer(Widget):

    def selected(self, filename):
        try:
            print(filename[0].split('/')[:-1])
            self.ids.midifile_label.text = filename[0]

        except Exception as e:
            print(f"Error on select... {e}")

    def reset_press(self):
        self.ids.ngram_slider_out.text = str(1)
        self.ids.ngram_slider_out.font_size = str(1 + 16)

    def start_press(self):
        filepath = self.ids.midifile_label.text
        ngram_len = int(self.ids.ngram_slider_out.text)
        self.mi.config_tracks(filepath=filepath)
        self.mi.set_tempo(bpm=120)
        self.mi.shift_pitch(semitones=0)
        self.mi.shift_velocity(vel=0)
        self.mi.remix_tracks(nlen=4, iters=10000)


    def end_press(self):
        print(self.mi)
        print('End...')

    def slide_ngram(self, *args):
        self.ids.ngram_slider_out.text = str(int(args[1]))
        self.ids.ngram_slider_out.font_size = str(int(args[1]) + 16)

    def __init__(self, **kwargs):
        super(AppContainer, self).__init__(**kwargs)
        self.mi = MidiInterface()


class MarkovApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 0)
        return AppContainer()


if __name__ == "__main__":
    app = MarkovApp().run()
