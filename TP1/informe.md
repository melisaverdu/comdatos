![](/assets/2_1_Isologotipo_FCEFyN_y_UNC-_blanco_Sin_fondo-Con_bajada.png)

# Trabajo Práctico N.º 1: Comunicaciones 101

**Alumnos**
- García, Lautaro Misael 
- Pastrana Lizárraga, Iván
- Peretti, Federico Ariel
- Renaudo Gaggioli, Valentino
- Verdú, Melisa Noel

## 1. Fundamentos de comunicaciones



## 2. Transmisión de señales digitales



## 3. Modulación de señales digitales

Una señal escalonada, utilizada habitualmente para representar información digital, presenta transiciones abruptas entre sus niveles. Estas transiciones requieren la presencia de componentes de alta frecuencia. En el caso ideal de una onda cuadrada periódica, su representación espectral está compuesta por la frecuencia fundamental y una serie de armónicos impares:

$$
f_0, 3f_0, 5f_0, 7f_0,\ldots
$$

Por lo tanto, esta señal tiene un número infinito de componentes en frecuencia y, en consecuencia, su ancho de banda ideal también es infinito. Sin embargo, la amplitud de los armónicos disminuye a medida que aumenta su frecuencia, por lo que la mayor parte de la energía se concentra en las primeras componentes.

Un sistema de transmisión real no puede transportar un ancho de banda infinito. Tanto los componentes del transmisor y receptor como el propio medio de transmisión actúan como sistemas limitados en frecuencia, por lo que las componentes espectrales que se encuentran fuera de la banda disponible son atenuadas o eliminadas. En consecuencia, la señal recibida ya no conserva la forma escalonada ideal. La eliminación de los armónicos de mayor frecuencia suaviza las transiciones y produce una distorsión de la señal.

Esta limitación resulta especialmente relevante en las comunicaciones inalámbricas, donde el ancho de banda disponible está restringido tanto por las características físicas de los sistemas como por la necesidad de evitar interferencias entre diferentes servicios y usuarios del espectro radioeléctrico. Por este motivo, no resulta viable transmitir directamente todas las componentes espectrales de una señal escalonada.

La distorsión producida por la limitación del ancho de banda no implica necesariamente que la información digital se pierda. Un receptor puede seguir distinguiendo los niveles correspondientes a los bits si se conservan suficientes componentes de la señal. Sin embargo, a medida que se reduce el ancho de banda, las transiciones se vuelven más lentas y la forma de onda se aleja progresivamente de la original, aumentando la posibilidad de errores durante la detección de los símbolos.

Por estas razones, las señales digitales destinadas a transmisión inalámbrica no se transmiten normalmente como señales escalonadas ideales. Se representan mediante señales adaptadas al ancho de banda disponible y, en los sistemas inalámbricos, se emplean técnicas de **modulación** que permiten trasladarla a una banda de frecuencias apropiada para su transmisión.[1]

En síntesis, los principales inconvenientes de transmitir inalámbricamente una señal escalonada son:

* **Ancho de banda idealmente infinito:** la señal contiene una cantidad ilimitada de componentes armónicas.
* **Limitación física del canal:** los sistemas reales solamente permiten transmitir una banda finita de frecuencias.
* **Restricciones del espectro radioeléctrico:** las bandas disponibles para comunicaciones inalámbricas están limitadas para permitir la coexistencia de diferentes sistemas.
* **Distorsión de la señal:** la eliminación de componentes de alta frecuencia modifica principalmente las transiciones de la señal.
* **Posible aumento de errores:** una distorsión excesiva puede dificultar que el receptor determine correctamente los niveles o símbolos transmitidos.

La relación entre estos fenómenos puede analizarse en el dominio de la frecuencia mediante la Transformada Rápida de Fourier (FFT). El análisis permite identificar las componentes armónicas presentes en una señal escalonada y observar cómo la reducción del ancho de banda disponible afecta a su reconstrucción en el dominio temporal.

