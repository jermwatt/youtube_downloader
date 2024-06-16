import tempfile
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import requests


def download_thumbnail(yt_thumbnail_url: str,
                       yt_title: str,
                       save_dir: str) -> str:
    img_data = requests.get(yt_thumbnail_url).content
    img_ext = yt_thumbnail_url.split(".")[-1]
    savepath = save_dir + "/" + yt_title + "." + img_ext
    with open(savepath, 'wb') as handler:
        handler.write(img_data)
    return savepath


def download_joint_stream(yt: YouTube,
                          itag: int,
                          save_dir: str,
                          yt_title: str) -> None:
    try:
        yt.streams.get_by_itag(itag).download(filename=save_dir + yt_title + ".mp4")
    except Exception as e:
        raise ValueError(f"download_joint_stream failed with exception {e}")
    
    
def download_separate_streams_and_join(yt: YouTube,
                                      audio_itag: int,
                                      video_itag: int,
                                      save_dir: str,
                                      yt_title: str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpaudiopath = tmpdirname + "/" + yt_title + "_audio.mp4"
        tmpvideopath = tmpdirname + "/" + yt_title + "_video.mp4"
        yt.streams.get_by_itag(audio_itag).download(filename=tmpaudiopath)
        yt.streams.get_by_itag(video_itag).download(filename=tmpvideopath)
        
        # combine the video clip with the audio clip
        video_clip = VideoFileClip(tmpvideopath)
        audio_clip = AudioFileClip(tmpaudiopath)
        video_clip.audio = audio_clip
        video_clip.write_videofile(
            save_dir + "/" +  yt_title + ".mp4",
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )