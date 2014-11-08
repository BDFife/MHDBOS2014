""" 
Import and audio file and generate an output file that is stretched in time. 

ToDo: Modify to hit a specific BPM. 

Heavily adapted from the demo file 'simple_stretch.py' bundled with remix library. 

""" 

import sys
from echonest.remix import audio

usage = """

Usage: 
  python audio_stretch.py <input_file> <output_file> <ratio> 
Example: 
  python audio_stretch.py song.mp3 output_song.mp3 0.75

"""

def stretch_audio(input_filename, output_filename, ratio):
    audiofile = audio.LocalAudioFile(input_filename)
    beats = audiofile.analysis.beats
    print(beats)


if __name__ =='__main__': 
    import sys
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        ratio = float(sys.argv[3])
    except:
        print usage
        sys.exit(-1)

    stretch_audio(input_filename, output_filename, ratio)
