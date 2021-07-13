"""
==========================================
 Title:  PyPlayer GUI
 Author: @jaquielajoie
 Date:   9 July 2021
 Liscence: Apache 2.0
==========================================
"""
import tkinter as tk
from tkinter import filedialog
from pyplayer.mido_interface import MidiInterface
import os

WIDTH = 800
HEIGHT = 700

"""
The midi interface is what triggers the markov chain to play or remix the midi file.
The midi interface uses mido to turn byte strings into midi notes.
Mido has an API to configure midi ports - this is used to send messages to a DAW.
"""
mi = MidiInterface()

# media paths
pngpath = os.path.abspath("gui/icons/favicon.png")

# midi path
midipath = os.path.abspath("midi/")

"""
GUI Components
- midifile dialog
- bus selection
- ngram setting
"""
# Root config
root = tk.Tk()
root.configure(bg="#FEFEFE", borderwidth=10)
root.iconphoto(True, tk.PhotoImage(file=pngpath))
root.title("PyPlayer")
root.midifile = None

"""
MAIN: Canvas & Main Frame
"""
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#80C1FF')
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.75, anchor='n')

"""
File Management
- Label
- Button
- Button Frame (border)
- Filedialog
- Var (filepath)
"""
# midi_frame = tk.Frame(root, bg='#000000')
# midi_frame.place(anchor='n', relx=0.05, rely=0.05, relwidth=0.9, relheight=0.25)

# Midi Bus Config
midibus_e = tk.Entry(frame, width=50, bg="#FFFFFF", borderwidth=5)
midibus_e.place(anchor='ne', relwidth=0.65, relheight=0.05)
midibus_e.insert(0, "IAC Driver Bus 1")

# Midi File Config
def open_midifile():
    root.midifile = filedialog.askopenfilename(initialdir=midipath, title="Select a MID/MIDI file",
                        filetypes=(("mid files", "*.mid"), ("midi files", "*.midi"), ("all files", "*.*"))
                    )

"""
Start Settings
"""
# Start
def start():
    start_settings_label = tk.Label(frame, text=f"{pitch_shift}\n{ngram_size}\n{velocity_shift}",
        font = (("Times New Roman"), 15)).pack()
    mi.config_tracks(filepath=root.midifile)
    mi.set_tempo(bpm=int(bpm_e.get()))
    mi.shift_pitch(semitones=pitch_shift.get())
    mi.shift_velocity(vel=velocity_shift.get())
    mi.remix_tracks(nlen=ngram_size.get(), iters=int(iters_e.get()))

start_bttn = tk.Button(frame, text='Start', fg = 'black',
                 highlightbackground="green" ,font = (("Times New Roman"),15), command=start).place(anchor='s', relwidth=0.3, relheight=0.05)


# midifile_bttn = tk.Button(frame, text='Open Midi File', fg = 'black',
#                 highlightbackground="yellow" ,font = (("Times New Roman"),15), command=open_midifile).pack()


"""
NGram Settings
- Label
- Var (ngram size)
- Radiobuttons
"""
# Size
ngram_radio_l = tk.Label(frame, text="NGram Size: ",
         font = (("Times New Roman"), 18)).pack()
ngram_size = tk.IntVar()
ngram_size.set(1)
tk.Radiobutton(frame, text="Length 1", variable=ngram_size, value=1, font = (("Times New Roman"), 15)).place(anchor='ne', relx=0.7, rely=0, relwidth=0.3, relheight=0.1)
tk.Radiobutton(frame, text="Length 2", variable=ngram_size, value=2, font = (("Times New Roman"), 15)).place(anchor='ne', relx=0.7, rely=0, relwidth=0.3, relheight=0.1)
tk.Radiobutton(frame, text="Length 4", variable=ngram_size, value=4, font = (("Times New Roman"), 15)).place(anchor='ne', relx=0.7, rely=0, relwidth=0.3, relheight=0.1)
tk.Radiobutton(frame, text="Length 8", variable=ngram_size, value=8, font = (("Times New Roman"), 15)).place(anchor='ne', relx=0.7, rely=0, relwidth=0.3, relheight=0.1)
tk.Radiobutton(frame, text="Length 12", variable=ngram_size, value=12, font = (("Times New Roman"), 15)).place(anchor='ne', relx=0.7, rely=0, relwidth=0.3, relheight=0.1)
tk.Radiobutton(frame, text="Length 16", variable=ngram_size, value=16, font = (("Times New Roman"), 15)).place(anchor='ne', relx=0.7, rely=0, relwidth=0.3, relheight=0.1)

# Tempo

# Velocity

"""
Pitch Settings
- Drop Down Box
"""
pitch_shift_l = tk.Label(frame, text="Pitch Shift: ",
         font = (("Times New Roman"), 18)).pack()
pitch_shift = tk.IntVar()
pitch_shift.set(0)
pitch_options = [shift for shift in range(-24,25)]
pitch_shift_dropdown = tk.OptionMenu(frame, pitch_shift, *pitch_options).pack()


"""
Velocity Settings
- Drop Down Box
"""
velocity_shift_l = tk.Label(frame, text="Velocity Shift: ",
         font = (("Times New Roman"), 18)).pack()
velocity_shift = tk.IntVar()
velocity_shift.set(0)
velocity_options = [shift for shift in range(-48,49)]
velocity_shift_dropdown = tk.OptionMenu(frame, velocity_shift, *velocity_options).pack()


"""
BPM Settings Settings
- Text Input
"""
bpm_shift_l = tk.Label(frame, text="BPM: ",
         font = (("Times New Roman"), 18)).pack()
bpm_e = tk.Entry(frame, width=50, bg="#FFFFFF", borderwidth=5)
bpm_e.pack()
bpm_e.insert(0, 120)


"""
Iterations
- Text Input
"""
iters_shift_l = tk.Label(frame, text="Iterations: ",
         font = (("Times New Roman"), 18)).pack()
iters_e = tk.Entry(frame, width=50, bg="#FFFFFF", borderwidth=5)
iters_e.pack()
iters_e.insert(0, 10000)


"""
start_bttn_border = tk.Frame(frame, highlightbackground = "black",
                         highlightthickness = 2, bd=0).pack()
 """

# Tempo Settings?

"""
Status Bar
"""


"""
Run Loop
"""
root.mainloop()
