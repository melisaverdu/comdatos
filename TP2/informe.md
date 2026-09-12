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

### Compensación de Variaciones de Frecuencia y Control de Fase

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
