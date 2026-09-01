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

La sincronizacion es el proceso mediante el cual el emisor y el receptor coordinan el tiempo para que el receptor sepa exactamente cuanod muestrar la señal entrante e interpretar correctamente la informacion digital enviada

* **Sincronizacion a nivel de bit** Permite al receptor determinar la velocidad de transmision y el instante exacto en el que empieza y termina un bit individual. Garantiza que el receptor lea la señal en el momento preciso para interpretar correctamente si es un 0 o un 1 digital

* **Sincronizacion de trama** Identifica donde empieza y termina un bloque completo de datos(trama) dentro de un flujo de bits ya sincronizados utilizando secuencias o patrones especiales de bits que delimitan el inicio y final de una estructura de datos

### Anatomía de una Trama: Encabezado, Carga Útil y Tráiler

Una trama es una unidad de datos estructurada que se transmite a nivel de la capa de enlace . Agrupa los datos del usuario junto con informacion de control para permitir una transmision confiable y ordenada sobre un medio fisico

* **Encabezado (Header)**, se ubica al inicio de la trama y contiene datos de control para el transporte y entrega como direcciones fisicas de origen y destino, tipo de protocolo, secuencia de paquete y bytes de sincronizacion

* **Carga Util (Payload)**, es el bloque central que contiene los datos que se desean transmitir

* **Trailer**, se encuentra en el final de la trama y contiene informacion de verificacion y cierre, como algoritmos de deteccion de errores o de correccion para los mismos.

### Función y Relevancia del Preámbulo en la Transmisión

El preambulo es una secuencia especifica de bits que se transmite inmediatamente antes de la trama propiamente dicha

Permite al receptor sincronizar su reloj con el del emisor antes de que lleguen datos reales. Consiste en un patron alternado (1010101 por ejemplo) que ayuda al receptor a captar la frecuencia de muestreo y detectar el momento en que la trama inicia

No necesariamente es parte de la informacion util que se quiere transmitir ya que este es un sobrecosto del nivel fisico/enlace que se utiliza unicamente para la sincronizacion del hardware, una vez sincronizado, el receptor descarta el preambulo

### Métodos para la Delimitación de Tramas en Protocolos de Enlace

1. **Tramas de longitud fija:** El receptor cuenta un numero fijo de bits o bytes a partir del delimitador de inicio. Una vez alcanzada esa cantidad exacta, se sabe que la trama actual a finalizado y que la siguiente secuencia correspondera a una nueva trama o estara en estado de inactividad

2. **Campo de longitud en el encabezado:** El encabezado de la trama incluye un campo numerico que especifica el tamaño total de la trama o de la carga util en bytes
Cuando el receptor recibe este encabezado, lee el valor numerico y configura un contador. A medida que procesa el flujo de datos entrante, decrementa el contador hasta llegar a cero, lo que señala el final preciso de la trama

3. **Caracteres o secuencias delimitadoras:** Consiste en utilizar patrones o secuencias de caracteres/bits especificos para marcar el inicio y el fin de la trama. El receptor monitorea continuamente el flujo de bits buscando el delimitador de cierre.
Para evitar que la secuencia se confunda si aparece de manera natural dentro de los datos transmitidos, se utilizan tecnicas como el relleno de bits(bit stuffing) o el relleno de caracteres(byte stuffing), garantizando que el receptor identifique el patron solo cuando actua como delimitador real.
---

## Procesamiento, Extracción y Reconstrucción de Tramas Binarias

### Formato de Trama y Extracción de la Carga Útil del Grupo

### Reensamblado Secuencial y Reconstrucción del Mensaje Global
