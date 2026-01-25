import wave
import math
import random
import struct
import os

SAMPLE_RATE = 44100

def write_wav(filename, data):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data)

def generate_square_wave(freq, duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    data = bytearray()
    period = SAMPLE_RATE / freq
    for i in range(n_samples):
        value = 32767 if (i % period) < (period / 2) else -32767
        data += struct.pack('<h', int(value * volume))
    return data

def generate_noise(duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    data = bytearray()
    for i in range(n_samples):
        value = random.randint(-32767, 32767)
        data += struct.pack('<h', int(value * volume))
    return data

def generate_sweep(start_freq, end_freq, duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    data = bytearray()
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Linear freq ramp
        current_freq = start_freq + (end_freq - start_freq) * (i / n_samples)
        phase = 2 * math.pi * current_freq * t
        # Use square wave logic with variable period for retro feel, or sine
        # Let's do a simple sine for sweep, or square
        # Square sweep:
        period = SAMPLE_RATE / current_freq
        value = 32767 if (i % period) < (period / 2) else -32767
        data += struct.pack('<h', int(value * volume))
    return data

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def main():
    ensure_dir("assets/sounds")
    
    # 1. Shoot (High to low sweep)
    print("Generating shoot.wav...")
    data = generate_sweep(880, 110, 0.15, 0.3)
    write_wav("assets/sounds/shoot.wav", data)
    
    # 2. Explosion (Noise)
    print("Generating explosion.wav...")
    data = generate_noise(0.4, 0.4)
    write_wav("assets/sounds/explosion.wav", data)
    
    # 3. Jump (Low to high sweep)
    print("Generating jump.wav...")
    data = generate_sweep(150, 400, 0.2, 0.3)
    write_wav("assets/sounds/jump.wav", data)
    
    # 4. Collect (High ding)
    print("Generating collect.wav...")
    data = generate_square_wave(1200, 0.1, 0.3) + generate_square_wave(1600, 0.1, 0.3)
    write_wav("assets/sounds/collect.wav", data)
    
    # 5. Select (Blip)
    print("Generating select.wav...")
    data = generate_square_wave(600, 0.05, 0.3)
    write_wav("assets/sounds/select.wav", data)

    print("Done!")

if __name__ == "__main__":
    main()
