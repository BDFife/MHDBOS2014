""" 
Import and audio file and generate an output file that is stretched in time.
Blend it with a video file specified. 

ToDo: Modify to hit a specific BPM. 

Heavily adapted from the demo file 'simple_stretch.py' bundled with remix library. 

""" 
import datetime
import sys
from echonest.remix import audio
import subprocess

usage = """

Usage: 
  python jazzer_size.py <input_audio_file> <input_video_file> <output_video_file> <multiplier>
Example: 
  python jazzer_size.py song.mp3 video.mp4 output.mp4 1

"""

def jazz(input_audio, input_video, output_video, mult=1):
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
    print("Multiplier: %s" % mult)

    # stretch the video and drop the audio track
    # the output from this will be 'temp_video_stretch.mp4'
    # fixme: use a variable
    # fixme: if the ratio is *too* close, leave it alone
    chop_video(input_video, video_mp3["bpm"], (float(audio_mp3["bpm"])*float(mult)))

    stretch_duration = get_video_duration('temp_video_stretch.mp4')
    print("Updated Video Duration: %s" % stretch_duration)

    if (audio_mp3["duration"] > float(stretch_duration)):
        print("The music is longer than the video")
        loop_video('temp_video_stretch.mp4')
        # fixme: hardcoded
        trim_video(audio_mp3["duration"], 'temp_video_stretch_full.mp4')
    else:
        print("The video is longer than the music")
        trim_video(audio_mp3["duration"], 'temp_video_stretch.mp4')

    blend_tracks("temp_output_silent.mp4", input_audio, output_video)
    


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

    # This number determines the stretch factor. >1 slows, <1 speeds.
    ratio = audio_bpm / video_bpm

    print("Using Ratio (audio to video) of %s")%ratio

    # Use a version of the video that has the audio dropped.
    ff_silence = "ffmpeg -i %s -vcodec copy -an temp_video.mp4" % video_file
    subprocess.call(ff_silence, shell=True)
    
    # Stretch the silenced video.
    ff_stretch = 'ffmpeg -i temp_video.mp4 -filter:v "setpts=%s*PTS" ./temp_video_stretch.mp4' % ratio
    subprocess.call(ff_stretch, shell=True)

def get_video_duration(video_file):
    """
    Get the duration of the stretched video file
    """

    ff_duration = "ffprobe -i %s -show_format -v quiet | sed -n 's/duration=//p'" % video_file
    return subprocess.check_output(ff_duration, shell=True)

def loop_video(video_file):
    """
    Loop the video. Hardcoded now as x3 because it's late (for me) and I am tired.
    """
    
    # mylist is not written in this program. hardcoded. 
    ff_loop = "ffmpeg -f concat -i mylist.txt -c copy temp_video_stretch_full.mp4"
    subprocess.call(ff_loop, shell=True)

def trim_video(video_seconds, video_file):
    """
    Trim the video to the length of the audio file.
    """

    # I was having trouble getting the format that ffmpeg wanted (0:00:00.00) so I am using datetime. 
    video_time = datetime.timedelta(seconds=video_seconds)
    ff_trim = "ffmpeg -i %s -vcodec copy -acodec copy -ss 00:00:00 -t %s temp_output_silent.mp4" % (video_file, video_time)
    #print(ff_trim)
    subprocess.call(ff_trim, shell=True)

def blend_tracks(video_file, audio_file, output_file):
    """
    Tie together the original audio and final-candidate video tracks.
    """

    ff_blend = "ffmpeg -i %s -i %s %s" % (audio_file, video_file, output_file)
    subprocess.call(ff_blend, shell=True)


if __name__ =='__main__': 
    import sys
    try:
        input_audio = sys.argv[1]
        input_video = sys.argv[2]
        output_video = sys.argv[3]
        mult = sys.argv[4]
    except:
        print usage
        sys.exit(-1)

    # Clean up the damnable temp files
    jazz(input_audio, input_video, output_video, mult)
