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

![Captura de pantalla mostrando paquete TCP y direcciones MAC](./assets/tp3-wiresharck-mac.png)

### Análisis de Tramas Ethernet y Direcciones MAC

En la trama Ethernet analizada, la dirección MAC de origen es `f0:c4:78:ba:88:40`, correspondiente al punto de acceso del router que proporciona la conexión Wi-Fi. La dirección MAC de destino es `24:b2:b9:5c:f0:7d`, correspondiente a la interfaz de red inalámbrica de la computadora.

Estas correspondencias se pudieron comprobar comparando la información mostrada por Wireshark con la dirección MAC de la interfaz inalámbrica de la computadora (mediante el comando `ifconfig`) y con la dirección MAC de la interfaz Wi-Fi del router (disponible en la etiqueta del dispositivo y en la interfaz web).

### Análisis del Paquete IP

Dentro de la trama Ethernet se encuentra un paquete IP cuya dirección de origen es `172.64.148.235` y cuya dirección de destino es `192.168.1.74`.

Esta última dirección corresponde a la computadora dentro de la red local, mientras que `172.64.148.235` corresponde al otro extremo con el que se está produciendo la comunicación.

### Comparación entre Direcciones MAC e IP

Las direcciones MAC e IP no representan lo mismo, ya que pertenecen a diferentes capas y cumplen funciones distintas.

En el caso de las direcciones de destino, ambas están relacionadas a la computadora, solo que tienen sentido en distintas capas del modelo. Por otro lado, la dirección MAC de origen corresponde al punto de acceso del router, mientras que la dirección IP de origen corresponde al extremo remoto de la comunicación.

Esto muestra que las direcciones MAC se utilizan para la comunicación dentro del enlace local, mientras que las direcciones IP permiten identificar los extremos de la comunicación a nivel de red. Por este motivo, el servidor remoto no aparece como origen de la trama Ethernet a nivel MAC: la trama que llega a la computadora proviene directamente del punto de acceso.

### Campo EtherType

El campo EtherType tiene el valor `0x0800`, que identifica al protocolo IPv4. Por lo tanto, la trama Ethernet encapsula un paquete IPv4.

IPv4 pertenece a la capa de Red del modelo OSI, situada por encima de la capa de Enlace de Datos.

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
