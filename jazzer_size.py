""" 
Import and audio file and generate an output file that is stretched in time.
Blend it with a video file specified. 

ToDo: Modify to hit a specific BPM. 

Heavily adapted from the demo file 'simple_stretch.py' bundled with remix library. 

""" 

import sys
from echonest.remix import audio
import subprocess

usage = """

Usage: 
  python audio_stretch.py <input_audio_file> <input_video_file> <output_video_file>
Example: 
  python audio_stretch.py song.mp3 video.mp4 output.mp4

"""

def jazz(input_audio, input_video, output_video):
    """
    Main loop. Go big or go home.
    
    Tasks:
      1) Separate the audio file from the video and get duration, BPM.
      2) Get duration and BPM of the to-match audio file.
      3) Strip the audio from the video file.
      4) If necessary, stretch or compress video file
      5) If necessary, loop the altered video file
      6) Blend the target audio and altered video
      7) Enjoy
    """
    
    extract_audio(input_video)

    # fixme: this is dirty variable handling
    video_mp3 = track_data("temp_audio.mp3")
    audio_mp3 = track_data(input_audio)

    print("Video Duration: %s" % video_mp3["duration"]) 
    print("Video BPM: %s" % video_mp3["bpm"]) 
    print("Audio Duration: %s" % audio_mp3["duration"]) 
    print("Audio BPM: %s" % audio_mp3["bpm"]) 

    chop_video(input_video, video_mp3["bpm"], audio_mp3["bpm"])

def extract_audio(video_file):
    """
    Pull the audio track from a video file and return as an encoded mp3 file.
    """

    #fixme: check the output of this function
    #fixme: break out the options and stuff

    ff_strip = "ffmpeg -i %s -vn -ac 2 -ar 44100 -ab 128k -f mp3 temp_audio.mp3" % input_video
    subprocess.call(ff_strip, shell=True)
    
def track_data(audio_file):
    """
    Get BPM and duration of Audio
    """

    audiofile = audio.LocalAudioFile(audio_file)
    tempo = audiofile.analysis.tempo
    bpm = tempo.get("value")
    duration = audiofile.analysis.duration

    return {'bpm':bpm,
            'duration':duration}

def chop_video(video_file, video_bpm, audio_bpm):
    """
    Develop a BPM ratio and run a ffmpeg command to align
    """
    
    pass

#def stretch_audio(input_filename):
#    """
#    Get BPM of Audio
#    """
#
#    audiofile = audio.LocalAudioFile(input_filename)
#    tempo = audiofile.analysis.tempo
#    # Fixme: replace with a value return.
#    print(tempo.get("value"))
#    
#    #beats = audiofile.analysis.beats
#    #print(beats)

if __name__ =='__main__': 
    import sys
    try:
        input_audio = sys.argv[1]
        input_video = sys.argv[2]
        output_video = sys.argv[3]

    except:
        print usage
        sys.exit(-1)

    jazz(input_audio, input_video, output_video)
