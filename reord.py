import streamlit as st
import pyaudio
import wave
import dropbox
import os


# ... Code for recording audio from the previous example ...
def record_audio(filename, duration, sample_rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    frames = []
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def upload_to_dropbox(filename, access_token, dropbox_folder="/Audio_Recordings/"):
    dbx = dropbox.Dropbox(access_token)

    with open(filename, "rb") as f:
        audio_data = f.read()

    try:
        dbx.files_upload(audio_data, dropbox_folder + os.path.basename(filename))
        st.write("Audio uploaded to Dropbox successfully.")
    except dropbox.exceptions.ApiError as e:
        st.write(f"Error uploading audio to Dropbox: {e}")

def main():
    # ... Code for the Streamlit app from the previous example ...
    access_token = "sl.BjSFfvfGR2Dn4hNtmKB2h-BGoXydjFVTr9a3U-xBpBlNgXBTZZjWFWWDvdUYWmQXRiTn9E2syS2DOXFhH5UPkOTDk7V5UjdZli5YqqqHRhAKGGBcu7GEx8a2OOjAG2CI9ttWLHC7CP0AV7F3wYyZBgA"

    st.title("Audio Recorder")
    st.write("How to use: Enter a name for the audio file (Make sure u enter unique name every time u start recording), then click 'Start Recording'. When you are done recording, click 'Upload to Dropbox'.")
    st.write("File format is .wav, so make sure to add that to the end of the file name.")
    name = st.text_input("Enter name of file to save audio to: ", placeholder="Ex: output.wav")
    
    if st.button("Start Recording"):
        
        st.write("Recording... Press 'Upload to Dropbox' when done.")
        record_audio(name, duration=5)

    if st.button("Upload to Dropbox"):
        st.write("Uploading to Dropbox...")
        
        upload_to_dropbox(name, access_token)

if __name__ == "__main__":
    main()
