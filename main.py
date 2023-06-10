import numpy as np
import matplotlib.pyplot as plt

def generate_signal(amplitude, frequency, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)

    if window is not None:
        window_func = getattr(np, window)
        signal = signal * window_func(len(t))

    return t, signal

def generate_combined_signal_shift(amplitude1, frequency1, amplitude2, frequency2, duration, shift_ratio, fade_time, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal1 = amplitude1 * np.sin(2 * np.pi * frequency1 * t)
    shift = int(shift_ratio * len(t))
    signal2 = amplitude2 * np.sin(2 * np.pi * frequency2 * (t - shift / sampling_rate))
    fade = np.exp(-t / fade_time)
    combined_signal = signal1 + signal2 * fade

    if window is not None:
        window_func = getattr(np, window)
        combined_signal = combined_signal * window_func(len(t))

    return t, combined_signal

def generate_combined_signal_freq(amplitude1, frequency1, amplitude2, frequency2, duration, frequency_shift, fade_time, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal1 = amplitude1 * np.sin(2 * np.pi * frequency1 * t)
    signal2 = amplitude2 * np.sin(2 * np.pi * (frequency2 + frequency_shift) * t)
    fade = np.exp(-t / fade_time)
    combined_signal = signal1 + signal2 * fade

    if window is not None:
        window_func = getattr(np, window)
        combined_signal = combined_signal * window_func(len(t))

    return t, combined_signal

def plot_time_domain(t, signal, title):
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal)
    plt.xlabel('Czas')
    plt.ylabel('Amplituda')
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_frequency_domain(t, signal, sampling_rate, title):
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sampling_rate)
    spectrum = np.abs(fft)
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, spectrum)
    plt.xlabel('Częstotliwość')
    plt.ylabel('Amplituda')
    plt.title(title)
    plt.grid(True)
    plt.show()

amplitude = 1.0  # Amplitude of the sinusoidal signal
frequency = 1.0  # Frequency of the sinusoidal signal
duration = 1.0  # Duration of the signal in seconds
sampling_rate = 1000.0  # Number of samples per second
window = 'hamming' # Window function for signal sampling (e.g., 'hamming', 'hann', 'blackman')

# Generate and plot the sinusoidal signal
t_sin, signal_sin = generate_signal(amplitude, frequency, duration, sampling_rate)
plot_time_domain(t_sin, signal_sin, 'Sygnał sinusoidalny w dziedzinie czasu')
plot_frequency_domain(t_sin, signal_sin, sampling_rate, 'Sygnał sinusoidalny w dziedzinie częstotliwości')


amplitude2_shift = 0.5  # Amplitude of the second sinusoidal signal with time shift
frequency2_shift = 20.0  # Frequency of the second sinusoidal signal with time shift
shift_ratio = 0.2  # Shift ratio in relation to the duration of the signal
fade_time_shift = 0.5  # Fade time in seconds for the time-shifted signal

# Generate and plot the combined signal with time-shifted sinusoids and fading
t_combined_shift, combined_signal_shift = generate_combined_signal_shift(amplitude, frequency, amplitude2_shift,
                                                                        frequency2_shift, duration, shift_ratio,
                                                                        fade_time_shift, sampling_rate)
plot_time_domain(t_combined_shift, combined_signal_shift, 'Złożenie 2 sygnałów sinusoidalnych (w tym gasnącej sinusoidy) przesuniętych względem siebie o czas')
plot_frequency_domain(t_combined_shift, combined_signal_shift, sampling_rate,
                     'Złożenie 2 sygnałów sinusoidalnych (w tym gasnącej sinusoidy) przesuniętych względem siebie o czas, w dziedzinie częstotliwości')

amplitude2_freq = 0.8  # Amplitude of the second sinusoidal signal with frequency shift
frequency2_freq = 5.0  # Frequency of the second sinusoidal signal with frequency shift
frequency_shift = 15.0  # Frequency shift of the second signal in Hz
fade_time_freq = 0.7  # Fade time in seconds for the frequency-shifted signal

# Generate and plot the combined signal with frequency-shifted sinusoids and fading
t_combined_freq, combined_signal_freq = generate_combined_signal_freq(amplitude, frequency, amplitude2_freq,
                                                                      frequency2_freq, duration, frequency_shift,
                                                                      fade_time_freq, sampling_rate)
plot_time_domain(t_combined_freq, combined_signal_freq, 'Złożenie 2 sygnałów sinusoidalnych (w tym gasnącej sinusoidy) przesuniętych względem siebie o czas i częstotliwość')
plot_frequency_domain(t_combined_freq, combined_signal_freq, sampling_rate,
                     'Złożenie 2 sygnałów sinusoidalnych (w tym gasnącej sinusoidy) przesuniętych względem siebie o czas i częstotliwość, w dziedzinie częstotliwości')
