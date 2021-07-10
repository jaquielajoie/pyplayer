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
Text Input
"""
midibus_e = tk.Entry(root, width=50, bg="#FFFFFF", borderwidth=5)
midibus_e.grid(row=0, column=0, columnspan=12)
midibus_e.insert(0, "IAC Driver Bus 1")


"""
File Management
- Label
- Button
- Button Frame (border)
- Filedialog
- Var (filepath)
"""
# open the file
def open_midifile():
    root.midifile = filedialog.askopenfilename(initialdir=midipath, title="Select a MID/MIDI file",
                        filetypes=(("mid files", "*.mid"), ("midi files", "*.midi"), ("all files", "*.*"))
                    )
    # midifile_label = tk.Label(root, text=root.midifile,
    #         font = (("Times New Roman"), 15)).grid(row=1, column=12, columnspan=12)

midifile_bttn_border = tk.Frame(root, highlightbackground = "black",
                         highlightthickness = 2, bd=0).grid(row=0, column=12, columnspan=12)
midifile_bttn = tk.Button(midifile_bttn_border, text='Open Midi File', fg = 'black',
                 highlightbackground="yellow" ,font = (("Times New Roman"),15), command=open_midifile).grid(row=0, column=12, columnspan=12)


"""
NGram Settings
- Label
- Var (ngram size)
- Radiobuttons
"""
# Size
ngram_radio_l = tk.Label(root, text="NGram Size: ",
         font = (("Times New Roman"), 18)).grid(row=1, column=0, columnspan=3)
ngram_size = tk.IntVar()
ngram_size.set(1)
tk.Radiobutton(root, text="Length 1", variable=ngram_size, value=1, font = (("Times New Roman"), 15)).grid(row=2, column=0, columnspan=3)
tk.Radiobutton(root, text="Length 2", variable=ngram_size, value=2, font = (("Times New Roman"), 15)).grid(row=3, column=0, columnspan=3)
tk.Radiobutton(root, text="Length 4", variable=ngram_size, value=4, font = (("Times New Roman"), 15)).grid(row=4, column=0, columnspan=3)
tk.Radiobutton(root, text="Length 8", variable=ngram_size, value=8, font = (("Times New Roman"), 15)).grid(row=5, column=0, columnspan=3)
tk.Radiobutton(root, text="Length 12", variable=ngram_size, value=12, font = (("Times New Roman"), 15)).grid(row=6, column=0, columnspan=3)
tk.Radiobutton(root, text="Length 16", variable=ngram_size, value=16, font = (("Times New Roman"), 15)).grid(row=7, column=0, columnspan=3)

# Tempo

# Velocity

"""
Pitch Settings
- Drop Down Box
"""
pitch_shift_l = tk.Label(root, text="Pitch Shift: ",
         font = (("Times New Roman"), 18)).grid(row=13, column=0, columnspan=3)
pitch_shift = tk.IntVar()
pitch_shift.set(0)
pitch_options = [shift for shift in range(-24,25)]
pitch_shift_dropdown = tk.OptionMenu(root, pitch_shift, *pitch_options).grid(row=14, column=0, columnspan=3)


"""
Velocity Settings
- Drop Down Box
"""
velocity_shift_l = tk.Label(root, text="Velocity Shift: ",
         font = (("Times New Roman"), 18)).grid(row=13, column=4, columnspan=3)
velocity_shift = tk.IntVar()
velocity_shift.set(0)
velocity_options = [shift for shift in range(-48,49)]
velocity_shift_dropdown = tk.OptionMenu(root, velocity_shift, *velocity_options).grid(row=14, column=4, columnspan=3)


"""
BPM Settings Settings
- Text Input
"""
bpm_shift_l = tk.Label(root, text="BPM: ",
         font = (("Times New Roman"), 18)).grid(row=1, column=7, columnspan=3)
bpm_e = tk.Entry(root, width=50, bg="#FFFFFF", borderwidth=5)
bpm_e.grid(row=2, column=8, columnspan=4)
bpm_e.insert(0, 120)


"""
Iterations
- Text Input
"""
iters_shift_l = tk.Label(root, text="Iterations: ",
         font = (("Times New Roman"), 18)).grid(row=1, column=8, columnspan=3)
iters_e = tk.Entry(root, width=50, bg="#FFFFFF", borderwidth=5)
iters_e.grid(row=2, column=10, columnspan=4)
iters_e.insert(0, 10000)


"""
Start Settings
"""
# Start
def start():
    start_settings_label = tk.Label(root, text=f"{pitch_shift}\n{ngram_size}\n{velocity_shift}",
        font = (("Times New Roman"), 15)).grid(row=2, column=12, columnspan=12)
    mi.config_tracks(filepath=root.midifile)
    mi.set_tempo(bpm=int(bpm_e.get()))
    mi.shift_pitch(semitones=pitch_shift.get())
    mi.shift_velocity(vel=velocity_shift.get())
    mi.remix_tracks(nlen=ngram_size.get(), iters=int(iters_e.get()))

start_bttn_border = tk.Frame(root, highlightbackground = "black",
                         highlightthickness = 2, bd=0).grid(row=2, column=12, columnspan=12)
start_bttn = tk.Button(start_bttn_border, text='Start', fg = 'black',
                 highlightbackground="green" ,font = (("Times New Roman"),15), command=start).grid(row=25, column=12, columnspan=12)


# Tempo Settings?

"""
Status Bar
"""
# root.status = "Not Running"
# status_l = tk.Label(root, text=root.status, fg="#ABABAB").grid(row=36, column=12, columnspan=12, pady=10)


"""
Run Loop
"""
root.mainloop()
