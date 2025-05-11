import os
import pyperclip
import wave
import time
import threading
import tkinter as tk
import pyaudio

class voiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button=tk.Button(text="🎤︎︎", font=("Arial", 120, "bold"),command=self.click_handler)

        self.button.pack()
        self.label=tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):
        audio=pyaudio.PyAudio()
        stream=audio.open(format=pyaudio.paInt16,channels=1, rate=44100,input=True,frames_per_buffer=1024)
        frames=[]
        start=time.time()

        while self.recording:
            data=stream.read(1024)
            frames.append(data)

            passed=time.time()-start
            secs=passed%60
            mins=passed // 60
            hours = mins// 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i=1
        while exists:
            file_path=f"recording{i}.wav"
            if os.path.exists(file_path):
                i+=1
            else:
                exists=False

        sound_file = wave.open(file_path,"wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

        pyperclip.copy(os.path.abspath(file_path))
        print(f"recording saved to {os.path.abspath(file_path)} (to cipboard)")


voiceRecorder()
