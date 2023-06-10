import numpy as np
import matplotlib.pyplot as plt

def generate_signal(amplitude, frequency, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)

    if window is not None:
        window_func = getattr(np, window)
        signal = signal * window_func(len(t))

    return t, signal

def generate_combined_signal_shift(amplitude, frequency, amplitude2, frequency2, duration, shift_ratio, fade_time, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal1 = amplitude * np.sin(2 * np.pi * frequency * t)
    shift = int(shift_ratio * len(t))
    signal2 = amplitude2 * np.sin(2 * np.pi * frequency2 * (t - shift / sampling_rate))
    fade = np.exp(-t / fade_time)
    combined_signal = signal1 + signal2 * fade

    if window is not None:
        window_func = getattr(np, window)
        combined_signal = combined_signal * window_func(len(t))

    return t, combined_signal

def generate_combined_signal_freq(amplitude, frequency, amplitude2, frequency2, duration, shift_ratio, frequency_shift, fade_time, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal1 = amplitude * np.sin(2 * np.pi * frequency * t)
    shift = int(shift_ratio * len(t))
    signal2 = amplitude2 * np.sin(2 * np.pi * (frequency2 + frequency_shift) * (t - shift / sampling_rate))
    fade = np.exp(-t / fade_time)
    combined_signal = signal1 + signal2 * fade

    if window is not None:
        window_func = getattr(np, window)
        combined_signal = combined_signal * window_func(len(t))

    return t, combined_signal


def generate_custom_signal(amplitude, K, duration, t1, t2, n, frequency, phi, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * K * ((t / t1) ** n) / (1 + ((t / t1) ** n)) * np.exp(-t / t2) * np.cos(2 * np.pi * frequency * t + phi)

    return t, signal


def plot_time_frequency_domains(t, signal, sampling_rate, title):
    plt.figure(figsize=(12, 5))

    # Styling
    plt.style.use("seaborn-whitegrid")
    plt.rcParams['font.size'] = 14

    # Plot in the time domain
    plt.subplot(1, 2, 1)
    plt.plot(t, signal, color="#1a0")
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.title('Sygnał w dziedzinie czasu')
    plt.grid(True)

    # Plot in the frequency domain
    plt.subplot(1, 2, 2)
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sampling_rate)
    spectrum = np.abs(fft)
    plt.plot(freqs, spectrum)
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Amplituda')
    plt.title('Spektrum częstotliwościowe')

    plt.tight_layout()
    plt.suptitle(title, fontweight='bold')
    plt.grid(True)
    plt.show()

amplitude = 1.0  # Amplitude of the sinusoidal signal
frequency = 10.0  # Frequency of the sinusoidal signal
duration = 2.0  # Duration of the signal in seconds
sampling_rate = 100.0  # Number of samples per second
window = 'hamming' # Window function for signal sampling (e.g., 'hamming', 'hann', 'blackman')

# Generate and plot the sinusoidal signal
t_sin, signal_sin = generate_signal(amplitude, frequency, duration, sampling_rate)
plot_time_frequency_domains(t_sin, signal_sin, sampling_rate, 'Sygnał sinusoidalny')

amplitude2_shift = 1.0  # Amplitude of the second sinusoidal signal with time shift
frequency2_shift = 20.0  # Frequency of the second sinusoidal signal with time shift
shift_ratio = 0.2  # Shift ratio in relation to the duration of the signal
fade_time_shift = 0.5  # Fade time in seconds for the time-shifted signal

# Generate and plot the combined signal with time-shifted sinusoids and fading
t_combined_shift, combined_signal_shift = generate_combined_signal_shift(amplitude, frequency, amplitude2_shift,
                                                                        frequency2_shift, duration, shift_ratio,
                                                                        fade_time_shift, sampling_rate)
plot_time_frequency_domains(t_combined_shift, combined_signal_shift, sampling_rate,
                            'Złożenie 2 sygnałów sinusoidalnych (czasowe przesunięcie)')

amplitude2_freq = 0.8  # Amplitude of the second sinusoidal signal with frequency shift
frequency2_freq = 5.0  # Frequency of the second sinusoidal signal with frequency shift
frequency_shift = 15.0  # Frequency shift of the second signal in Hz
fade_time_freq = 0.7  # Fade time in seconds for the frequency-shifted signal

# Generate and plot the combined signal with frequency-shifted sinusoids and fading
t_combined_freq, combined_signal_freq = generate_combined_signal_freq(amplitude, frequency, amplitude2_freq,
                                                                      frequency2_freq, duration, shift_ratio, frequency_shift,
                                                                      fade_time_freq, sampling_rate)
plot_time_frequency_domains(t_combined_freq, combined_signal_freq, sampling_rate,
                            'Złożenie 2 sygnałów sinusoidalnych (czasowe i częstotliwościowe przesunięcie)')


K = 1
t1 = 0.5
n = 20
t2 = 0.5
phi = 0

# Generate and plot the custom signal
t_custom, signal = generate_custom_signal(amplitude, K, duration, t1, t2, n, frequency, phi, sampling_rate)
plot_time_frequency_domains(t_custom, signal, sampling_rate, 'Sygnał z Etapu II')
