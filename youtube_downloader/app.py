import streamlit as st
from youtube_downloader.streams import get_yt_streams
from youtube_downloader.download import download_thumbnail, download_joint_stream, download_separate_streams_and_join
import tempfile


st.title("Youtube Downloader")
st.markdown("instructions: paste a valid youtube url in the textbox and download ")

# Initialization
if "stream_button_pressed" not in st.session_state:
    st.session_state["stream_button_pressed"] = False
if "yt" not in st.session_state:
    st.session_state["yt"] = None
if "yt_title" not in st.session_state:
    st.session_state["yt_title"] = None
if "yt_thumbnail_url" not in st.session_state:
    st.session_state["yt_thumbnail_url"] = None

if "a_v_selection_index" not in st.session_state:
    st.session_state["a_v_selection_index"] = 1
if "audio_video_streams" not in st.session_state:
    st.session_state["audio_video_streams"] = None
if "audio_video_choices" not in st.session_state:
    st.session_state["audio_video_choices"] = None

if "v_selection_index" not in st.session_state:
    st.session_state["v_selection_index"] = 0
if "video_only_streams" not in st.session_state:
    st.session_state["video_streams"] = None
if "video_only_choices" not in st.session_state:
    st.session_state["video_only_choices"] = None

if "a_selection_index" not in st.session_state:
    st.session_state["a_selection_index"] = 0
if "audio_only_streams" not in st.session_state:
    st.session_state["audio_only_streams"] = None
if "audio_only_choices" not in st.session_state:
    st.session_state["audio_only_choices"] = None


base = st.container(border=True)
with base:
    x, col1, y = st.columns([3, 20, 3])
    with col1:
        url = col1.text_input(
            label="enter youtube url",
            placeholder="your youtube url goes here",
            value="https://www.youtube.com/shorts/R1P1FgTrcHo",
        )
        col2, col3, col4 = st.columns([3, 2, 3])
        with col2:
            check_button_val = st.button(
                label="fetch available streams", type="primary"
            )
        with col3:
            empty_container = st.container()
        with col4:
            placeholder = st.empty()


def get_set_streams(url: str) -> None:
    # collect video data
    (
        yt,
        yt_title,
        yt_thumbnail_url,
        audio_only_streams,
        video_only_streams,
        audio_video_streams,
    ) = get_yt_streams(url)

    # save to session state
    st.session_state["yt"] = yt
    st.session_state["yt_title"] = yt_title
    st.session_state["yt_thumbnail_url"] = yt_thumbnail_url

    audio_video_choices = []
    if len(audio_video_streams) > 0:
        audio_video_choices = [(v.resolution, v.itag) for v in audio_video_streams]
        audio_video_choices = tuple([None] + [v[0] for v in audio_video_choices])
        st.session_state["audio_video_choices"] = audio_video_choices
        st.session_state["audio_video_streams"] = audio_video_streams

    video_only_choices = []
    if len(video_only_streams):
        video_only_choices = [(v.resolution, v.itag) for v in video_only_streams]
        video_only_choices = tuple([None] + [v[0] for v in video_only_choices])
        st.session_state["video_only_choices"] = video_only_choices
        st.session_state["video_only_streams"] = video_only_streams

    audio_only_choices = []
    if len(audio_only_streams) > 0:
        audio_only_choices = [(v.abr, v.itag) for v in audio_only_streams]
        audio_only_choices = tuple([None] + [v[0] for v in audio_only_choices])
        st.session_state["audio_only_choices"] = audio_only_choices
        st.session_state["audio_only_streams"] = audio_only_streams


