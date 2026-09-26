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

La capa de enlace de datos(Capa 2) se encarga de la transferencia confiable de datos a traves del medio físico. Sus funciones principales son la detección y corrección de errores, la delimitación de tramas y control de acceso al medio(MAC) y gestión de flujos de datos.

Resuelve la comunicación de **nodo a nodo** dentro de una misma red local(LAN). Solo se encarga de llevar los datos entre dispositivos adyacentes conectados al mismo segmento físico o lógico

### Dirección MAC vs. Dirección IP

Las direcciones MAC(Media Access Control) es un identificador único de 48 bits asignado por el fabricante a la tarjeta de interfaz de red(NIC) del dispositivo. Es una dirección **física** y **permanente**

Las diferencias principales con las direcciones IP son:

- Capa OSI: La MAC trabaja en la capa 2(Enlace), mientras que la IP trabaja en la capa 3(Red)

- La dirección MAC es física e inmutable mientras que la dirección IP es lógica y dinámica

- La dirección MAC se utiliza solo para direccionar paquetes dentro de la misma red local mientras que la IP se utiliza para enrutar paquetes a traves de diferentes redes e internet

### Trama Ethernet y sus campos

- **Preámbulo y SFD(Start Frame Delimiter)** 8 bytes en total. Sirven para sincronizar los relojes del emisor y el receptor, e indicar el inicio exacto de la trama.

- **Dirección MAC de destino**: 6 bytes. Indica la dirección física del dispositivo receptor

- **Dirección MAC de origen** : 6 bytes . indica la dirección física del emisor

- **Tipo/Ethertype**: 2 bytes, indican que protocolo de capa 3 viene encapsulado dentro de los datos

- **Datos y relleno**: de 46 a 1500 bytes, contiene la información de capas superiores, si los datos son de menos de 46 bytes se agrega un relleno para cumplir con la longitud minima de la trama

- **Secuencia de verificación de trama**: 4 bytes para un código de comprobación de redundancia cíclica utilizado por el receptor para verificar se la trama sufrió corrupción de datos durante la transmisión

### Determinación del protocolo de capa superior

La información que permite determinar que protocolo de capa superior esta transportando una trama Ethernet es el campo EtherType de la trama Ethernet, que contiene un valor numérico hexadecimal que especifica el protocolo encapsulado en la carga util

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

### Sesión de Comandos con el Servidor


### Validación por Nombre de Grupo


---

## Conclusiones Generales
