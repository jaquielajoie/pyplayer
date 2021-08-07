"""
==========================================
 Title:  PyPlayer GUI
 Author: @jaquielajoie
 Date:   23 July 2021
 Liscence: Apache 2.0
==========================================
"""
import kivy as kv
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.toast import toast
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.screenmanager import ScreenManager, Screen
from pyplayer.midointerface import MidiInterface
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
import threading
import os

# class ScreenManagement(ScreenManager):
#     pass

# expansion list content
class VelocityListItem(BoxLayout):
    '''Custom content.'''

# returns a list of MidiInterface(s) based on configuration given
def configure_midi_interfaces(midi_config, nlen, pitch_shift, velocity_shift):

    interfaces = []
    for channel, conf in midi_config.items():
        try:
            mi = MidiInterface()

            mi.config_tracks(filepath=conf["filepath"])
            mi.set_nlen(nlen=nlen)
            mi.shift_pitch(semitones=pitch_shift)
            mi.shift_velocity(vel=velocity_shift)

            mi.set_channel_number(channel_number=conf["channel_number"]) # FIXME
        except KeyError as k:
            print(f'No configuation was found for {channel}: {k}')
        # mi.set_tempo(bpm=conf["bpm"])
        # mi.shift_velocity(vel=conf["velocity_shift"])
        # mi.shift_pitch(semitones=conf["pitch_shift"])
        # iters = conf["iters"]

        """
        Change channel_number to track number to be selected (of midi file)
        """
        # mi.set_tempo(bpm=120)
        # mi.shift_pitch(semitones=0)
        # mi.shift_velocity(vel=0)
        # mi.remix_track(nlen=4, iters=10000)
        interfaces.append(mi)

    return interfaces


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        Window.size = (600, 800)

        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=['.mid','.midi']
        )

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Midi Bus",
                "height": dp(56),
                "on_release": lambda x=f"Midi Bus": self.menu_callback(x),
             } # for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        self.channel_index_selected = None
        self.bus = "IAC Driver Bus 1"

        self.midi_config = { # example format
            "channel_0": {
                "filepath": "",
                "channel_number": 0,

                # "pitch_shift": 0,
                # "velocity_shift": 0,
                # "bpm": None, # corresponds to global
                "ngram": 1
            }, "channel_1": {"channel_number": 1, "ngram": 1
            }, "channel_2": {"channel_number": 2, "ngram": 1
            }, "channel_3": {"channel_number": 3, "ngram": 1
            }, "channel_4": {"channel_number": 4, "ngram": 1
            }, "channel_5": {"channel_number": 5, "ngram": 1
            }, "channel_6": {"channel_number": 6, "ngram": 1
            }, "channel_7": {"channel_number": 7, "ngram": 1
            }, "channel_8": {"channel_number": 8, "ngram": 1
            }, "channel_9": {"channel_number": 9, "ngram": 1
            }, "channel_10": {"channel_number": 10, "ngram": 1
            }, "channel_11": {"channel_number": 11, "ngram": 1
            }, "channel_12": {"channel_number": 12, "ngram": 1
            }, "channel_13": {"channel_number": 13, "ngram": 1
            }, "channel_14": {"channel_number": 14, "ngram": 1
            }, "channel_15": {"channel_number": 15, "ngram": 1
            } # 16 total channels
        }

        self.channel_widgets = {}
        self.interfaces = []

        self.iterations = 100
        self.bpm = 120 # make this a per track basis
        self.nlen = 1
        self.pitch_shift = 0
        self.velocity_shift = 0

    def build(self):
        self.title = "PyPlayer"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file(os.path.abspath('kivy/design/v2.kv'))

    """
    Bus
    """
    def set_bus(self):
        self.root.ids.bus_label.text = self.root.ids.bus_input.text
        self.bus = self.root.ids.bus_input.text

    """
    BPM
    """
    def set_bpm(self):

        try:
            self.bpm = int(self.root.ids.bpm_input.text)
        except ValueError as v:
            print(f'set_iterations: {v}')
            self.bpm = 0

        self.root.ids.bpm_label.text = f'{self.bpm} bpm'

    """
    Velocities
    """
    def set_velocity_shift(self, *args):

        try:
            self.velocity_shift = int(args[1])
        except ValueError as v:
            print(f'set_velocity_shift: {v}')
            self.velocity_shift = 0

        self.root.ids.velocity_shift_label.text = f'Velocity Shift: {self.velocity_shift}'

    """
    Pitches
    """
    def set_pitch_shift(self, *args):

        try:
            self.pitch_shift = int(args[1])
        except ValueError as v:
            print(f'set_velocity_shift: {v}')
            self.pitch_shift = 0

        self.root.ids.pitch_shift_label.text = f'Pitch Shift: {self.pitch_shift}'

    """
    Iterations
    """
    def set_iterations(self):

        try:
            self.iterations = int(self.root.ids.iterations_input.text)
        except ValueError as v:
            print(f'set_iterations: {v}')
            self.iterations = 0

        self.root.ids.iterations_labal.text = f'{self.iterations} notes'

    """
    Iterations
    """
    def slide_ngram(self, *args):
        self.nlen = int(args[1])
        self.root.ids.pattern_nlen_label.text = f'Pattern length of {self.nlen}'

    """
    Create & Play -> MidiInterface(s)
    Stop & Destryo -> self.interfaces
    """
    def play_pause(self):

        state = self.root.ids.play_pause_button.icon

        if state == 'play':
            self.root.ids.play_pause_button.icon = 'pause'

            try:
                self.interfaces = configure_midi_interfaces(self.midi_config, self.nlen, self.pitch_shift, self.velocity_shift)
                threads = [] # is this needed?

                for interface in self.interfaces:
                    # interface must be made playable
                    interface.make_playable(playing=True)
                    kwargs = {"iters": self.iterations, "bus": self.bus}
                    t = threading.Thread(target=interface.remix_track, kwargs=kwargs).start()
                    threads.append(t)


            except ValueError as v:
                print(v)
                quit()

        elif state == 'pause':
            self.root.ids.play_pause_button.icon = 'play'

            for interface in self.interfaces:
                try:
                    # interface must become unplayable
                    interface.make_playable(playing=False)
                except Exception as e:
                    print(f'Exception: {e} -- {interface}')

            self.interfaces = []
            print(f"tracks were stopped!")

    """
    File Manager
    """
    def file_manager_open(self, channel_index):
        self.file_manager.show(os.path.abspath('midi/'))  # output manager to the screen
        self.manager_open = True
        self.channel_index_selected = channel_index

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.update_midi_channel_details(self.channel_index_selected, path)

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

        print(f'The saved filepath was: {self.midi_config[f"channel_{self.channel_index_selected}"]["filepath"]}')
        self.channel_index_selected = None # return to starting state

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def update_midi_channel_details(self, channel_index, path):
        print(f'update_midi_channel_details {self.channel_index_selected} midi file.')

        # switch statement
        if channel_index == 0:
            self.root.ids.choose_file_0.text = str(path.split('/')[::-1][0])
            self.midi_config["channel_0"]["filepath"] = path

            self.root.ids.active_file_0.active = True
            """
            self.root.ids.velocity_settings_panels.add_widget(
                MDExpansionPanel(
                    icon="music-note",
                    content=VelocityListItem(),
                    panel_cls=MDExpansionPanelThreeLine(
                        text=f'{"channel_0"}',
                        secondary_text=f'{str(path.split("/")[::-1][0])}',
                        tertiary_text="Modify Velocity",
                    )
                )
            )
            """

        if channel_index == 1:
            self.root.ids.choose_file_1.text = str(path.split('/')[::-1][0])
            self.midi_config["channel_1"]["filepath"] = path

            self.root.ids.active_file_1.active = True

        if channel_index == 2:
            self.root.ids.choose_file_2.text = str(path.split('/')[::-1][0])
            self.midi_config["channel_2"]["filepath"] = path

            self.root.ids.active_file_2.active = True

        if channel_index == 3:
            self.root.ids.choose_file_3.text = str(path.split('/')[::-1][0])
            self.midi_config["channel_3"]["filepath"] = path

            self.root.ids.active_file_3.active = True

    """
    Settings
    """
    def toolbar_callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        MDApp.get_running_app().root.current  = "settings"

if __name__ == "__main__":
    app = MainApp().run()
