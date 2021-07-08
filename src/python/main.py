from markov import MarkovMidiPlayer

if __name__ == "__main__":
    nlen = 2
    note_list = [1,2,3,4,5,6,7,8,9,8,7,6,7,8,7,6,5,4,5,6,7,6,5,4,8,6,6,4,2,1,2,3,54,7,8,431,2,678,7,5,23,1] # replace with mido notes...
    mmp = MarkovMidiPlayer(nlen=nlen, note_list=note_list)
    mmp.run(100000)
