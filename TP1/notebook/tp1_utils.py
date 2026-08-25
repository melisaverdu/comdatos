import numpy as np
import matplotlib.pyplot as plt


def generate_bits(bit_string):
    """Convierte una cadena de bits en un array de enteros."""
    if not all(bit in "01" for bit in bit_string):
        raise ValueError("La cadena debe contener únicamente 0 y 1.")

    return np.array([int(bit) for bit in bit_string])


def bpsk_symbols(bits):
    """
    Mapea:
        0 -> +1
        1 -> -1

    bits:
        Array de bits 0/1.
    """
    return 1 - 2 * bits


def generate_bpsk_waveform(
    bits,
    fc=10,
    samples_per_symbol=100,
):
    """
    Genera una señal BPSK pasobanda ideal.

    bits:
        Array de bits 0/1.

    fc:
        Frecuencia de la portadora en ciclos por símbolo.

    samples_per_symbol:
        Cantidad de muestras por símbolo.

    Retorna:
        t       -> vector temporal
        signal  -> señal BPSK
        symbols -> símbolos BPSK
    """
    symbols = bpsk_symbols(bits)

    t = np.arange(
        len(bits) * samples_per_symbol
    ) / samples_per_symbol

    symbol_values = np.repeat(symbols, samples_per_symbol)

    carrier = np.sin(2 * np.pi * fc * t)

    signal = symbol_values * carrier

    return t, signal, symbols


def generate_baseband_waveform(
    bits,
    samples_per_symbol=100,
):
    """Genera la señal de banda base NRZ asociada a los bits."""

    symbols = bpsk_symbols(bits)

    t = np.arange(
        len(bits) * samples_per_symbol
    ) / samples_per_symbol

    signal = np.repeat(symbols, samples_per_symbol)

    return t, signal

def plot_bpsk(
    bits,
    t,
    signal,
    samples_per_symbol,
    ax=None,
):
    """Grafica la señal BPSK junto con los límites de símbolo."""

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(t, signal)

    for i in range(len(bits) + 1):
        ax.axvline(
            i,
            linestyle="--",
            linewidth=0.8,
            alpha=0.4,
        )

    ax.set_xlabel("Tiempo [símbolos]")
    ax.set_ylabel("Amplitud")
    ax.set_title(
        f"BPSK para la secuencia {''.join(map(str, bits))}"
    )

    ax.grid(True, alpha=0.25)

    return ax


def compute_fft(signal, samples_per_symbol):
    """Calcula la FFT y devuelve frecuencias y magnitud normalizada."""

    n = len(signal)

    spectrum = np.fft.fftshift(
        np.fft.fft(signal)
    )

    frequencies = np.fft.fftshift(
        np.fft.fftfreq(
            n,
            d=1 / samples_per_symbol
        )
    )

    magnitude = np.abs(spectrum) / n

    return frequencies, magnitude


def plot_spectrum(
    frequencies,
    magnitude,
    ax=None,
):
    """Grafica el espectro de magnitud."""

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(frequencies, magnitude)

    ax.set_xlabel("Frecuencia [ciclos/símbolo]")
    ax.set_ylabel("Magnitud")
    ax.set_title("Espectro de la señal")

    ax.grid(True, alpha=0.25)

    return ax