def download_button_logic(download_button_val: bool):
    if download_button_val:
        if st.session_state["a_v_selection_index"] == 0:
            if (
                st.session_state["a_selection_index"] == 0
                and st.session_state["v_selection_index"] == 0
            ):
                st.warning("please make a selection", icon="⚠️")
            elif (
                st.session_state["a_selection_index"] == 0
                or st.session_state["v_selection_index"] == 0
            ):
                st.warning(
                    "if video only value chosen so must audio only value and vice-versa",
                    icon="⚠️",
                )
            else:
                with st.spinner(text="download in progress..."):
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        vid_col, img_col = st.columns([4, 2])
                        # download thumbnail
                        img_savepath = download_thumbnail(
                            st.session_state["yt_thumbnail_url"],
                            st.session_state["yt_title"],
                            tmpdirname,
                        )
                        with img_col:
                            st.subheader("thumbnail")
                            st.image(img_savepath, caption=st.session_state["yt_title"])

                        # download audio/video jointly
                        audio_index = st.session_state["a_selection_index"]
                        audio_only_streams = st.session_state["audio_only_streams"]
                        audio_selection = audio_only_streams[audio_index]
                        audio_itag = audio_selection.itag
                        
                        video_index = st.session_state["v_selection_index"]
                        video_only_streams = st.session_state["video_only_streams"]
                        video_selection = video_only_streams[video_index]
                        video_itag = video_selection.itag
                        video_savepath = download_separate_streams_and_join(st.session_state["yt"],
                                                                            audio_itag, 
                                                                            video_itag, 
                                                                            tmpdirname,
                                                                            st.session_state["yt_title"])
            
                        with vid_col:
                            st.subheader("video")
                            video_file = open(video_savepath, "rb")
                            video_bytes = video_file.read()
                            st.video(video_bytes)
        else:
            if (
                st.session_state["a_selection_index"] != 0
                or st.session_state["v_selection_index"] != 0
            ):
                st.warning(
                    "cannot chose option for audio/video joint, video only, and audio only",
                    icon="⚠️",
                )
            else:
                with st.spinner(text="download in progress..."):
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        vid_col, img_col = st.columns([4, 2])
                        # download thumbnail
                        img_savepath = download_thumbnail(
                            st.session_state["yt_thumbnail_url"],
                            st.session_state["yt_title"],
                            tmpdirname,
                        )
                        with img_col:
                            st.subheader("thumbnail")
                            st.image(img_savepath, caption=st.session_state["yt_title"])

                        # download audio/video jointly
                        index = st.session_state["a_v_selection_index"]
                        audio_video_streams = st.session_state["audio_video_streams"]
                        selection = audio_video_streams[index]
                        itag = selection.itag
                        video_savepath = download_joint_stream(
                            st.session_state["yt"],
                            itag,
                            tmpdirname,
                            st.session_state["yt_title"],
                        )
                        with vid_col:
                            st.subheader("video")
                            video_file = open(video_savepath, "rb")
                            video_bytes = video_file.read()
                            st.video(video_bytes)


def render_panel():
    with st.container(border=True):
        col_a, col_b, col_c = st.columns([5, 5, 5])
        a_selection, v_selection, a_v_selection = None, None, None

        with col_a:
            a_v_selection = st.selectbox(
                "audio/video joint selection (fps)",
                options=st.session_state["audio_video_choices"],
                index=st.session_state["a_v_selection_index"],
                placeholder="Select video fps",
            )
            if a_v_selection:
                st.session_state["a_v_selection_index"] = list(
                    st.session_state["audio_video_choices"]
                ).index(a_v_selection)
            else:
                st.session_state["a_v_selection_index"] = 0

        with col_b:
            v_selection = st.selectbox(
                "video only selection (fps)",
                options=st.session_state["video_only_choices"],
                index=st.session_state["v_selection_index"],
                placeholder="Select video fps",
            )
            if v_selection:
                st.session_state["v_selection_index"] = list(
                    st.session_state["video_only_choices"]
                ).index(v_selection)
            else:
                st.session_state["v_selection_index"] = 0

        with col_c:
            a_selection = st.selectbox(
                "audio only selection (kbps)",
                options=st.session_state["audio_only_choices"],
                index=st.session_state["a_selection_index"],
                placeholder="Select audio kbps",
            )
            if a_selection:
                st.session_state["a_selection_index"] = list(
                    st.session_state["audio_only_choices"]
                ).index(a_selection)
            else:
                st.session_state["a_selection_index"] = 0

    # download button
    download_button_val = st.button(label="download selected stream", type="primary")
    download_button_logic(download_button_val)


def streams_button_logic(url: str) -> None:
    if check_button_val:
        st.session_state["stream_button_pressed"] = True
        get_set_streams(url)
        render_panel()


if st.session_state["stream_button_pressed"]:
    render_panel()

with st.spinner(text="streams pull in progress..."):
    streams_button_logic(url)
