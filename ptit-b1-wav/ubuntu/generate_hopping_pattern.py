import numpy as np

def generate_pattern(num_bits, f_min=2000, f_max=2600, step=10):
    freqs = np.arange(f_min, f_max, step)
    return np.random.choice(freqs, size=num_bits * 2)

if __name__ == "__main__":
    num_bits = int(input("Enter number of bits: "))
    pattern = generate_pattern(num_bits)
    np.savetxt("hopping_pattern.txt", pattern, fmt="%d")
    print("Generated hopping pattern for redundancy mode")

