"""
Button example for Pico. Prints button pressed state to serial console.

REQUIRED HARDWARE:
* Button switch on pin GP13.
"""
import time
import board
import digitalio
import audiobusio
import audiocore
from analogio import AnalogIn
import array

button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.GP14)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

analog1in = AnalogIn(board.A0)

audio1 = audiobusio.I2SOut(bit_clock=board.GP20, word_select=board.GP21, data=board.GP22)
buffer = []
processedCopy = []

sample_rate = 16000
conversion_time = 1.5e-6
delay_time_seconds = 1 / sample_rate - conversion_time

potentiometer = AnalogIn(board.A1)

def translate_value(value, from_min, from_max, to_min, to_max):
    # Check for invalid input
    if from_min == from_max:
        raise ValueError("Invalid input: 'from_min' and 'from_max' must be different")

    if to_min == to_max:
        raise ValueError("Invalid input: 'to_min' and 'to_max' must be different")

    # Translate the value from the original range to the new range
    translated_value = to_min + (value - from_min) * (to_max - to_min) / (from_max - from_min)

    # Ensure the result is within the new range
    return max(to_min, min(to_max, int(translated_value)))

def processBuffer(processedCopy):
    potevalue = potentiometer.value
    print('before: '+ str(len(processedCopy)))
    translated = translate_value(potevalue, 0, 65536, 0, len(processedCopy))
    print(translated)

    # Modify the elements of the original list
    del processedCopy[:translated]
    print('after:' + str(len(processedCopy)))

    print((translated,))


while True:
    if (button2.value == True):
        #audio1.play( audiocore.WaveFile( open("8-bit-drums-kick_130bpm_G_minor.wav","rb") ), loop=False)
        processedCopy = buffer.copy()
        processBuffer(processedCopy)
        print('outside: ' + str(len(processedCopy)))
        audio1.play( audiocore.RawSample(array.array("h",processedCopy), sample_rate=16000), loop=False)

    if (button.value == True):
        #audio1.play( audiocore.WaveFile( open("8-bit-drums-snare_130bpm_D_major.wav","rb") ), loop=False)
        sample = analog1in.value - 32768
        if (abs(sample) > 1000):
            buffer.append(sample)
        else:
            buffer.append(0)
        time.sleep(delay_time_seconds)  # Sleep in microseconds
    else :
        #print((potentiometer.value,))
        #time.sleep(0.1)
        pass

