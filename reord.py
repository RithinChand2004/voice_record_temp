import streamlit as st
from scipy.io.wavfile import write
import wavio as wv
import sounddevice as sd
#import wave
import dropbox
import os

def record_audio(filename, duration=5):
    fs = 44100  # Sample rate
    seconds = duration  # Duration of recording
    
    # devices = sd.query_devices()
    # for i, device in enumerate(devices):
    #     print(i, device['name'])

    # input_device_index = 0  # Replace with the index of your desired input device
    # audio_data = sd.rec(int(fs * seconds), samplerate=fs, channels=2, device=input_device_index)


    st.write("Recording...")
    audio_data = sd.rec(int(fs * seconds), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished

    # with wave.open(filename, "wb") as wf:
    #     wf.setnchannels(2)
    #     wf.setsampwidth(2)
    #     wf.setframerate(fs)
    #     wf.writeframes(audio_data.tobytes())
    
    # This will convert the NumPy array to an audio
	# file with the given sampling frequency
    write(filename, fs, audio_data)

	# Convert the NumPy array to audio file
    wv.write(filename, audio_data, fs, sampwidth=2)
    st.write("Finished recording")

    

def upload_to_dropbox(filename, access_token, dropbox_folder="/Audio_Recordings/"):
    dbx = dropbox.Dropbox(access_token)

    with open(filename, "rb") as f:
        audio_data = f.read()

    try:
        dbx.files_upload(audio_data, dropbox_folder + os.path.basename(filename))
        st.write("Audio uploaded to Dropbox successfully.")
    except dropbox.exceptions.ApiError as e:
        st.write(f"Error uploading audio to Dropbox: {e}")

# def main():
#     st.title("Audio Recorder and Uploader")
#     st.write("Click the 'Record' button to start recording audio for 5 seconds.")
    
#     if st.button("Record"):
#         record_audio("output.wav", duration=5)

#     if st.button("Stop Recording"):
#         st.write("Stopped Recording")
#         upload_to_dropbox("output.wav", "YOUR_DROPBOX_ACCESS_TOKEN")

def main():
    # ... Code for the Streamlit app from the previous example ...
    access_token = "sl.BjUcmiCTA_UCfCfV2dj1p-n3brEk6ekA1Qf9jHjD3yLmK6NqaguX8z2YqCBu8BJvQXQ3pwkSGYqHVLdx86dH0urpELjcFrKH1DoRNvNe14la1W2VgP-6ltwcReSlJ3xgOREfJ_CuzJ5QMF5igm-Se2c"

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
