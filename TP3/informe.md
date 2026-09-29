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


### Campos del Frame/Cabecera TCP y UDP


### Handshake en TCP


### Captura de Conexión Local (PacketSender + Wireshark)


### Cierre de Conexión


### Conclusión sobre Seguridad


---

## Comunicación con Servidor en la Nube y Validación de Grupo

Para esta actividad se utilizó una instancia de **Packet Sender** como cliente para establecer una comunicación con el servidor proporcionado por el docente. El servidor se encuentra desplegado en la nube y se accedió mediante la dirección IP y el puerto indicados en el material de la materia.

La sesión fue capturada mediante **Wireshark**, permitiendo observar el establecimiento de la conexión y el intercambio de datos entre el cliente y el servidor.

### Sesión de Comandos con el Servidor

Se estableció una conexión persistente con el servidor utilizando la opción **Persistent TCP** de Packet Sender. Esta modalidad permitió mantener la conexión abierta para enviar sucesivos comandos e interactuar con el servidor.

Los comandos enviados debían finalizar con la secuencia `\r`, utilizada como terminador de cada mensaje. Para simplificar el procedimiento, se habilitó la opción **Append \r** de Packet Sender, de modo que el carácter de terminación se agregara automáticamente a cada comando.

Se enviaron los comandos indicados en la consigna:

* `hola`
* `ping`
* `tic`
* `status`

En cada caso se verificó la respuesta recibida desde el servidor.

<p align="center">
  <img src="./assets/4-1-comandos_server.png" alt="Packet Sender mostrando la conexión persistente y el intercambio de comandos y respuestas." width="80%" />
</p>

La comunicación completa fue capturada con Wireshark. En la captura se puede observar el tráfico TCP correspondiente a la sesión, incluyendo los segmentos intercambiados entre el cliente y el servidor.

<p align="center">
  <img src="./assets/4-3-sesion_wireshark_payload.png" alt="Wireshark mostrando la captura completa de la sesión TCP." width="80%" />
</p>

### Validación por Nombre de Grupo

Como instancia final de validación, se utilizó el **nombre del grupo como comando**. Se mantuvo la conexión con el servidor y se envió el nombre correspondiente al grupo, nuevamente utilizando `\r` como terminador.

El servidor reconoció el nombre del grupo como un comando válido y respondió con el mensaje correspondiente.

<p align="center">
  <img src="./assets/4-2-respuesta_nombre_grupo.png" alt="Packet Sender mostrando el envío del nombre del grupo y la respuesta del servidor." width="80%" />
</p>

La respuesta obtenida fue registrada también en la pestaña correspondiente de la planilla compartida de la materia, completando así la validación solicitada en la consigna.

---

## Conclusiones Generales
