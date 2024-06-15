import streamlit as st
from youtube_downloader.streams import get_yt_streams


st.title("Youtube Downloader")
st.markdown(
    "instructions: paste a valid youtube url in the textbox and download "
)


base = st.container(border=True)
with base:
    x, col1, y = st.columns([3, 20, 3])
    with col1:
        url = col1.text_input(label="enter youtube url", placeholder="your youtube url goes here")
        col2, col3, col4 = st.columns([3, 2, 3])
        with col2:
            check_button_val = st.button(label="fetch available streams", type="primary")
            video_options = st.selectbox(
                            "fps",
                            (),
                            index=None,
                            placeholder="Select video fps",
                            )

        with col3:
            empty_container = st.container()
        with col4:
            placeholder = st.empty()
            
            
def button_logic(url: str) -> None:
    if check_button_val:
        yt, yt_title, yt_thumbnail_url, audio_only_streams, video_only_streams, audio_video_streams = get_yt_streams(url)

        # grab all choices from different stream types
        audio_only_choices = [(v.abr, v.itag) for v in audio_only_streams]
        video_only_choices = [(v.resolution, v.itag) for v in video_only_streams]
        audio_video_joint_choices = [(v.resolution, v.itag) for v in audio_video_streams]

        st.write(video_only_choices)
        st.write(video_only_choices[0][0])
        
        # video_options.options = (v[0] for v in video_only_choices)
        st.write(url)
        pass
    
with st.spinner(text="streams pull in progress..."):
    button_logic(url)
