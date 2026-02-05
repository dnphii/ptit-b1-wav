import numpy as np
import soundfile as sf

def embed():
    audio, fs = sf.read("voice-sample.wav", dtype="float32")

    if audio.ndim > 1:
        audio = audio[:, 0]

    with open("message_bits.txt") as f:
        bits = f.read()

    # Nhân đôi bit (redundancy)
    bits = "".join([b*2 for b in bits])

    hopping = np.loadtxt("hopping_pattern.txt").astype(int)

    duration = 0.04
    samples_per_bit = int(fs * duration)
    amp = 0.025

    max_bits = len(audio) // samples_per_bit
    bits = bits[:max_bits]
    hopping = hopping[:len(bits)]

    stego = audio.copy()

    for i, bit in enumerate(bits):
        f = hopping[i] + (60 if bit == "1" else 0)
        t = np.arange(samples_per_bit) / fs
        sig = amp * np.sin(2 * np.pi * f * t)

        start = i * samples_per_bit
        stego[start:start+samples_per_bit] += sig

    sf.write("stego_voice.wav", stego, fs, subtype="PCM_16")
    print("✔ Stego audio created (robust mode)")

if __name__ == "__main__":
    embed()

