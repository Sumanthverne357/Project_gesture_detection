import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="Medical Media Player", page_icon=":microscope:")
    st.title("Medical Media Player")

    st.sidebar.header("Media Controls")
    media_type = st.sidebar.radio("Select Media Type", ("Image", "GIF", "Video"))

    if media_type == "Image":
        uploaded_file = st.sidebar.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
    elif media_type == "GIF":
        uploaded_file = st.sidebar.file_uploader("Upload GIF", type=['gif'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded GIF', use_column_width=True)
    else:
        uploaded_file = st.sidebar.file_uploader("Upload Video", type=['mp4', 'avi', 'webm'])
        if uploaded_file is not None:
            st.video(uploaded_file)

    # Playback controls
    if st.sidebar.button("Play/Pause"):
        st.write("Play/Pause button clicked!")
    if st.sidebar.button("Forward"):
        st.write("Forward button clicked!")
    if st.sidebar.button("Backward"):
        st.write("Backward button clicked!")
    if st.sidebar.button("Rotate Right"):
        st.write("Rotate Right button clicked!")
    if st.sidebar.button("Rotate Left"):
        st.write("Rotate Left button clicked!")

if __name__ == "__main__":
    main()
  
