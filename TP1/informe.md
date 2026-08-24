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



## 4. Implementación en Packet Tracer

### Análisis de la Configuración Inalámbrica del Router
![Red implementada](/TP1/assets/punto_4.png)

A partir de la información extraída de la interfaz de configuración del router, se determinan los siguientes parámetros físicos y de espectro:

* **Frecuencia de Operación:** *2.412 GHz*, correspondiente al **Canal 1** asignado en la interfaz inalámbrica.
* **Región del Espectro Electromagnético:** Pertenece al espectro de **Radiofrecuencia (RF)**, específicamente a la región de **Ultra Alta Frecuencia (UHF)**, la cual abarca el rango comprendido entre $300 \text{ MHz}$ y $3 \text{ GHz}$.
* **Banda de Operación:** Opera en la banda de *2.4 GHz*.

---

### Comprobación de conectividad entre computadoras mediante Ping

#### Comprobación 1
Desde la computadora de escritorio (PC0), revisamos la conexión con la notebook desde la CLI mediante `ping`:
![Ping desde PC0 a Notebook](/TP1/assets/punto_4_g_(1).png)

#### Comprobación 2
Desde la notebook, revisamos la conexión con la computadora de escritorio desde la CLI mediante `ping`:
![Ping desde Notebook a PC0](/TP1/assets/punto_4_g_(2).png)

---

### Comprobación de Cobertura Inalámbrica en la Vista Física (Punto 4.h)

Se evaluó la calidad de la señal y la conectividad inalámbrica desplazando la notebook a distintas distancias del router dentro de la vista física, ejecutando pruebas de `ping` hacia la PC de escritorio (`192.168.0.102`):

#### Pruebas de Conectividad CLI
   ![Pruebas de Ping en consola](/TP1/assets/punto_4_h_pings.png)

#### Análisis según ubicación física:

1. **Ubicación 1 (Dentro de la oficina):** 
   * **Estado:** Enlace óptimo.
   * **Resultado:** **0% de paquetes perdidos** / Latencia promedio: **14 ms**.
   ![Notebook dentro de la oficina](/TP1/assets/punto_4_h_pos1.png)

2. **Ubicación 2 (Límite de señal Wi-Fi):** 
   * **Estado:** Enlace operativo en el borde de cobertura.
   * **Resultado:** **0% de paquetes perdidos** / Latencia promedio: **17 ms**.
   ![Notebook en el limite de cobertura](/TP1/assets/punto_4_h_pos2.png)

3. **Ubicación 3 (Fuera de la zona de cobertura):** 
   * **Estado:** Sin señal.
   * **Resultado:** **100% de paquetes perdidos** (`Request timed out`).
   ![Notebook fuera de cobertura](/TP1/assets/punto_4_h_pos3.png)


## 5. Conclusiones

Se analizaron los aspectos fundamentales de la transmisión de datos, integrando la teoría física con la simulación práctica:

* **Propagación y atenuación:** La atenuación es inherente a cualquier medio. En bandas como UHF (2.4 GHz) y SHF (5 GHz), la pérdida de potencia por distancia limita la cobertura, exigiendo un diseño adecuado entre potencia de emisión y sensibilidad del receptor.
* **Limitación del canal y modulación:** Las señales digitales escalonadas poseen un ancho de banda teóricamente infinito. Dado que los canales reales filtran las altas frecuencias y distorsionan la señal, la modulación de portadoras es esencial para transmitir información digital eficientemente.
* **Compromiso en $M\text{-PSK}$ (BER vs. Eficiencia):** Existe un balance entre velocidad y robustez frente al ruido. Mientras $\text{BPSK}$ ofrece la menor probabilidad de error ($\text{BER}$) gracias a la máxima separación entre símbolos ($180^\circ$), esquemas de mayor orden ($\text{QPSK}$, $8\text{-PSK}$) aumentan la tasa de transferencia a costa de una mayor sensibilidad a las interferencias.
* **Validación en Packet Tracer:** La simulación confirmó que la atenuación impacta de forma directa en el desempeño. Dentro del área de cobertura la pérdida de paquetes es del 0% con latencias estables, pero al superar el umbral de sensibilidad del receptor la señal se degrada por completo y la comunicación se corta.

## Referencias
*[1]* William Stallings, Comunicaciones y redes de computadores, 7.ª edición, capítulo 3 *“Transmisión de datos”*.