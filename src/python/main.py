from mido_interface import MidiInterface

if __name__ == "__main__":
    mi = MidiInterface()
    mi.config_tracks()
    mi.set_tempo(bpm_denom=120)
    mi.shift_pitch(semitones=18)
    mi.shift_velocity(vel=-25)
    mi.remix_tracks(nlen=4, iters=1000000)
