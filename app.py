import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import os
import tempfile

st.set_page_config(page_title="Text to Video Generator", layout="centered")

st.title("🎬 Text to Video Generator")
st.write("Enter text below to generate a video with voice narration.")

# Text input
user_text = st.text_area("Enter your text here:", height=200)

# Background color and video duration
bg_color = st.color_picker("Choose background color", "#000000")
duration = st.slider("Video duration (seconds):", 5, 60, 10)

if st.button("Generate Video"):
    if not user_text.strip():
        st.warning("Please enter some text to generate the video.")
    else:
        with st.spinner("Generating video... please wait."):
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Generate audio using gTTS
                audio_path = os.path.join(temp_dir, "audio.mp3")
                tts = gTTS(text=user_text, lang="en")
                tts.save(audio_path)

                # Create an image clip with background color
                txt_clip = TextClip(
                    user_text,
                    fontsize=40,
                    color="white",
                    size=(1280, 720),
                    method="caption",
                    align="center"
                ).on_color(size=(1280, 720), color=bg_color, col_opacity=1)

                # Load audio and set duration
                audio_clip = AudioFileClip(audio_path)
                video_clip = txt_clip.set_audio(audio_clip).set_duration(duration)

                # Save video
                output_path = os.path.join(temp_dir, "text_video.mp4")
                video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                st.success("✅ Video generated successfully!")
                st.video(output_path)

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Video",
                        data=file,
                        file_name="text_to_video.mp4",
                        mime="video/mp4"
                    )
