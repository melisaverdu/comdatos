![](/assets/2_1_Isologotipo_FCEFyN_y_UNC-_blanco_Sin_fondo-Con_bajada.png)

# Trabajo Práctico N.º 1: Comunicaciones 101

**Alumnos**
- García, Lautaro Misael 
- Pastrana Lizárraga, Iván
- Peretti, Federico Ariel
- Renaudo Gaggioli, Valentino
- Verdú, Melisa Noel

## 1. Fundamentos de comunicaciones

La comunicación a distancia requiere transformar la información original en una señal capaz de propagarse a través de un medio. Una señal acústica, como la voz, necesita un medio material para propagarse y presenta una atenuación considerable, por lo que no resulta adecuada para establecer comunicaciones a grandes distancias. Las ondas electromagnéticas, en cambio, permiten transportar información a grandes distancias y, dependiendo del medio y la frecuencia utilizada, pueden propagarse incluso en el vacío.

Para realizar una comunicación mediante ondas electromagnéticas, la información debe convertirse primero en una señal eléctrica y posteriormente en una onda electromagnética mediante una antena. La longitud de onda de esta radiación está relacionada con su frecuencia mediante

$$
\lambda = \frac{c}{f}
$$

donde $c$ es la velocidad de propagación de la onda electromagnética y $f$ su frecuencia.

La frecuencia de la señal original puede resultar demasiado baja para una transmisión eficiente mediante una antena. Por ejemplo, una señal de $1\text{ kHz}$ tendría una longitud de onda de aproximadamente $300 \text{ km}$, lo que conduciría a dimensiones de antena impracticables. Para resolver este inconveniente se utiliza una señal periódica de frecuencia mucho mayor, denominada **portadora**, sobre la cual se incorpora la información de la señal original o **banda base**.

Este proceso se denomina **modulación** y consiste, en términos generales, en trasladar la información desde su banda de frecuencias original hacia otra región del espectro mediante una portadora. En el receptor, el proceso inverso, denominado **demodulación**, permite recuperar la información contenida en la señal recibida.

La señal de banda base puede presentar diferentes características. Una **señal continua** está definida para todo instante de tiempo y puede adoptar valores que varían de manera continua, como ocurre con una señal eléctrica asociada a la voz. Una **señal discreta**, en cambio, está definida únicamente en determinados instantes o puede tomar un conjunto discreto de valores. Esta distinción resulta importante al estudiar los sistemas de comunicación, ya que la naturaleza de la información y de la señal condiciona las técnicas empleadas para su transmisión.

De manera general, cuando la información que modula la portadora es analógica, se habla de **modulación analógica**; cuando la información es digital, se emplean técnicas de **modulación digital**. En ambos casos, el principio fundamental es el mismo: utilizar una señal portadora para adaptar la información a las condiciones del medio de transmisión.

La portadora es una señal periódica caracterizada principalmente por su **amplitud, frecuencia y fase**. Según cuál de estos parámetros sea modificado por la información, pueden distinguirse diferentes técnicas de modulación. En las modulaciones analógicas clásicas se encuentran la **modulación de amplitud (AM)**, la **modulación de frecuencia (FM)** y la **modulación de fase (PM)**. En las técnicas digitales, esta misma idea da lugar a esquemas en los que la información modifica de manera discreta alguno de estos parámetros.

### Análisis del gráfico

El gráfico representa una onda electromagnética senoidal cuya amplitud disminuye a medida que aumenta la distancia recorrida. La disminución de amplitud representa la atenuación de la señal durante su propagación.

![Onda electromagnética](./assets/grafico-p1.png)

### Cálculo de parámetros de la onda

**Longitud de onda ($\lambda$)**

La longitud de onda es la distancia que recorre la onda durante un ciclo y puede determinarse como la distancia entre dos máximos consecutivos.

A partir del gráfico:

$$
\lambda = 120 \text{mm} - 60 \text{mm}
$$

$$
\boxed{\lambda = 60 \text{mm} = 0,06 \text{m}}
$$

**Frecuencia ($f$)**

Considerando una velocidad de propagación de $c=3 \times10^8 \text{m/s}$:

$$
f = \frac{c}{\lambda}
$$

$$
f = \frac{3\times10^8 \text{m/s}}{0,06 \text{m}}
= 5\times10^9 \text{Hz}
$$

$$
\boxed{f=5 \text{GHz}}
$$

### Región y banda del espectro electromagnético

La frecuencia obtenida, $5 \text{GHz}$, se encuentra dentro del rango de **microondas**, correspondiente a frecuencias comprendidas aproximadamente entre $3$ y $30 \text{GHz}$.

