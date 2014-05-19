import pyaudio
import struct
import math
import urllib
import urllib2
import time

INITIAL_TAP_THRESHOLD = 0.0045
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)                  

def get_rms(block):

    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

pa = pyaudio.PyAudio()                                 #]
                                                       #|
stream = pa.open(format = FORMAT,                      #|
         channels = CHANNELS,                          #|---- You always use this in pyaudio...
         rate = RATE,                                  #|
         input = True,                                 #|
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)   #]    

while True:
    try:                                                    #]
        block = stream.read(INPUT_FRAMES_PER_BLOCK)         #|
    except IOError, e:                                      #|---- just in case there is an error!
        errorcount += 1                                     #|
        print( "Error recording: %s"%(e) )  #|

    amplitude = get_rms(block)
    #print amplitude
    if amplitude > INITIAL_TAP_THRESHOLD: 
        print 'Soglia superata!'
        try:
            response = urllib2.urlopen('http://192.168.0.86:8080/volumedown/')
            html = response.read()
        except:
            print "errore nel web server"

