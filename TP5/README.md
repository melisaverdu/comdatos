# Trabajo Práctico N.º 5: Transmisión de Datos: de ICMP y ARP a Sockets TCP entre Dos Computadoras

Trabajo práctico correspondiente a la asignatura **Comunicaciones de Datos** (FCEFyN - UNC).

## Estructura

```text
TP5/
├── assets/
├── src/
│   ├── tcp_client.py
│   └── tcp_server.py
├── informe.md
└── README.md
```

### `informe.md`

Documento principal del trabajo práctico. Contiene el desarrollo teórico y práctico de:
* ICMP y primer contacto con Wireshark: funcionamiento de `ping` (Echo Request / Echo Reply), configuración de red, filtros de captura, análisis de capas y encapsulación, alcance de las direcciones MAC e IP, *payload* y TTL.
* ARP: resolución de direcciones IP a MAC, caché ARP, generación de tráfico (borrado de la caché y ping a una IP inexistente) y análisis de las tramas ARP Request y Reply.
* TCP y UDP "a mano" con `ncat`: experimentos en loopback, comparación de encabezados, cantidad de paquetes, cierre de sesión y comportamiento ante puertos cerrados (`RST` vs. ICMP *Port Unreachable*).
* Servidor TCP mínimo en Python: análisis de la API de sockets y correlación de cada llamada con los segmentos TCP observados en Wireshark.

### `src/`

Programas en Python utilizados en el punto 4:
* `tcp_server.py`: servidor TCP mínimo que acepta una conexión, recibe un mensaje y responde con `Recibido: <mensaje>`.
* `tcp_client.py`: cliente TCP que se conecta al servidor, envía un mensaje y muestra la respuesta.

Uso en loopback:

```bash
# Terminal A
python3 TP5/src/tcp_server.py

# Terminal B
python3 TP5/src/tcp_client.py 127.0.0.1 "Hola desde mi programa"
```

### `assets/`

Recursos gráficos y capturas de pantalla utilizadas en el informe, con un prefijo por punto:
* `p1_*`: configuración de red, pings y capturas de Wireshark con los filtros ICMP.
* `p2_*`: caché ARP, borrado y nueva resolución del gateway, ping a una IP inexistente y detalle de las tramas ARP.
* `p3_*`: terminales y capturas de las sesiones TCP y UDP con `ncat`, y de la prueba con puertos cerrados.
* `p4_*`: captura general y detalle de cada segmento de la sesión del servidor TCP mínimo.
