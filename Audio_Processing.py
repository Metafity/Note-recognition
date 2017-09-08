############################################################################
#									   #
#			Musical Note Identification 		    	   #
#   									   #
############################################################################

import numpy as np
import wave
import struct

sampling_freq = 44100	              #Sampling frequency of audio signal

def freqToNote(freq) :                #convert freq to note
    
    if(freq > 977 and freq < 1100):
        return "C6"
    if(freq >= 1100 and freq < 1244):
        return "D6"
    
    if(freq >= 1244 and freq < 1355):
        return "E6"

    if(freq >= 1355 and freq < 1479):
        return "F6"

    if(freq >= 1479 and freq < 1661):
        return "G6"

    if(freq >= 1661 and freq < 1864):
        return "A6"

    if(freq >= 1864 and freq < 2030):
        return "B6"

    if(freq >= 2030 and freq < 2217.46):
        return "C7"
        
    if(freq >= 2217.46 and freq < 2489.02):
        return "D7"

    if(freq >= 2489.02 and freq < 2700):
        return "E7"

    if(freq >= 2700 and freq < 2959.96):
        return "F7"

    if(freq >= 2959.96 and freq < 3322.44):
        return "G7"

    if(freq >= 3322.44 and freq < 3729.31):
        return "A7"

    if(freq >= 3729.31 and freq < 4050):
        return "B7"

    if(freq >= 4050 and freq < 4434.92):
        return "C8"

    if(freq >= 4434.92 and freq < 4978.03):
        return "D8"

    if(freq >= 4978.03 and freq < 5370):
        return "E8"

    if(freq >= 5370 and freq < 5919.91):
        return "F8"

    if(freq >= 5919.91 and freq < 6644.88):
        return "G8"

    if(freq >= 6644.88 and freq < 7458.62):
        return "A8"

    if(freq >= 7458.62 and freq <  8000):
        return "B8"


def play(sound_file):    
    file_length = sound_file.getnframes()
    sound = np.zeros(file_length)
    
    for i in range(file_length):
        data = sound_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])

    sound = np.divide(sound, float(2**15)) 
    Identified_Notes  = []                      #return value
    threshold = 0                               #assuming no noise
    flag = 0                                    #0 for continued silence, 1 for note to silence
    Indices = []                                #all indices of sound, for one note
    frame_length = int(sampling_freq * 0.02)
    
    for i in range(0, file_length-frame_length, frame_length):
        temp = max(sound[i: i + frame_length])

        if temp > threshold:                        #continued note
            for k in range(frame_length):
                Indices.append(i + k)       #append indexes in current frame
            flag = 1
            
        elif ((flag == 1) or (flag == 1 and i == file_length - frame_length - 1)):     #found beginning of silence
            flag = 0
            Note = np.take(sound, Indices)                   #take all values of sound at indexes, in Indices
            dftNote = np.fft.fft(Note)                       #fft
            Imax = dftNote.argsort()[::-1][:2]               #to sort in descending order and take 0th and 1st ele because two peaks
            x = min(Imax[0], Imax[1])
            freq = ((x * sampling_freq) / len(Indices))
            Indices = []                                     #empty indices for next note
            Identified_Notes.append(freqToNote(freq))
    return Identified_Notes


############################## Read Audio File #############################

if __name__ == "__main__":

        file_name = "Audio"+".wav"
        sound_file = wave.open(file_name)
        Identified_Notes = play(sound_file)
        print(Identified_Notes)
    


