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

<p align="center">
  <img src="./assets/figura_propagacion.png" alt="Corrimiento Doppler en comunicaciones móviles" width="60%" />
</p>

### Efecto Doppler y Corrimiento Frecuencial en Comunicaciones Móviles

El fenómeno físico representado en la figura corresponde al **Efecto Doppler** (o corrimiento Doppler) en comunicaciones inalámbricas y satelitales. Este efecto describe el cambio aparente en la frecuencia y en la longitud de onda recibidas debido a la existencia de velocidad relativa entre la fuente transmisora y el receptor a lo largo de la línea de vista.

Cuando el emisor y el receptor reducen su distancia relativa (aproximación), cada frente de onda sucesivo se emite desde una posición más cercana que el anterior, provocando una compresión espacial de la longitud de onda y un consecuente incremento en la frecuencia percibida por el receptor ($f_{\text{recibida}} > f_{\text{transmitida}}$). Por el contrario, cuando se incrementa la distancia (alejamiento), los frentes de onda se dilatan en el medio, reduciendo la frecuencia recibida. En el gráfico se observa cómo los frentes de onda llegan progresivamente más próximos entre sí al receptor durante la aproximación, representando el incremento de la frecuencia recibida.

La relación fundamental para el cálculo de la frecuencia percibida y del desplazamiento Doppler ($\Delta f_d$) se modela analíticamente como:

$$
f_{\text{recibida}} = f_{\text{transmitida}} \cdot \left(1 + \frac{v_r}{c}\right) \implies \Delta f_d = f_c \cdot \frac{v_r}{c} = f_c \cdot \frac{v}{c} \cdot \cos(\theta)
$$

donde:
- $f_c$ es la frecuencia portadora nominal emitida.
- $v_r$ es la componente de velocidad radial relativa proyectada sobre la línea de vista directa (*Line-of-Sight*, LOS) entre el transmisor y el receptor.
- $v$ es la velocidad relativa total y $\theta$ es el ángulo entre el vector de movimiento y el enlace visual.
- $c$ es la velocidad de propagación de la luz en el vacío ($3 \times 10^8\text{ m/s}$).

Este fenómeno constituye la principal restricción de diseño de radiofrecuencia en sistemas de satélites de órbita terrestre baja (**LEO**, *Low Earth Orbit*), como Starlink, OneWeb o Kuiper, donde los vehículos orbitan a altitudes de $500\text{ a }1200\text{ km}$ a velocidades del orden de $7,5\text{ a }7,8\text{ km/s}$ ($\approx 27.000\text{ km/h}$). Durante el paso orbital de un satélite LEO (que dura apenas entre 5 y 10 minutos), la velocidad radial traza una **curva en S**: es máxima positiva al asomar en el horizonte (acercamiento), se anula momentáneamente en el cenit o punto de máxima elevación (movimiento puramente transversal) y pasa a ser máxima negativa al ocultarse en el horizonte. En transmisiones en **banda Ka** ($20\text{ GHz}$), este comportamiento induce desviaciones de hasta $\pm 500\text{ kHz}$ con una excursión de frecuencia total de hasta $1\text{ MHz}$ a lo largo de un solo pase, con tasas de variación (*Doppler drift rate*) de hasta $40\text{ kHz/s}$, lo que descalibra severamente los circuitos de recuperación de portadora (*Carrier Frequency Offset*, CFO) y altera el sincronismo temporal de los símbolos en hasta $\pm 25\text{ ppm}$ ($\pm 2.500\text{ símbolos/s}$ para una tasa de $100\text{ Msym/s}$).[1]

### Sensibilidad y Resiliencia según Bandas del Espectro y Modulaciones

Debido a que el desplazamiento Doppler absoluto ($\Delta f_d$) es estrictamente proporcional a la frecuencia de la portadora ($f_c$), el impacto técnico se distribuye desigualmente según la banda espectral y la arquitectura orbital:

