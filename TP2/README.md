## Interpretación de la figura

Analizando la figura se ve una antena de transmisión que emite una señal senoidal limpia, que se distorsiona por un momento al pasar cerca de una persona operando con una herramienta y luego vuelve a viajar al celular.

---

### A) Fenómeno físico representado y sus características

Aparece **interferencia (ruido electromagnético)**: una alteración o degradación de una señal de comunicación producida por la superposición de otra señal no deseada (ruido) proveniente de una fuente externa, en este caso, una herramienta de tipo industrial.

**Características principales:**

1. **Superposición de señales**: la señal útil (senoidal limpia) se suma a una señal no deseada, deformando la forma de onda original.
2. **Origen externo**: proviene de una fuente distinta al transmisor y al receptor.
3. **Degrada la calidad de la señal**: dificulta que el receptor interprete correctamente la información original.
4. **Afecta la relación señal-ruido (SNR)**, aumentando la probabilidad de errores en la recepción..

---

### B) Bandas de transmisión y resiliencia a la interferencia

Este fenómeno afecta principalmente a las **frecuencias bajas**, ya que suelen ser más susceptibles a interferencia de origen industrial/eléctrico, porque muchas máquinas y motores generan ruido electromagnético justamente en esos rangos. También afecta a las **transmisiones inalámbricas de corto alcance en bandas ISM compartidas**, vulnerables porque muchos dispositivos comparten esa misma banda (Bluetooth, Wi-Fi, etc.).

**¿Cuáles son más resilientes?**

1. La **fibra óptica** es prácticamente inmune a la interferencia electromagnética, debido a que transmite luz y no señales eléctricas.
2. Las transmisiones en **frecuencias más altas** con mayor ancho de banda dedicado (como enlaces de microondas dedicados o 5G en bandas milimétricas) suelen tener mejor inmunidad relativa si están bien planificadas, aunque son más sensibles a obstáculos físicos.

---

### C) ¿Qué es la SNR? ¿Tiene algo que ver con el concepto BER del TP1?

La **SNR (Signal-to-Noise Ratio)** es la relación entre la potencia de la señal útil y la potencia del ruido presente en el canal de comunicación. Se expresa en decibeles (dB):

$$
SNR_{dB} = 10 \log_{10}\left(\frac{P_{signal}}{P_{noise}}\right)
$$

El **BER** y la **SNR** están relacionados: el BER mide la proporción de bits transmitidos. A menor SNR, el receptor tiene más dificultad para distinguir correctamente los símbolos/bits transmitidos, y por consecuencia, aumenta el BER. Ocurre lo contrario a mayor SNR.