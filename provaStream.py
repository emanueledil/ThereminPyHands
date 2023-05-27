import numpy
import  AudioStream as AS
import math
generator = AS.ToneGenerator()

frequency_start = 150  # Frequency to start the sweep from
frequency_end = 10000  # Frequency to end the sweep at
num_frequencies = 200  # Number of frequencies in the sweep
amplitude = 0.50  # Amplitude of the waveform
step_duration = 0.5  # Time (seconds) to play at each step

for frequency in numpy.logspace(math.log(frequency_start, 10),
                                math.log(frequency_end, 10),
                                num_frequencies):

    print("Playing tone at {0:0.2f} Hz".format(frequency))
    generator.play(frequency, step_duration, amplitude)

   # while generator.is_playing():
    #    pass  # Do something useful in here (e.g. recording)