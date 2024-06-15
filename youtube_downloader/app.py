import streamlit as st
from youtube_downloader.streams import get_yt_streams


st.title("Youtube Downloader")
st.markdown(
    "instructions: paste a valid youtube url in the textbox and download "
)

# Initialization
if "stream_button_pressed" not in st.session_state:
    st.session_state["stream_button_pressed"] = False
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
        url = col1.text_input(label="enter youtube url",
                              placeholder="your youtube url goes here",
                              value="https://www.youtube.com/watch?v=v8Tp3g40y6Y")
        col2, col3, col4 = st.columns([3, 2, 3])
        with col2:
            check_button_val = st.button(label="fetch available streams", type="primary")
        with col3:
            empty_container = st.container()
        with col4:
            placeholder = st.empty()
         

def get_set_streams(url: str) -> None:
    # collect video data
    yt, yt_title, yt_thumbnail_url, audio_only_streams, video_only_streams, audio_video_streams = get_yt_streams(url)

    # save to session state
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
                st.session_state["a_v_selection_index"] = list(st.session_state["audio_video_choices"]).index(a_v_selection)

        with col_b:
            v_selection = st.selectbox(
                                "video only selection (fps)",
                                options=st.session_state["video_only_choices"],
                                index=st.session_state["v_selection_index"],
                                placeholder="Select video fps",
                                )
            if v_selection:
                st.session_state["v_selection_index"] = list(st.session_state["video_only_choices"]).index(v_selection)

        with col_c:
            a_selection = st.selectbox(
                        "audio only selection (kbps)",
                        options=st.session_state["audio_only_choices"],
                        index=st.session_state["a_selection_index"],
                        placeholder="Select audio kbps",
                        )
            if a_selection:
                st.session_state["a_selection_index"] = list(st.session_state["audio_only_choices"]).index(a_selection)

                    
    # download button
    download_button_val = st.button(label="download selected stream", type="primary")             
   
            
def button_logic(url: str) -> None:
    if check_button_val:
        st.session_state["stream_button_pressed"] = True
        get_set_streams(url)
        render_panel()
    

if st.session_state["stream_button_pressed"]:
    render_panel()

with st.spinner(text="streams pull in progress..."):
    button_logic(url)
