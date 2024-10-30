import numpy as np
import matplotlib.pyplot as plt
import wave
import moviepy.editor as moviepy

webmObj = moviepy.VideoFileClip("krenger/52502ff5-6665-4dc5-94ae-b0536038a803.webm")
wavObj = webmObj.write_audiofile("out_audio.wav")
obj = wave.open("krenger/strawberries.wav", "r")
sample_freq  = wavObj.getframerate()
print(sample_freq, "sample freq")
n_samples = wavObj.getnframes()
print(n_samples, "num of samples")
signal_wave = wavObj.readframes(n_samples)
obj.close()

t_audio = n_samples / sample_freq
#t_audio is the time elapsed

print(t_audio)

signal_wave = obj.readframes(n_samples)
signal_array = np.frombuffer(signal_wave, dtype = np.int16)

print(signal_array.shape, "signal array shape")

times = np.linspace(0,n_samples/sample_freq, num = n_samples)

plt.figure(figsize=(15,5))
plt.plot(times, signal_array)
plt.title("audio signal")
plt.xlabel("time (s)")
plt.ylabel("signal array")

plt.show()