- **Bandas de mayor sensibilidad (menor resiliencia):** Las frecuencias elevadas de microondas y ondas milimétricas en las bandas **SHF** y **EHF** sufren las mayores variaciones absolutas. En enlaces de banda **Ka** ($20\text{ GHz}$), el corrimiento alcanza $\pm 500\text{ kHz}$; en banda **Ku** ($12\text{ GHz}$), ronda los $\pm 300\text{ kHz}$ ($\approx 60\%$ del valor en Ka). Estas magnitudes exceden ampliamente el ancho de captura de demoduladores satelitales convencionales (como DVB-S2X), demandan bandas de guarda mayores (de hasta $1\text{ MHz}$) para evitar el solapamiento de canales adyacentes y destruyen la ortogonalidad en esquemas multiportadora como OFDM debido a la interferencia entre subportadoras (ICI).
- **Bandas de mayor resiliencia:** En la banda **L** ($1,5\text{ GHz}$, utilizada en servicios móviles satelitales tradicionales como Inmarsat o Iridium para voz), el corrimiento máximo se reduce a sólo $\approx \pm 37,5\text{ kHz}$ ($7,5\%$ del valor en Ka). En bandas más bajas (**HF**, **VHF** y **UHF** baja, de $3\text{ a }300\text{ MHz}$), los corrimientos se limitan a unos pocos hercios o centenas de hercios, resultando despreciables para los anchos de canal estándar.
- **Satélites Geoestacionarios (GEO):** Al orbitar a $35.786\text{ km}$ en sincronismo con la rotación terrestre, su velocidad radial relativa con terminales terrestres proviene únicamente de imperfecciones de mantenimiento de posición (*station-keeping*, $\pm 0,05^\circ$), resultando en velocidades relativas de apenas $\sim 1\text{ m/s}$ y desviaciones Doppler marginales de $\pm 40\text{ a }\pm 67\text{ Hz}$ en bandas Ku/Ka, las cuales son absorbidas sin dificultad por los bucles de enganche de fase estándar.

Para mitigar el efecto en constelaciones LEO modernas, se implementa una arquitectura híbrida:
  1. **Compensación en lazo abierto (*Open-Loop*):** El transmisor precorrige su frecuencia calculando la trayectoria del satélite a partir de datos de efemérides orbitales y posición GPS, reduciendo el error residual a menos de $1\text{ kHz}$.
  2. **Seguimiento en lazo cerrado (*Closed-Loop*):** El receptor rastrea y elimina en tiempo real la desviación residual mediante lazos de control automático de frecuencia (**AFC**) y lazos de enganche de fase (**PLL**).[1]

### Desplazamiento a Alta Velocidad e Interferencia en Aeronaves Comerciales

La restricción que prohíbe el uso activo de telefonía celular comercial a bordo de aeronaves en vuelo responde a dos factores electromagnéticos y de ingeniería de redes:

1. **Interferencia electromagnética (EMI) en la aviónica de a bordo:** En determinadas condiciones de vuelo, especialmente cuando el terminal se encuentra lejos de las estaciones base terrestres, puede incrementar su potencia de transmisión para mantener el enlace. Las emisiones simultáneas de múltiples dispositivos pueden aumentar el riesgo de interferencias electromagnéticas con los sistemas de comunicaciones, navegación y otros equipos electrónicos de la aeronave. Por este motivo, las transmisiones de los dispositivos móviles se encuentran sujetas a restricciones durante determinadas fases del vuelo.
2. **Efecto Doppler cinemático y saturación de la red terrestre:** A velocidades de crucero comercial ($\approx 800\text{ a }900\text{ km/h} = 250\text{ m/s}$), el movimiento del avión aporta un corrimiento Doppler adicional propio de hasta $\pm 1,7\text{ kHz}$ en frecuencias de microondas. Además, la altitud de vuelo otorga al móvil una línea de vista directa (LOS) sin obstáculos con decenas de estaciones base terrestres al mismo tiempo. La alta velocidad de desplazamiento genera una tasa crítica de intentos de traspaso de celda (**hand-overs**) entre múltiples torres por minuto y desalineaciones de sincronismo frecuencial, provocando la congestión y sobrecarga del plano de control y señalización de la red celular terrestre, degradando el servicio para los usuarios en tierra.

