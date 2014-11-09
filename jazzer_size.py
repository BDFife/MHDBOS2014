""" 
Import and audio file and generate an output file that is stretched in time.
Blend it with a video file specified. 

ToDo: Modify to hit a specific BPM. 

Heavily adapted from the demo file 'simple_stretch.py' bundled with remix library. 

""" 

import sys
from echonest.remix import audio

usage = """

Usage: 
  python audio_stretch.py <input_file> 
Example: 
  python audio_stretch.py song.mp3 

"""

def stretch_audio(input_filename):
    """
    Get BPM of Audio
    """

    audiofile = audio.LocalAudioFile(input_filename)
    tempo = audiofile.analysis.tempo
    # Fixme: replace with a value return.
    print(tempo.get("value"))
    
    #beats = audiofile.analysis.beats
    #print(beats)


if __name__ =='__main__': 
    import sys
    try:
        input_filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)

    stretch_audio(input_filename)
