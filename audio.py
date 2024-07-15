import sounddevice as sd
import wave
import numpy as np
import threading

class VoiceRecorder:
    def __init__(self, filename, samplerate=44100, channels=1, dtype='int16'):
        self.filename = filename
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.recording = False
        self.frames = []

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record)
        self.thread.start()
        print("Recording started...")

    def stop_recording(self):
        self.recording = False
        self.thread.join()
        self._save_wave_file()
        print("Recording stopped and saved to", self.filename)

    def _record(self):
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=self._callback):
            while self.recording:
                sd.sleep(100)

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, flush=True)
        if self.recording:
            self.frames.append(indata.copy())

    def _save_wave_file(self):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(np.dtype(self.dtype).itemsize)
        wf.setframerate(self.samplerate)
        wf.writeframes(b''.join(self.frames))
        wf.close()