Dentro de la clasificación de bandas de radio, este rango corresponde a la **banda SHF (Super High Frequency)**.

### Dispositivos de comunicaciones en la banda SHF

La banda de $5 \text{GHz}$ es utilizada por diferentes sistemas de comunicaciones inalámbricas. Entre ellos se encuentran las redes **Wi-Fi**, particularmente aquellas que utilizan las bandas de $5 \text{GHz}$, como Wi-Fi 5 (IEEE 802.11ac) y Wi-Fi 6 (IEEE 802.11ax).

Un ejemplo de dispositivo que opera en esta banda es un **punto de acceso o router Wi-Fi de 5 GHz**.

### Fenómeno representado por la línea de trazos roja

La línea de trazos roja representa la **atenuación**, es decir, la disminución de la amplitud o potencia de una señal a medida que se propaga.

### Incidencia del fenómeno y experiencia cotidiana

La atenuación afecta a las comunicaciones Wi-Fi y limita su alcance efectivo. En una vivienda, por ejemplo, la señal suele disminuir al aumentar la distancia respecto del punto de acceso y al atravesar obstáculos como paredes, lo que puede reducir la calidad y velocidad de la conexión.

### Efecto de la atenuación en distintos medios

La atenuación está presente en diferentes medios de transmisión. En las **comunicaciones celulares**, la señal pierde potencia debido a la distancia recorrida y a obstáculos presentes en el entorno. En **cables coaxiales**, se producen pérdidas asociadas al conductor y al dieléctrico. En **fibra óptica** también existe atenuación, en este caso, las pérdidas se deben principalmente a fenómenos como la absorción y la dispersión en el material de la fibra.


## 2. Transmisión de señales digitales

Comunicar datos a través de cualquier medio es un proceso que consiste en modificar el comportamiento de una señal en el tiempo. Analicemos el siguiente sistema:

![Esquema de comunicación digital](assets/punto2_esquema.png)

### Tipo y modo de transmisión
El esquema muestra dos módulos de comunicación conectados por dos líneas: una de ellas es de datos y la otra es de reloj, donde cada módulo posee su propio reloj sincronizado y las flechas van en un solo sentido (izquierda a derecha).

* **Modo de transmisión (Direccionalidad):** Es de modo **simplex**, es decir, los datos viajan en una sola dirección.
* **Características temporales:** Es de tipo **sincrónica**, debido a que existe una señal de reloj compartida entre ambos módulos que marca el momento exacto en el que se debe leer cada bit.
* **Formato:** Es una transmisión **serial (en serie)**, lo que significa que los bits se transmiten uno detrás de otro por una única línea de datos, no en paralelo.

### Evaluación del esquema de comunicación
#### ¿Es este el mejor paradigma si se busca transmitir datos rápidamente y de forma bidireccional?
No. Este esquema no permite la bidireccionalidad por ser de tipo simplex. Para lograr una comunicación en ambos sentidos y con mayor eficiencia, se requeriría como mínimo un esquema **Half-Duplex** (bidireccional no simultáneo) o idealmente **Full-Duplex** (bidireccional simultáneo).

### Transmisión de la cuarta letra del nombre del grupo
En la expresión más simple de señal digital, podemos pensar que un nivel de tensión "1" representa un 1 digital, y un nivel de tensión "0" representa un 0 digital. Con esto en mente, analicemos el gráfico de ejemplo donde se representa la transmisión del byte `"00100011"` (símbolo `#` en ASCII):

![Ejemplo de transmisión de byte en ASCII](assets/punto2_ejemplo.png)

Si quisiéramos transmitir la **cuarta letra** del nombre del grupo (la letra **"a"**, cuyo valor en código ASCII es **97** o `01100001` en binario de 8 bits), el diagrama de la señal digital correspondiente queda representado de la siguiente manera:

![Diagrama de transmisión de la letra 'a'](assets/punto2.png)


### Punto de medición de la señal
Debido a que la transición de tensión no es instantánea (representada con las flechas rojas), no conviene realizar el muestreo o medición justo en los flancos de subida o de bajada, ya que en esos instantes la señal se encuentra en estado de transición y se podrían obtener lecturas erróneas.

Lo correcto es realizar la medición en el **punto medio del intervalo del bit**, dando el tiempo suficiente para que el nivel de tensión se estabilice en la línea antes del muestreo.


## 3. Modulación de señales digitales



## 4. Implementación en Packet Tracer



## 5. Conclusiones



## Referencias
