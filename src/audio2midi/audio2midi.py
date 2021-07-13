import os
import librosa as li
import librosa.display as lid
import matplotlib.pyplot as plt

bpm = 120

num2note = {
    0: "C"
    , 1: "C#"
    , 2: "D"
    , 3: "D#"
    , 4: "E"
    , 5: "F"
    , 6: "F#"
    , 7: "G"
    , 8: "G#"
    , 9: "A"
    , 10: "A#"
    , 11: "B"
    , 12: "C"
}

def get_signal(filename, folder='loops', duration=5):
    audio_path = os.path.abspath(f'../audio/{folder}/{filename}')
    y, sr = li.load(audio_path, duration=duration)
    return y, sr

def set_window_size(sr, bpm, scale):
    return samples_per_beat(sr=sr, bpm=bpm) * scale

def samples_per_beat(sr, bpm=60):
    # sr = samples per second
    beats_per_second = bpm / 60
    return int(sr // beats_per_second)

def seconds_to_samples(sr, seconds):
    return sr * seconds

def avg_chunk(chunk):
    return sum(chunk) / len(chunk)


if __name__ == "__main__":
    y, sr = get_signal(filename='a_tone.wav', folder='one_shots', duration=10)

    window_size = set_window_size(sr=sr, bpm=bpm, scale=1)
    chroma_chunks = []

    try:
        # set max length to process
        samples_to_scan = seconds_to_samples(sr=sr, seconds=20)

        for i in range(0, samples_to_scan - 1):
            chroma = li.feature.chroma_stft(y=y[i * window_size: (i+1) * window_size], sr=sr)
            chroma_chunks.append(chroma)

    except Exception as e:
        # likely out of bounds
        print(e)

    for chunk in chroma_chunks:
        fig, ax = plt.subplots()
        img = lid.specshow(chunk, y_axis='chroma', x_axis='time', ax=ax)
        fig.colorbar(img, ax=ax)
        ax.set(title='Chromagram')
        plt.show()
