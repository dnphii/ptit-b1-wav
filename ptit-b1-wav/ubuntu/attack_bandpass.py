import soundfile as sf
from scipy.signal import butter, lfilter

def bandstop(low, high, fs, order=8):
    nyq = 0.5 * fs
    return butter(order, [low/nyq, high/nyq], btype="bandstop")

def attack():
    audio, fs = sf.read("stego_voice.wav")

    b, a = bandstop(2000, 2600, fs)
    filtered = lfilter(b, a, audio)

    sf.write("stego_voice_filtered.wav", filtered, fs, subtype="PCM_16")
    print("Created stego_voice_filtered.wav")

if __name__ == "__main__":
    attack()

