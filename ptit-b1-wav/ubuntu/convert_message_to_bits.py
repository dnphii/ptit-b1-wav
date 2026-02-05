import os

def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

if __name__ == "__main__":
    if not os.path.exists("message.txt"):
        with open("message.txt", "w") as f:
            f.write("HELLO PTIT!")

    with open("message.txt", "r") as f:
        message = f.read().strip()

    bits = text_to_bits(message)

    with open("message_bits.txt", "w") as f:
        f.write(bits)

    print("Message:", message)
    print("Bits:", len(bits))