### Técnica de modulación

![](./assets/tp1-bpsk.png)

La técnica de modulación representada es **BPSK (Binary Phase Shift Keying)**, una técnica de modulación digital por desplazamiento de fase. En BPSK se utilizan dos fases de una señal portadora, separadas $180^\circ$, para representar los dos posibles valores binarios.

En la representación utilizada, cada bit determina la fase de la portadora:

$$
0 \rightarrow 0^\circ
$$

$$
1 \rightarrow 180^\circ
$$

Por lo tanto, un cambio de bit produce una inversión de la fase de la señal modulada.

### Modulación de una secuencia

Para la secuencia de ejemplo

$$
01110110
$$

cada bit se representa mediante una de las dos fases disponibles. Utilizando el mapeo antes visto, se obtiene:

$$
0^\circ,180^\circ,180^\circ,180^\circ,0^\circ,180^\circ,180^\circ,0^\circ
$$

La señal resultante consiste en segmentos de la onda portadora que mantienen una fase constante durante cada intervalo de símbolo. Cuando cambia el valor del bit, la fase de la portadora se desplaza $180^\circ$, produciendo una inversión de la onda.

![Modulación BPSK de la secuencia 01110110](./assets/tp1-bpsk_01110110.png)

La representación fue generada mediante una simulación en Python, utilizando una portadora senoidal y aplicando el desplazamiento de fase correspondiente a cada bit.

### Otras técnicas basadas en el mismo principio

Interpretando la consigna como una referencia a las técnicas basadas en **desplazamiento de fase (PSK)**, BPSK constituye el caso de dos fases posibles. A partir del mismo principio pueden utilizarse más estados de fase, dando lugar a técnicas de modulación $M$-PSK, entre las que se encuentran **QPSK (4-PSK)** y **8-PSK**.

Al aumentar la cantidad de fases disponibles, cada símbolo puede representar una mayor cantidad de bits. En general:

$$
\text{bits por símbolo}=\log_2(M)
$$

donde $M$ es la cantidad de estados de fase.

Por ejemplo, BPSK utiliza dos fases y transmite un bit por símbolo, mientras que QPSK utiliza cuatro fases y transmite dos bits por símbolo.

### Bit Error Rate (BER)

El **Bit Error Rate** es una medida de la cantidad de bits recibidos incorrectamente respecto de la cantidad total de bits transmitidos:

$$
BER=\frac{N_{\text{bits erróneos}}}{N_{\text{bits transmitidos}}}
$$

Por ejemplo, un BER de $10^{-4}$ significa que, en promedio, se produce un error por cada $10^4$ bits transmitidos.

En términos de BER, entre las modulaciones PSK consideradas, **BPSK presenta las mejores prestaciones**, bajo iguales condiciones de potencia y ruido. Esto puede explicarse mediante su constelación: sus dos símbolos se encuentran separados por $180^\circ$, por lo que están lo más alejados posible entre sí para una constelación PSK de amplitud determinada.

Al aumentar $M$ en una modulación $M$-PSK, los símbolos deben distribuirse entre más fases dentro de la misma circunferencia. Por lo tanto, la distancia entre símbolos vecinos disminuye, haciendo que sea más difícil distinguirlos en presencia de ruido y aumentando la probabilidad de error para una misma relación señal/ruido.

Existe, por lo tanto, un compromiso entre **eficiencia espectral** y **prestaciones frente al ruido**: aumentar el número de fases permite transmitir más bits por símbolo, pero reduce la separación entre los símbolos y, en consecuencia, empeora el BER bajo las mismas condisiones de comparación.

### Referencia utilizada

**[1]** William Stallings, *Comunicaciones y redes de computadores*, 7.ª edición, capítulo 3 **“Transmisión de datos”**.

## 4. Implementación en Packet Tracer



## 5. Conclusiones



## Referencias
