# Trabajo Práctico N° 3 - Redes de Computadoras

**Integrantes:**
- García, Lautaro Misael 
- Pastrana Lizárraga, Iván
- Peretti, Federico Ariel
- Renaudo Gaggioli, Valentino
- Verdú, Melisa Noel

---

## Organización de la Información en la Red Local

### Función de la capa de enlace y tipo de comunicación


### Dirección MAC vs. Dirección IP


### Trama Ethernet y sus campos


### Determinación del protocolo de capa superior


---

## Captura e Inspección de Tráfico con Wireshark

### Análisis de Tramas Ethernet y Direcciones MAC


### Análisis del Paquete IP


### Comparación entre Direcciones MAC e IP


### Campo EtherType


---

## Capa de Transporte y Protocolo TCP

### Problemas que resuelve TCP

La capa de transporte proporciona un servicio de transferencia de datos **extremo a extremo**, aislando a las capas superiores de los detalles de las redes intermedias. En Internet, IP ofrece un servicio de entrega de datagramas que no garantiza que los datos lleguen, que lo hagan en orden ni que no se produzcan pérdidas o duplicaciones. TCP incorpora mecanismos adicionales para proporcionar a las aplicaciones un servicio **orientado a conexión y fiable**. 

Entre las principales funciones de TCP se encuentran:

* **Segmentación:** recibe un flujo de bytes de la aplicación y lo divide en segmentos para su transmisión. TCP numera los bytes del flujo, permitiendo reconstruirlo en el receptor. 
* **Entrega fiable:** utiliza números de secuencia, confirmaciones y retransmisiones para detectar pérdidas y recuperar los datos que no hayan llegado correctamente.
* **Entrega ordenada:** los números de secuencia permiten que el receptor reconstruya el flujo de bytes en el orden correspondiente.
* **Control de flujo:** regula la cantidad de datos que puede enviar el emisor para evitar que el receptor se vea desbordado. TCP utiliza para ello un mecanismo basado en créditos, mediante los campos de número de secuencia, número de confirmación y ventana. 
* **Control de congestión:** adapta la velocidad de transmisión cuando detecta congestión en la red, evitando que una conexión TCP contribuya excesivamente a saturar los enlaces y routers intermedios. 
* **Multiplexación y demultiplexación:** utiliza números de puerto para asociar los datos recibidos con el proceso correspondiente. Una conexión TCP queda identificada por las direcciones IP y los números de puerto de origen y destino. 
* **Establecimiento y finalización de la conexión:** utiliza mecanismos específicos para establecer una conexión antes de transmitir datos y finalizarla posteriormente.

De esta manera, TCP permite que una aplicación utilice un servicio de transporte fiable sin tener que implementar directamente los mecanismos necesarios para detectar pérdidas, ordenar los datos, controlar el flujo o adaptarse a la congestión de la red.

### Campos del Frame/Cabecera TCP y UDP

TCP agrega una **cabecera** a los datos provenientes de la capa de aplicación, formando un segmento TCP. Entre los campos más importantes se encuentran:

| Campo                                  | Función                                                                                                                                      |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Puerto de origen**                   | Identifica el proceso o aplicación que envía los datos.                                                                                      |
| **Puerto de destino**                  | Identifica el proceso o aplicación que debe recibir los datos.                                                                               |
| **Número de secuencia**                | Identifica la posición de los bytes transportados dentro del flujo de datos y permite mantener su orden.                                     |
| **Número de confirmación (ACK)**       | Indica el próximo número de secuencia que el receptor espera recibir, confirmando los datos recibidos correctamente.                         |
| **Longitud de cabecera (Data Offset)** | Indica dónde comienza la carga útil del segmento, permitiendo determinar el tamaño de la cabecera.                                           |
| **Flags o indicadores**                | Controlan diferentes funciones de TCP. Entre ellos se encuentran `SYN`, `ACK`, `FIN` y `RST`.                                                |
| **Ventana de recepción (Window)**      | Indica la cantidad de datos que el receptor está preparado para aceptar y participa en el control de flujo.                                  |
| **Checksum**                           | Permite detectar errores en el segmento recibido. TCP calcula la suma de comprobación sobre el segmento y una pseudocabecera asociada a IP.  |
| **Opciones**                           | Permiten incorporar parámetros y funcionalidades adicionales de TCP.                                                                         |
| **Datos**                              | Contiene la carga útil proveniente de la capa de aplicación.                                                                                 |

