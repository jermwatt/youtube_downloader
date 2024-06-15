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
        with col3:
            empty_container = st.container()
        with col4:
            placeholder = st.empty()
            
            
def button_logic(url: str) -> None:
    if check_button_val:
        yt, yt_title, yt_thumbnail_url, audio_only_streams, video_only_streams, audio_video_streams = get_yt_streams(url)
        st.write(url)
        pass
    
with st.spinner(text="streams pull in progress..."):
    button_logic(url)
