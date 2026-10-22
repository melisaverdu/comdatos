# Trabajo Práctico N.º 3: Capas de Enlace de Datos, Red y Transporte

Trabajo práctico correspondiente a la asignatura **Comunicaciones de Datos** (FCEFyN - UNC).

## Estructura

```text
TP3/
├── assets/
├── informe.md
└── README.md
```

### `informe.md`

Documento principal del trabajo práctico. Contiene el desarrollo teórico y práctico de:
* Organización de la información en la red local (capa de enlace vs. capa de red, direcciones MAC e IP, estructura de la trama Ethernet y campo EtherType).
* Captura e inspección de tráfico en vivo con Wireshark.
* Capa de transporte y protocolo TCP (funciones y problemas que resuelve, análisis de cabeceras TCP/UDP, mecanismos de establecimiento *Three-way handshake* y finalización de conexión).
* Captura de conexión local mediante Packet Sender y Wireshark, junto con el análisis de seguridad en tráfico no cifrado.
* Comunicación interactiva con un servidor en la nube vía TCP persistente y validación de comando de grupo.

### `assets/`

Recursos gráficos y capturas de pantalla utilizadas en el informe:
* Esquemas conceptuales de establecimiento (*Three-way handshake*) y cierre (*Four-way handshake*) de conexiones TCP.
* Capturas de paquetes y tramas en Wireshark (direcciones MAC/IP, EtherType y análisis de carga útil).
* Capturas de la secuencia de conexión TCP local en loopback (`SYN`, `SYN-ACK`, `ACK`, datos y cierre con `FIN`).
* Capturas de la interacción y sesión de comandos con el servidor remoto en Packet Sender y Wireshark.