Los campos de **puerto de origen y destino** permiten realizar la multiplexación y demultiplexación de las aplicaciones, mientras que los campos de **secuencia, confirmación y ventana** son fundamentales para los mecanismos de transferencia fiable y control de flujo.

A diferencia de TCP, **UDP posee una cabecera mucho más sencilla**. Sus campos principales son puerto de origen, puerto de destino, longitud y checksum. UDP no establece una conexión previamente ni proporciona mecanismos propios de entrega fiable, ordenamiento o control de congestión. Por este motivo, ofrece una sobrecarga y una complejidad menores que TCP. 

### Handshake en TCP

TCP establece una conexión mediante un **proceso de acuerdo en tres fases (Three-way handshake)**. Su objetivo es que ambos extremos puedan establecer los parámetros iniciales de la conexión y confirmar que están preparados para comunicarse.

Supongamos que un cliente desea establecer una conexión con un servidor. El procedimiento consta de tres pasos:

1. **SYN:** el cliente envía un segmento TCP con el indicador `SYN` activado. El segmento no contiene datos de la aplicación y contiene un **número de secuencia inicial** seleccionado por el cliente, denominado `cliente_nsi`.

2. **SYN + ACK:** al recibir el segmento, el servidor responde con un segmento que tiene activados los indicadores `SYN` y `ACK`. El servidor selecciona su propio número de secuencia inicial, `servidor_nsi`, y establece el número de confirmación en `cliente_nsi + 1`. De esta forma, confirma la recepción del `SYN` del cliente y comunica su propio número de secuencia inicial.

3. **ACK:** el cliente responde con un segmento `ACK`, cuyo número de confirmación es `servidor_nsi + 1`. En este segmento el indicador `SYN` ya se encuentra desactivado. Una vez completado este intercambio, ambos extremos pueden comenzar a enviar segmentos con datos de la aplicación. Este tercer segmento también puede transportar datos. 

**Figura 3.39. Proceso de acuerdo en tres fases de TCP.**
*Fuente: Kurose y Ross, sección 3.5.6.*

<p align="center">
  <img src="./assets/three-way_handshake.png" alt="El proceso de acuerdo en tres fases de TCP: intercambio de segmentos." width="80%" />
</p>

Para finalizar una conexión, cualquiera de los dos extremos puede solicitar el cierre. En el caso descrito por Kurose y Ross, el cliente inicia el procedimiento enviando un segmento con el indicador `FIN` activado. El servidor responde con un `ACK` y posteriormente envía su propio segmento `FIN`. Finalmente, el cliente confirma este último segmento mediante otro `ACK`. 

Este intercambio suele denominarse **Four-way handshake**. A diferencia del establecimiento, el cierre requiere que cada extremo indique que terminó de transmitir en su propia dirección. Una vez finalizado el procedimiento, se liberan los recursos asociados a la conexión, como los buffers y las variables utilizadas por TCP. 

**Figura 3.40. Cierre de una conexión TCP.**
*Fuente: Kurose y Ross, sección 3.5.6.*

<p align="center">
  <img src="./assets/four-way_handshake.png" alt="Cierre de una conexión TCP." width="80%" />
</p>


### Captura de Conexión Local (PacketSender + Wireshark)


### Cierre de Conexión


### Conclusión sobre Seguridad


---

## Comunicación con Servidor en la Nube y Validación de Grupo

### Sesión de Comandos con el Servidor


### Validación por Nombre de Grupo


---

## Conclusiones Generales
