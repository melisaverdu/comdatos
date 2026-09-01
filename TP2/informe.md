![](/assets/2_1_Isologotipo_FCEFyN_y_UNC-_blanco_Sin_fondo-Con_bajada.png)

# Trabajo Práctico N.º 2: Capa Física y Capa de Enlace de Datos

**Alumnos**
- García, Lautaro Misael 
- Pastrana Lizárraga, Iván
- Peretti, Federico Ariel
- Renaudo Gaggioli, Valentino
- Verdú, Melisa Noel

---

## Fenómenos de Propagación y Movilidad en Enlaces Inalámbricos

![Corrimiento Doppler en comunicaciones móviles](./assets/figura_propagacion.png)

### Efecto Doppler y Corrimiento Frecuencial en Comunicaciones Móviles

### Sensibilidad y Resiliencia según Bandas del Espectro y Modulaciones

### Desplazamiento a Alta Velocidad e Interferencia en Aeronaves Comerciales

---

## Degradación de Señal, Ruido e Interferencia en el Canal

![Ruido e interferencia electromagnética](./assets/figura_interferencia.png)

### Ruido Impulsivo e Interferencia Electromagnética

### Vulnerabilidad y Robustez en Distintos Medios de Transmisión

### Relación Señal a Ruido (SNR) y su Relación con la Tasa de Error de Bits (BER)

---

## Estrategias Digitales de Detección, Corrección y Compensación Frecuencial

### Detección y Corrección de Errores Inducidos por Ruido en el Canal
Los sistemas de transmisión digital no pueden evitar las perturbaciones causadas por el ruido en el canal físico, pero sí pueden detectar y, en algunos casos, corregir los errores mediante la incorporación de información redundante a los datos transmitidos.

* **Detección de Errores:** Se basa en añadir información redundante a los datos originales antes de ser transmitidos. El receptor compara el resultado con la redundancia adjunta. Si no coinciden, se detecta la presencia de errores causados por el ruido.
  * *Métodos habituales:* Bit de paridad, Suma de comprobación (*Checksum*) y Chequeo de Redundancia Cíclica (*CRC*).

* **Corrección de Errores:** Una vez detectada la alteración de los datos, los sistemas emplean dos mecanismos principales para subsanarla:
  * **ARQ (*Automatic Repeat Request*):** Es una estrategia por retransmisión. Cuando el receptor detecta un error, solicita al emisor la retransmisión de los datos afectados.
  * **FEC (*Forward Error Correction*):** Se agregan bits de redundancia suficientes para que el receptor pueda detectar y corregir determinados errores directamente, sin necesidad de retransmisión.

### Compensación de Variaciones de Frecuencia y Control de Fase
En los canales digitales, la frecuencia de la señal recibida puede variar debido a imperfecciones térmicas o inestabilidades en los osciladores locales, así como por el efecto Doppler derivado del movimiento relativo entre el emisor y el receptor. Para mantener la sincronía, se utilizan los siguientes mecanismos de compensación:

* **Lazos de Seguimiento de Fase y Frecuencia (PLL / FLL):** Son circuitos o algoritmos digitales en el receptor que monitorean de forma continua la señal entrante y ajustan la fase y frecuencia del oscilador local para mantenerse "enganchados" exactamente a la frecuencia de la portadora recibida.
* **Símbolos Piloto (*Pilot Signals* / *Training Sequences*):** Consisten en la inserción periódica de patrones de datos previamente conocidos por el receptor dentro del flujo de información. Al comparar los símbolos recibidos con el patrón ideal esperado, el sistema puede estimar con alta precisión el desplazamiento de frecuencia (*frequency offset*) y aplicar correcciones digitales mediante ecualizadores.
---

## Sincronización, Estructura y Delimitación en la Capa de Enlace

### Sincronización a Nivel de Bit y Sincronización de Trama

### Anatomía de una Trama: Encabezado, Carga Útil y Tráiler

### Función y Relevancia del Preámbulo en la Transmisión

### Métodos para la Delimitación de Tramas en Protocolos de Enlace

---

## Procesamiento, Extracción y Reconstrucción de Tramas Binarias

### Formato de Trama y Extracción de la Carga Útil del Grupo

### Reensamblado Secuencial y Reconstrucción del Mensaje Global