---

## Degradación de Señal, Ruido e Interferencia en el Canal

<p align="center">
  <img src="./assets/figura_interferencia.png" alt="Ruido e interferencia electromagnética" width="60%" />
</p>

Analizando la figura provista, se observa una antena de transmisión que emite una señal senoidal pura y limpia, la cual se distorsiona transitoriamente al propagarse en las inmediaciones de una persona operando una herramienta electromecánica (un taladro eléctrico) y luego continúa su viaje hacia el teléfono celular receptor.

### Ruido Impulsivo e Interferencia Electromagnética

El fenómeno físico representado en la figura corresponde a la **Interferencia Electromagnética (EMI)** y al **Ruido**, específicamente al **Ruido Impulsivo** (*Impulse Noise*) de origen artificial (*man-made noise*).

El ruido se define como toda señal electromagnética no deseada proveniente de fuentes externas y ajenas al transmisor que se suma, combina y deforma la señal útil durante su propagación en el medio, dificultando o impidiendo que el receptor interprete correctamente la información original.

#### Características Principales:
1. **Superposición de Señales:** La señal portadora útil (senoidal limpia) se suma aditivamente a la energía de la señal espuria no deseada, distorsionando y deformando la forma de onda original.
2. **Origen Externo y Artificial:** Proviene de una fuente desacoplada e independiente tanto del emisor como del receptor. En este caso, el motor eléctrico del taladro genera chispas y arcos en sus escobillas de conmutación, produciendo transitorios de radiofrecuencia (RF) de alta energía que se radian al entorno.
3. **Naturaleza Discontinua e Impulsiva:** A diferencia del ruido térmico continuo, el ruido impulsivo está compuesto por pulsos o picos transitorios irregulares de muy corta duración (microsegundos) pero de **gran amplitud**. En comunicaciones digitales de datos, constituye la fuente primordial de errores en ráfaga (*burst errors*), corrompiendo bloques completos de bits adyacentes.
4. **Degradación de la Calidad y de la SNR:** La inserción de energía espuria reduce la relación señal a ruido (SNR) en el receptor, incrementando significativamente la probabilidad de error en la demodulación.

En el marco general de las comunicaciones, se distinguen cuatro tipos principales de ruido:
- **Ruido Térmico (Ruido Blanco):** Ineludible y permanente en cualquier conductor o dispositivo electrónico debido a la agitación térmica de los electrones. Posee una densidad espectral uniforme en todas las frecuencias y fija el límite teórico superior de prestaciones del canal.
- **Ruido de Intermodulación:** Aparece cuando señales de diferentes frecuencias comparten un mismo medio que presenta no linealidades, produciendo armónicos a frecuencias suma y diferencia.
- **Diafonía (*Crosstalk*):** Acoplamiento inductivo o capacitivo no deseado entre líneas de transmisión adyacentes (típico en pares trenzados de cobre contiguos).
- **Ruido Impulsivo:** Perturbaciones transitorias de gran amplitud producidas por conmutaciones eléctricas, motores o maquinaria industrial.

### Vulnerabilidad y Robustez en Distintos Medios de Transmisión

La susceptibilidad frente a las interferencias electromagnéticas y al ruido varía ampliamente según la banda del espectro y el medio físico empleado:

