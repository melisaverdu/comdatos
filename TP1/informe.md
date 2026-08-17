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

## 2. Transmisión de señales digitales



## 3. Modulación de señales digitales



## 4. Implementación en Packet Tracer



## 5. Conclusiones



## Referencias
