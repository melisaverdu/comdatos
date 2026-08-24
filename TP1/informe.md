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

### Tipo y modo de transmisión
El esquema muestra dos módulos de comunicación conectados por dos líneas: una de ellas es de datos y la otra es de reloj, donde cada módulo posee su propio reloj sincronizado y las flechas van en un solo sentido (izquierda a derecha).

* **Modo de transmisión (Direccionalidad):** Es de modo **simplex**, es decir, los datos viajan en una sola dirección.
* **Características temporales:** Es de tipo **sincrónica**, debido a que existe una señal de reloj compartida entre ambos módulos que marca el momento exacto en el que se debe leer cada bit.
* **Formato:** Es una transmisión **serial (en serie)**, lo que significa que los bits se transmiten uno detrás de otro por una única línea de datos, no en paralelo.

### ¿Es este el mejor paradigma si se busca transmitir datos rápidamente y de forma bidireccional?
No. Este esquema no permite la bidireccionalidad por ser de tipo simplex. Para lograr una comunicación en ambos sentidos y con mayor eficiencia, se requeriría como mínimo un esquema **Half-Duplex** (bidireccional no simultáneo) o idealmente **Full-Duplex** (bidireccional simultáneo).

### Transmisión de la cuarta letra del nombre del grupo
La cuarta letra del nombre del grupo es la **"a"**, cuyo valor en código ASCII es **97** (o `01100001` en binario de 8 bits).

![Diagrama de transmisión de la letra 'a'](/TP1/assets/punto2.png)


### ¿Dónde medir la señal dada la pendiente de transición?
Debido a que la transición de tensión no es instantánea (representada con las flechas rojas), no conviene realizar el muestreo o medición justo en los flancos de subida o de bajada, ya que en esos instantes la señal se encuentra en estado de transición y se podrían obtener lecturas erróneas.

Lo correcto es realizar la medición en el **punto medio del intervalo del bit**, dando el tiempo suficiente para que el nivel de tensión se estabilice en la línea antes del muestreo.


## 3. Modulación de señales digitales



## 4. Implementación en Packet Tracer



## 5. Conclusiones



## Referencias