#### Susceptibilidad según las Bandas de Frecuencia:
- **Frecuencias Bajas y Medias (más afectadas):** Las bandas inferiores (desde VLF y LF hasta HF y el umbral bajo de VHF, típicamente por debajo de los $100\text{ MHz}$) son las más susceptibles a la interferencia de origen industrial y eléctrico, ya que la mayor parte de las máquinas, motores y redes de distribución eléctrica ($50\text{--}60\text{ Hz}$) concentran su emisión de ruido electromagnético en estos rangos.
- **Bandas ISM Compartidas (2,4 GHz):** Las transmisiones inalámbricas de corto alcance que operan en bandas no licenciadas (como Wi-Fi y Bluetooth en $2,4\text{ GHz}$) son sumamente vulnerables debido a la congestión de múltiples dispositivos heterogéneos compartiendo y emitiendo simultáneamente en el mismo espectro.
- **Frecuencias Altas (más resilientes):** Las bandas superiores (**UHF**, **SHF** y ondas milimétricas, como enlaces de microondas dedicados o 5G) poseen mayor inmunidad relativa frente al ruido impulsivo eléctrico industrial, dado que la energía de estas perturbaciones decae fuertemente con la frecuencia. No obstante, son más sensibles a obstáculos físicos (paredes, lluvia) y su factor limitante dominante pasa a ser el **ruido térmico** acumulado ante la mayor pérdida de trayectoria.

#### Susceptibilidad según los Medios Físicos de Transmisión:
1. **Medio Inalámbrico (Menor Resiliencia):** Es el medio más expuesto y vulnerable. Al propagarse en un canal abierto y compartido sin confinamiento ni blindaje físico, las perturbaciones externas y las interferencias se acoplan y superponen directamente sobre la portadora útil.
2. **Cable Coaxial (Mayor Resiliencia):** Presenta una elevada protección frente a interferencias gracias a su blindaje conductor exterior continuo (malla metálica a tierra), el cual actúa como una jaula de Faraday bloqueando y derivando las corrientes inducidas por campos electromagnéticos externos.
3. **Fibra Óptica (Inmunidad Absoluta / Máxima Resiliencia):** Es **100% inmune** a la interferencia electromagnética (EMI), al ruido impulsivo y a la diafonía. Debido a que transmite información mediante pulsos de luz (fotones) confinados en un núcleo de vidrio de sílice dieléctrico, no experimenta interacción física con campos electromagnéticos, posicionándose como el medio más seguro y robusto en entornos industriales severamente ruidosos.

### Relación Señal a Ruido (SNR) y su Relación con la Tasa de Error de Bits (BER)

#### Definición de SNR:
La **Relación Señal a Ruido** (*Signal-to-Noise Ratio*, SNR o S/N) es la relación cuantitativa entre la potencia media de la señal útil ($P_{\text{señal}}$ o $S$) y la potencia media del ruido ($P_{\text{ruido}}$ o $N$) en un punto del enlace (medido habitualmente a la entrada del receptor). Se expresa en escala logarítmica de **decibelios (dB)**:

$$
\text{SNR}_{\text{dB}} = 10 \cdot \log_{10}\left(\frac{P_{\text{señal}}}{P_{\text{ruido}}}\right)
$$

Una SNR alta indica una señal nítida donde la potencia útil predomina ampliamente sobre el ruido, mientras que una SNR baja refleja una señal degradada, débil y sepultada por la interferencia.

#### Relación con el BER (Bit Error Rate):
El **BER** (*Bit Error Rate*) —concepto analizado en el TP1— mide la proporción de bits recibidos con error respecto del total de bits transmitidos:

$$
\text{BER} = \frac{N_{\text{bits erróneos}}}{N_{\text{bits transmitidos}}}
$$

La **SNR** y el **BER** guardan una **relación estrictamente inversa y exponencial** en los sistemas de comunicaciones digitales:

1. **Comportamiento Inverso Exponencial:** A medida que la **SNR aumenta**, el **BER disminuye exponencialmente**. Con una SNR elevada, la distancia entre los estados lógicos de la constelación permite que la circuitería del receptor decodifique y discrimine con precisión los símbolos ('0' o '1') en el instante de muestreo.
2. **Efecto de una SNR Reducida:** Si la SNR disminuye, los picos de ruido se vuelven comparables a la amplitud de la señal útil, superando los umbrales de decisión durante el muestreo temporal. Esto provoca que el receptor interprete un '0' como un '1' (o viceversa), disparando la tasa de errores de bit (BER).
3. **Límite de Capacidad de Shannon y Selección de Modulaciones:** De acuerdo con el teorema de capacidad de Shannon:
   $$
   C = B \cdot \log_2(1 + \text{SNR})
   $$
   donde $C$ es la capacidad teórica del canal en bps y $B$ el ancho de banda en Hz. Si la SNR del canal cae, para sostener una comunicación fiable con un BER aceptable (típicamente $< 10^{-5}$ en enlaces de datos) el sistema debe conmutar hacia modulaciones más robustas y con menor número de niveles de señalización $M$ (como BPSK o QPSK en lugar de 16-QAM o 64-QAM), reduciendo la tasa efectiva de bits por símbolo transmitido.

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

