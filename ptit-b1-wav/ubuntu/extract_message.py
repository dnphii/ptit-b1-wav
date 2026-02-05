import numpy as np
import soundfile as sf

def goertzel(samples, fs, freq):
    k = int(0.5 + (len(samples) * freq) / fs)
    w = (2 * np.pi / len(samples)) * k
    cosine = np.cos(w)
    sine = np.sin(w)
    coeff = 2 * cosine

    q0 = q1 = q2 = 0
    for s in samples:
        q0 = coeff * q1 - q2 + s
        q2 = q1
        q1 = q0

    real = q1 - q2 * cosine
    imag = q2 * sine
    return real**2 + imag**2

def bits_to_text(bits):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7)//8, "big").decode(errors="ignore")

def extract(filename):
    audio, fs = sf.read(filename)

    if audio.ndim > 1:
        audio = audio[:, 0]

    hopping = np.loadtxt("hopping_pattern.txt").astype(int)
    samples_per_bit = int(fs * 0.04)

    raw_bits = ""

    for i, f in enumerate(hopping):
        start = i * samples_per_bit
        segment = audio[start:start+samples_per_bit]

        if len(segment) < samples_per_bit:
            break

        e0 = goertzel(segment, fs, f)
        e1 = goertzel(segment, fs, f + 60)

        raw_bits += "1" if e1 > e0 else "0"

    # Majority voting (2 bit → 1 bit)
    bits = ""
    for i in range(0, len(raw_bits)-1, 2):
        bits += "1" if raw_bits[i:i+2].count("1") >= 1 else "0"

    print("Recovered bits:", bits)
    print("Message:", bits_to_text(bits))

if __name__ == "__main__":
    extract("stego_voice.wav")