La sincronización es el proceso mediante el cual el emisor y el receptor coordinan el tiempo para que el receptor sepa exactamente cuándo muestrear la señal entrante e interpretar correctamente la información digital enviada.

* **Sincronización a nivel de bit** Permite al receptor determinar la velocidad de transmisión y el instante exacto en el que empieza y termina un bit individual. Garantiza que el receptor lea la señal en el momento preciso para interpretar correctamente si es un 0 o un 1 digital.

* **Sincronización de trama** Identifica donde empieza y termina un bloque completo de datos(trama) dentro de un flujo de bits ya sincronizados utilizando secuencias o patrones especiales de bits que delimitan el inicio y final de una estructura de datos.

### Anatomía de una Trama: Encabezado, Carga Útil y Tráiler

Una trama es una unidad de datos estructurada que se transmite a nivel de la capa de enlace. Agrupa los datos del usuario junto con información de control para permitir una transmisión confiable y ordenada sobre un medio físico.

* **Encabezado (Header)**, se ubica al inicio de la trama y contiene datos de control para el transporte y entrega como direcciones físicas de origen y destino, tipo de protocolo, secuencia de paquete y bytes de sincronización.

* **Carga Util (Payload)**, es el bloque central que contiene los datos que se desean transmitir.

* **Trailer**, se encuentra en el final de la trama y contiene información de verificación y cierre, como algoritmos de detección de errores o de corrección para los mismos.

### Función y Relevancia del Preámbulo en la Transmisión

El preámbulo es una secuencia especifica de bits que se transmite inmediatamente antes de la trama propiamente dicha. 
Permite al receptor sincronizar su reloj con el del emisor antes de que lleguen datos reales. Consiste en un patron alternado (`1010101` por ejemplo) que ayuda al receptor a captar la frecuencia de muestreo y detectar el momento en que la trama inicia. 
No necesariamente es parte de la información util que se quiere transmitir ya que este es un sobrecosto del nivel físico/enlace que se utiliza unicamente para la sincronización del hardware, una vez sincronizado, el receptor descarta el preámbulo.

### Métodos para la Delimitación de Tramas en Protocolos de Enlace

1. **Tramas de longitud fija:** El receptor cuenta un numero fijo de bits o bytes a partir del delimitador de inicio. Una vez alcanzada esa cantidad exacta, se sabe que la trama actual a finalizado y que la siguiente secuencia corresponderá a una nueva trama o estará en estado de inactividad.

2. **Campo de longitud en el encabezado:** El encabezado de la trama incluye un campo numérico que especifica el tamaño total de la trama o de la carga util en bytes.
Cuando el receptor recibe este encabezado, lee el valor numérico y configura un contador. A medida que procesa el flujo de datos entrante, decrementa el contador hasta llegar a cero, lo que señala el final preciso de la trama.

3. **Caracteres o secuencias delimitadoras:** Consiste en utilizar patrones o secuencias de caracteres/bits específicos para marcar el inicio y el fin de la trama. El receptor monitorea continuamente el flujo de bits buscando el delimitador de cierre.
Para evitar que la secuencia se confunda si aparece de manera natural dentro de los datos transmitidos, se utilizan técnicas como el relleno de bits(bit stuffing) o el relleno de caracteres(byte stuffing), garantizando que el receptor identifique el patron solo cuando actúa como delimitador real.

---

## Procesamiento, Extracción y Reconstrucción de Tramas Binarias

### Formato de Trama y Extracción de la Carga Útil del Grupo

### Reensamblado Secuencial y Reconstrucción del Mensaje Global
