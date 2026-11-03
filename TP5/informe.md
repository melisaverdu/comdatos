![](/assets/2_1_Isologotipo_FCEFyN_y_UNC-_blanco_Sin_fondo-Con_bajada.png)

# Trabajo Práctico N.º 5: Transmisión de Datos: de ICMP y ARP a Sockets TCP entre Dos Computadoras

**Alumnos**
- García, Lautaro Misael 
- Pastrana Lizárraga, Iván
- Peretti, Federico Ariel
- Renaudo Gaggioli, Valentino
- Verdú, Melisa Noel

---

### Índice

- [Trabajo Práctico N.º 5: Transmisión de Datos: de ICMP y ARP a Sockets TCP entre Dos Computadoras](#trabajo-práctico-nº-5-transmisión-de-datos-de-icmp-y-arp-a-sockets-tcp-entre-dos-computadoras)
    - [Índice](#índice)
  - [ICMP y primer contacto con Wireshark.](#icmp-y-primer-contacto-con-wireshark)
    - [Fundamentos teóricos de ICMP y Ping](#fundamentos-teóricos-de-icmp-y-ping)
    - [Configuración de red y captura de tráfico](#configuración-de-red-y-captura-de-tráfico)
    - [Análisis de capas, encapsulación y campos](#análisis-de-capas-encapsulación-y-campos)
  - [ARP: de una IP a una dirección MAC](#arp-de-una-ip-a-una-dirección-mac)
    - [Resolución de direcciones y caché ARP](#resolución-de-direcciones-y-caché-arp)
    - [Generación y captura de tráfico ARP](#generación-y-captura-de-tráfico-arp)
    - [Análisis de tramas ARP Request y Reply](#análisis-de-tramas-arp-request-y-reply)
  - [TCP y UDP "a mano" con ncat](#tcp-y-udp-a-mano-con-ncat)
    - [Conceptos de la capa de transporte](#conceptos-de-la-capa-de-transporte)
    - [Experimento TCP en Loopback](#experimento-tcp-en-loopback)
    - [Experimento UDP en Loopback](#experimento-udp-en-loopback)
    - [Comparación detallada TCP vs. UDP](#comparación-detallada-tcp-vs-udp)
  - [Servidor TCP mínimo](#servidor-tcp-mínimo)
    - [Análisis de sockets TCP](#análisis-de-sockets-tcp)
    - [Ejecución e inspección en Loopback](#ejecución-e-inspección-en-loopback)
    - [Tabla de primitivas de sockets vs. tráfico de red](#tabla-de-primitivas-de-sockets-vs-tráfico-de-red)
  - [Conclusión](#conclusión)
  - [Referencias](#referencias)

---

## ICMP y primer contacto con Wireshark.

### Fundamentos teóricos de ICMP y Ping

<!-- 
Preguntas a responder:
a) ¿Qué es ICMP y para qué se usa? ¿Transporta datos de aplicaciones como lo hacen TCP o UDP?
b) ¿Qué relación tiene con IP? ¿Viaja dentro de IP, al lado de IP o debajo de IP? ¿Cómo sabe el receptor que el contenido de un paquete IP es ICMP?
c) ¿Qué hace ping? ¿Qué son un Echo Request y un Echo Reply? ¿Qué campos de ICMP permiten distinguirlos?
d) ¿Qué información mínima contiene un mensaje ICMP de tipo Echo?
-->

### Configuración de red y captura de tráfico

<!-- 
Configuración de red local:
- IPv4, máscara, gateway por defecto y dirección MAC (ip addr / ip route / ipconfig).
- Capturas en Wireshark: ping al gateway y ping a 8.8.8.8.
- Filtros utilizados: icmp, icmp.type == 8, icmp.type == 0, icmp && ip.addr == 8.8.8.8.
-->

### Análisis de capas, encapsulación y campos

<!-- 
- Tabla de capas identificadas en Wireshark (Ethernet II, IPv4, ICMP, Payload) con direcciones origen/destino y campos selectores de protocolo superior.
- Análisis justificativo:
  a) MAC destino a 8.8.8.8 vs gateway (alcance MAC vs IP).
  b) Comparación Echo Request vs Echo Reply (campos que varían vs fijos, IDs y secuencia).
  c) Payload de ping (tamaño, contenido y diferencias entre SO).
  d) Análisis de TTL (Request vs Reply de 8.8.8.8 y acción del router).
  e) Diagrama de encapsulación "cajas dentro de cajas" con tamaños en bytes.
-->

---

## ARP: de una IP a una dirección MAC

### Resolución de direcciones y caché ARP

<!-- 
Preguntas conceptuales:
a) ¿Qué problema resuelve ARP? ¿En qué capa se ubica y por qué es discutible?
b) ¿Qué es un ARP Request y un ARP Reply? ¿A quién se envía cada uno?
c) ¿Qué es la caché ARP y por qué existe?
d) Explicación con palabras propias del mecanismo de resolución en LAN.
e) Inspección de la caché ARP local (arp -a / ip neigh show) y verificación de la MAC del gateway.
-->

### Generación y captura de tráfico ARP

<!-- 
- Procedimiento para generar tráfico ARP nuevo (Opción A: IP inexistente en LAN, Opción B: borrado de caché del gateway, Opción C: ping a otro host LAN).
- Captura de tráfico con filtros: arp, arp.opcode, arp.dst.proto_ipv4, arp || icmp, eth.dst == ff:ff:ff:ff:ff:ff.
-->

### Análisis de tramas ARP Request y Reply

<!-- 
- Tabla comparativa de campos de ARP Request y Reply (MAC destino/origen Ethernet, Opcode, Sender MAC/IP, Target MAC/IP).
- Preguntas de análisis:
  a) Por qué Request es broadcast y Reply unicast; valor de Target MAC en Request.
  b) Campo EtherType en Ethernet (0x0806) y ausencia de encabezado IP (dónde vive ARP).
  c) Observación con IP inexistente (reintentos de ARP, presencia/ausencia de ICMP).
  d) Reintento de ping tras 1 minuto (comportamiento de caché, ventajas y riesgos de entradas desactualizadas).
-->

---

## TCP y UDP "a mano" con ncat

### Conceptos de la capa de transporte

<!-- 
Investigación previa:
a) ¿Qué significa "establecer una conexión"? ¿Dónde "existe" una conexión TCP (cables, routers o extremos)?
b) ¿Qué es un puerto? ¿Qué identifica el par (IP, puerto)?
c) ¿Qué significa que un proceso esté "escuchando" en un puerto?
-->

### Experimento TCP en Loopback

<!-- 
- Ejecución con ncat en loopback (puerto 12000): servidor ncat -v -l 12000, cliente ncat -v 127.0.0.1 12000.
- Captura Wireshark con filtro tcp.port == 12000 en interfaz loopback (lo / Npcap Loopback).
- Intercambio de mensajes y cierre de sesión.
-->

### Experimento UDP en Loopback

<!-- 
- Ejecución con ncat en loopback (puerto 12001): servidor ncat -v -u -l 12001, cliente ncat -v -u 127.0.0.1 12001.
- Captura Wireshark con filtro udp.port == 12001 en interfaz loopback.
- Intercambio de datagramas y cierre con Ctrl+C.
-->

### Comparación detallada TCP vs. UDP

<!-- 
Respuestas a las consignas de análisis:
a) Comportamiento en la red al ejecutar el cliente antes del primer mensaje (TCP vs UDP).
b) Datagramas generados por mensaje y presencia/ausencia de ACKs.
c) Comparación de encabezados (campos y tamaños en bytes de TCP vs UDP).
d) Comportamiento al cerrar con Ctrl+C (teardown de TCP vs silencio de UDP).
e) Cantidad total de paquetes para una misma frase (overhead vs confiabilidad).
f) Comportamiento ante puertos cerrados (RST en TCP vs ICMP Port Unreachable en UDP).
-->

---

## Servidor TCP mínimo

### Análisis de sockets TCP

Los scripts `TP5/src/tcp_server.py` y `TP5/src/tcp_client.py` implementan una comunicación cliente-servidor sobre TCP utilizando la API de sockets provista por el módulo `socket` de Python. Un socket actúa como el punto final (*endpoint*) local a través del cual el proceso de usuario entrega y consume bytes, delegando en el sistema operativo la gestión de la máquina de estados de TCP, el encapsulamiento en paquetes IPv4 y la transmisión a través de la interfaz de red.

- **Funcionamiento de `tcp_server.py`:** crea un socket TCP sobre IPv4 (`servidor`), habilita la reutilización inmediata del puerto local (`SO_REUSEADDR`), lo asocia a la dirección `127.0.0.1:12000` (`bind()`) y lo coloca en estado de escucha pasiva (`listen(1)`). A continuación, se bloquea en `accept()` hasta que un cliente completa el *three-way handshake*. Cuando esto ocurre, recibe el nuevo socket dedicado a esa sesión (`conexion`) junto con la tupla `(IP, puerto)` del cliente, lee hasta 1024 bytes del flujo mediante `recv(1024)`, decodifica el mensaje en UTF-8 y envía de vuelta la cadena `"Recibido: " + mensaje` con `sendall()`. Finalmente, aguarda a que el cliente inicie el cierre ordenado consumiendo del socket en un bucle `while conexion.recv(1024): pass` hasta recibir `b""` (EOF) y libera ambos descriptores con `conexion.close()` y `servidor.close()`.
- **Funcionamiento de `tcp_client.py`:** crea su propio socket TCP sobre IPv4 (`cliente`), fija un tiempo máximo de espera de 5 segundos (`settimeout(5)`) e invoca `connect(("127.0.0.1", 12000))` para iniciar la conexión activa. Una vez completado el *handshake*, consulta el par `(IP, puerto)` efímero que le asignó el sistema operativo mediante `getsockname()`, envía el mensaje codificado en UTF-8 con `sendall()`, espera la respuesta del servidor con `recv(1024)` y cierra su extremo de la comunicación ejecutando `cliente.close()`.

#### Opciones y parámetros de configuración del socket

| Parámetro / Opción | Ubicación en el código | Función |
|---|---|---|
| `AF_INET` | `socket.socket(socket.AF_INET, ...)` (ambos) | Especifica la familia de direcciones de capa de red **IPv4** (direcciones de 32 bits e identificación de extremos mediante pares `(IP, puerto)`). |
| `SOCK_STREAM` | `socket.socket(..., socket.SOCK_STREAM)` (ambos) | Define un socket orientado a flujo continuo de bytes, bidireccional, confiable y orientado a conexión, implementado por el sistema operativo mediante el protocolo **TCP**. |
| `SO_REUSEADDR` | `servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` (servidor) | Configura a nivel de socket (`SOL_SOCKET`) la reutilización de la dirección y puerto locales (`12000`). Permite reiniciar el servidor inmediatamente sin obtener el error `Address already in use` cuando quedan conexiones previas en estado `TIME_WAIT` dentro del kernel. |
| `settimeout(5)` | `cliente.settimeout(5)` (cliente) | Establece un tiempo máximo de espera de 5 segundos para las operaciones bloqueantes del socket (`connect()`, `recv()`, `sendall()`). Si el servidor no responde dentro de ese plazo, lanza una excepción `socket.timeout` (`TimeoutError`) evitando que el proceso quede bloqueado indefinidamente. |

#### Análisis de las llamadas a la API de sockets

1. **`socket()`:** solicita al sistema operativo la creación de un nuevo descriptor de socket en memoria, especificando la familia de red (`AF_INET`) y el tipo de servicio de transporte (`SOCK_STREAM`).
2. **`bind((HOST, PORT))`:** asocia localmente el socket del servidor a la dirección IP `127.0.0.1` y al puerto TCP `12000` en la tabla de sockets del sistema operativo.
3. **`listen(1)`:** marca el socket del servidor como pasivo (estado TCP `LISTEN`) e instruye al kernel para aceptar solicitudes de conexión entrantes (`SYN`) dirigidas al puerto `12000`, encolando hasta 1 conexión pendiente de ser tomada por `accept()`.
4. **`connect((SERVER_IP, SERVER_PORT))`:** inicia de forma activa el establecimiento de la conexión desde el cliente hacia `127.0.0.1:12000`. Bloquea al proceso cliente hasta que se completa el *three-way handshake* (o hasta que falla con `ConnectionRefusedError` si recibe un `RST` o `TimeoutError` si expira el temporizador).
5. **`accept()`:** bloquea al proceso servidor hasta que la cola de conexiones completadas del socket de escucha tiene al menos una sesión en estado `ESTABLISHED`. Extrae esa conexión y devuelve un par `(conexion, direccion_cliente)`.
6. **`sendall(bytes)`:** copia los datos de la aplicación al buffer de envío de TCP en el kernel para su transmisión al extremo remoto, invocando internamente envíos sucesivos hasta asegurar que todos los bytes hayan sido entregados a la pila TCP.
7. **`recv(bufsize)`:** lee hasta `bufsize` bytes (1024 en los scripts) desde el buffer de recepción de TCP mantenido por el sistema operativo. Si aún no hay datos disponibles y la conexión sigue abierta, bloquea al proceso hasta que lleguen bytes o se cierre el flujo.
8. **`close()`:** libera el descriptor de socket del proceso e indica al kernel que no se enviarán más datos por esa conexión; en un socket conectado (`ESTABLISHED` o `CLOSE_WAIT`), esto dispara el envío de un segmento con el flag `FIN`.

#### Aspectos clave de la relación entre la API de sockets y TCP

1. **Por qué `accept()` devuelve un nuevo socket dedicado mientras el original continúa escuchando:**
   En TCP, cada conexión activa se identifica de manera única en el sistema operativo mediante la cuádrupla `(IP_local, puerto_local, IP_remota, puerto_remoto)`. El socket original (`servidor`) sólo está ligado al par local `(127.0.0.1, 12000)` en estado `LISTEN`, cuya única función es recibir segmentos `SYN` de nuevos clientes. Cuando se completa el *three-way handshake*, `accept()` instancia y devuelve un socket distinto (`conexion`, en estado `ESTABLISHED`) asociado a la cuádrupla completa de ese cliente particular (`127.0.0.1:12000 ↔ 127.0.0.1:38512`). De este modo, el servidor utiliza `conexion` para intercambiar datos con ese cliente sin alterar el socket pasivo `servidor`, que permanece en estado `LISTEN` para poder aceptar conexiones adicionales en el puerto `12000`.

2. **Por qué `recv()` devuelve `b""` cuando el extremo remoto cierra ordenadamente su conexión:**
   Dado que TCP transporta un flujo continuo de bytes sin delimitadores de mensajes, la aplicación receptora necesita distinguir entre la ausencia temporal de datos (que hace que `recv()` aguarde bloqueado) y el fin definitivo del flujo (*End-Of-File*, EOF). Cuando el cliente invoca `cliente.close()`, su pila TCP transmite un segmento con el flag `FIN` indicando que no enviará más bytes. Al arribar este segmento `FIN` al servidor, el kernel marca el fin del flujo de entrada en el buffer de recepción y desbloquea la llamada `conexion.recv(1024)` haciendo que retorne inmediatamente la cadena de bytes vacía `b""` (0 bytes). En `tcp_server.py`, el bucle `while conexion.recv(1024): pass` utiliza este valor de retorno vacío (que se evalúa como `False` en Python) para detectar que el cliente cerró su extremo antes de proceder a cerrar el socket del lado servidor.

3. **Por qué las operaciones `socket()`, `bind()` y `listen()` no generan directamente segmentos TCP:**
   Las tres primitivas configuran únicamente estructuras de datos locales dentro del kernel del sistema operativo antes de que exista una contraparte remota:
   - `socket()` sólo reserva el descriptor y la estructura interna del endpoint en memoria.
   - `bind()` registra en el sistema operativo la reserva local del par `(127.0.0.1, 12000)` verificando que no esté ocupado por otro proceso.
   - `listen()` cambia el estado local del socket a `LISTEN` y crea las colas del kernel para gestionar futuros *handshakes*.
   Como en ninguno de estos pasos se especifica una dirección de destino ni hay una conexión activa, no se transmite ningún paquete por la interfaz de red; recién a partir de `listen()` la pila TCP del kernel queda preparada para responder automáticamente con `SYN, ACK` cuando arribe un `SYN`.

4. **Qué sucede a nivel TCP cuando se ejecuta `connect()`:**
   Al ejecutarse `cliente.connect(("127.0.0.1", 12000))`, el sistema operativo del cliente:
   - Selecciona automáticamente una dirección IP local (`127.0.0.1`) y un **puerto efímero** libre (`38512` en la prueba realizada), además de generar un número de secuencia inicial (`ISN`).
   - Envía el primer segmento del *three-way handshake* con el flag `SYN` activado hacia `127.0.0.1:12000` y coloca el socket en estado `SYN_SENT`.
   - Al recibir la respuesta `SYN, ACK` generada por el kernel del servidor, la pila TCP del cliente valida el acuse de recibo (`Ack = ISN_cliente + 1`), envía el tercer segmento con el flag `ACK` (`Ack = ISN_servidor + 1`) y pasa el socket al estado `ESTABLISHED`.
   - Recién cuando se envía ese `ACK` final, `connect()` retorna el control al script `tcp_client.py` (y, al llegar dicho `ACK` al servidor, el kernel desbloquea `accept()` en `tcp_server.py`).

### Ejecución e inspección en Loopback

Se inició la captura en **Wireshark** sobre la interfaz de loopback (`lo`) aplicando el filtro de visualización:

```text
tcp.port == 12000
```

Con la captura activa, se ejecutó primero el servidor en la Terminal A y a continuación el cliente en la Terminal B:

```bash
# Terminal A (Servidor)
python3 TP5/src/tcp_server.py

# Terminal B (Cliente)
python3 TP5/src/tcp_client.py 127.0.0.1 "Hola desde mi programa"
```

#### Salidas obtenidas en las terminales

**Terminal A (`tcp_server.py`):**

```text
[servidor TCP] escuchando en 127.0.0.1:12000 ...
[servidor TCP] conexión aceptada desde 127.0.0.1:38512
[servidor TCP] recibido (22 bytes): 'Hola desde mi programa'
[servidor TCP] respuesta enviada: 'Recibido: Hola desde mi programa'
[servidor TCP] el cliente cerró la conexión
```

**Terminal B (`tcp_client.py`):**

```text
[cliente TCP] conectado a 127.0.0.1:12000 desde 127.0.0.1:38512
[cliente TCP] enviado: 'Hola desde mi programa'
[cliente TCP] respuesta (32 bytes): 'Recibido: Hola desde mi programa'
```

A partir de las salidas registradas se identifican los parámetros de la sesión:

- **Dirección y puerto del servidor:** `127.0.0.1:12000` (fijado explícitamente con `bind()`).
- **Dirección y puerto efímero del cliente:** `127.0.0.1:38512` (asignado dinámicamente por el sistema operativo al invocar `connect()`, observado en el cliente mediante `getsockname()` y en el servidor a través de la tupla devuelta por `accept()`).
- **Bytes transmitidos del cliente al servidor:** **22 bytes**, correspondientes a la codificación UTF-8 de la cadena `'Hola desde mi programa'` (22 caracteres ASCII de 1 byte cada uno).
- **Bytes transmitidos del servidor al cliente:** **32 bytes**, correspondientes a la cadena `'Recibido: Hola desde mi programa'` (los 10 bytes del prefijo `'Recibido: '` sumados a los 22 bytes del mensaje recibido).

#### Inspección del tráfico capturado en Wireshark

Al aplicar el filtro `tcp.port == 12000`, se registraron exactamente **10 segmentos TCP** (paquetes `1` a `10`) que abarcan el ciclo completo de la conexión ([ver captura general de la sesión](./assets/p4_captura_general.png)):

| N.º Paquete | Origen | Destino | Flags TCP | Seq (rel.) | Ack (rel.) | Len (payload) | Etapa de la comunicación |
|---|---|---|---|---|---|---|---|
| **1** | `127.0.0.1:38512` | `127.0.0.1:12000` | `[SYN]` (`0x002`) | `0` | — | `0 B` | Inicio del *three-way handshake* (cliente → servidor) |
| **2** | `127.0.0.1:12000` | `127.0.0.1:38512` | `[SYN, ACK]` (`0x012`) | `0` | `1` | `0 B` | Respuesta del *three-way handshake* (servidor → cliente) |
| **3** | `127.0.0.1:38512` | `127.0.0.1:12000` | `[ACK]` (`0x010`) | `1` | `1` | `0 B` | Confirmación del *three-way handshake* (cliente → servidor) |
| **4** | `127.0.0.1:38512` | `127.0.0.1:12000` | `[PSH, ACK]` (`0x018`) | `1` | `1` | `22 B` | Envío del mensaje `'Hola desde mi programa'` |
| **5** | `127.0.0.1:12000` | `127.0.0.1:38512` | `[ACK]` (`0x010`) | `1` | `23` | `0 B` | Confirmación TCP de los 22 bytes recibidos por el servidor |
| **6** | `127.0.0.1:12000` | `127.0.0.1:38512` | `[PSH, ACK]` (`0x018`) | `1` | `23` | `32 B` | Envío de la respuesta `'Recibido: Hola desde mi programa'` |
| **7** | `127.0.0.1:38512` | `127.0.0.1:12000` | `[ACK]` (`0x010`) | `23` | `33` | `0 B` | Confirmación TCP de los 32 bytes recibidos por el cliente |
| **8** | `127.0.0.1:38512` | `127.0.0.1:12000` | `[FIN, ACK]` (`0x011`) | `23` | `33` | `0 B` | Solicitud de cierre iniciada por el cliente |
| **9** | `127.0.0.1:12000` | `127.0.0.1:38512` | `[FIN, ACK]` (`0x011`) | `33` | `24` | `0 B` | Confirmación del `FIN` del cliente y cierre del servidor |
| **10** | `127.0.0.1:38512` | `127.0.0.1:12000` | `[ACK]` (`0x010`) | `24` | `34` | `0 B` | Confirmación final del cierre por parte del cliente |

A continuación se detalla cada fase observada en las capturas:

1. **Establecimiento de la conexión (*Three-way handshake*, paquetes 1 a 3):**
   - **Paquete 1 (`[SYN]`):** el cliente (`38512`) envía un segmento con el flag `SYN` activado (`Flags: 0x002`), número de secuencia inicial relativo `Seq=0` (*raw* `1424810866`), `Len=0` y opciones de negociación (`MSS=65495`, `SACK_PERM`, `WS=1024`) hacia el puerto `12000` ([ver captura del paquete 1](./assets/p4_handshake_syn.png)).
   - **Paquete 2 (`[SYN, ACK]`):** el kernel del servidor (`12000`) responde al puerto `38512` con los flags `SYN` y `ACK` activados (`Flags: 0x012`), anunciando su propio número de secuencia inicial `Seq=0` (*raw* `3312352991`) y confirmando el `SYN` del cliente con `Ack=1` (*raw* `1424810867`) ([ver captura del paquete 2](./assets/p4_handshake_syn_ack.png)).
   - **Paquete 3 (`[ACK]`):** el cliente (`38512`) completa el *handshake* enviando un segmento con el flag `ACK` (`Flags: 0x010`), `Seq=1`, `Ack=1` y `Len=0` ([ver captura del paquete 3](./assets/p4_handshake_ack.png)). En este punto la conexión queda establecida en ambos extremos.

2. **Transmisión del mensaje del cliente al servidor (paquetes 4 y 5):**
   - **Paquete 4 (`[PSH, ACK]`):** el cliente transmite desde el puerto `38512` al `12000` un segmento con `Flags: 0x018 (PSH, ACK)`, `Seq=1`, `Ack=1` y una carga útil de `TCP Segment Len: 22` (longitud total de trama de 88 bytes en `lo`). En el panel de detalles y en el volcado hexadecimal/ASCII se observa el campo `Data (22 bytes)` con los bytes `48 6f 6c 61 20 64 65 73 64 65 20 6d 69 20 70 72 6f 67 72 61 6d 61`, correspondientes al texto `'Hola desde mi programa'` ([ver captura del paquete 4](./assets/p4_datos_cliente.png)). El flag `PSH` solicita que la pila receptora entregue los datos de inmediato a la aplicación.
   - **Paquete 5 (`[ACK]`):** la pila TCP del servidor (`12000 → 38512`) confirma automáticamente la recepción de los 22 bytes enviando un segmento con `Flags: 0x010 (ACK)`, `Seq=1`, `Ack=23` (`1 + 22`) y `Len=0` ([ver captura del paquete 5](./assets/p4_ack_servidor.png)).

3. **Respuesta del servidor al cliente (paquetes 6 y 7):**
   - **Paquete 6 (`[PSH, ACK]`):** el servidor transmite desde el puerto `12000` hacia el `38512` un segmento con `Flags: 0x018 (PSH, ACK)`, `Seq=1`, `Ack=23` y `TCP Segment Len: 32` (98 bytes totales en `lo`). El campo `Data (32 bytes)` contiene la cadena `'Recibido: Hola desde mi programa'` (`52 65 63 69 62 69 64 6f 3a 20 ...`) ([ver captura del paquete 6](./assets/p4_respuesta_servidor.png)).
   - **Paquete 7 (`[ACK]`):** el kernel del cliente (`38512 → 12000`) confirma los 32 bytes recibidos mediante un segmento con `Flags: 0x010 (ACK)`, `Seq=23`, `Ack=33` (`1 + 32`) y `Len=0` ([ver captura del paquete 7](./assets/p4_ack_cliente.png)).

4. **Cierre de la conexión TCP (paquetes 8 a 10):**
   - **Paquete 8 (`[FIN, ACK]`):** al ejecutarse `cliente.close()`, el cliente (`38512 → 12000`) inicia el cierre activo enviando un segmento con `Flags: 0x011 (FIN, ACK)`, `Seq=23`, `Ack=33` y `Len=0` ([ver captura del paquete 8](./assets/p4_cierre_fin_cliente.png)).
   - **Paquete 9 (`[FIN, ACK]`):** la llegada del `FIN` del cliente hace que `conexion.recv(1024)` en el servidor retorne `b""`, saliendo del bucle `while` y ejecutando inmediatamente `conexion.close()`. Debido a que el cierre del servidor ocurre de forma inmediata en loopback, el kernel del servidor combina en un solo segmento (`12000 → 38512`) el acuse del `FIN` del cliente (`Ack=24`, ya que el flag `FIN` consume un número de secuencia) y su propio indicador de finalización (`Seq=33`, `Flags: 0x011 (FIN, ACK)`) ([ver captura del paquete 9](./assets/p4_cierre_fin_servidor.png)).
   - **Paquete 10 (`[ACK]`):** el kernel del cliente (`38512 → 12000`) envía la confirmación final con `Flags: 0x010 (ACK)`, `Seq=24`, `Ack=34` (`33 + 1`) y `Len=0`, dando por concluido el cierre de la conexión ([ver captura del paquete 10](./assets/p4_cierre_ack_final.png)).

### Tabla de primitivas de sockets vs. tráfico de red

La siguiente tabla relaciona cada llamada a la API de sockets presente en `tcp_server.py` y `tcp_client.py` con su ubicación de ejecución, su comportamiento respecto a la red y los segmentos observados en la captura:

| Llamada | ¿Dónde se ejecuta? | ¿Genera tráfico? | Segmentos observados |
|---|---|---|---|
| `socket()` | Ambos (servidor y cliente) | No (operación local del SO) | Ninguno. Reserva localmente el descriptor y la estructura del socket en el kernel. |
| `bind()` | Servidor | No (operación local del SO) | Ninguno. Asocia localmente el socket a `127.0.0.1:12000`. |
| `listen()` | Servidor | No (operación local del SO) | Ninguno al ejecutarse. Pone el socket en estado `LISTEN`, habilitando al kernel del servidor para responder con el **Paquete 2** (`[SYN, ACK]`) cuando arriba un `[SYN]`. |
| `connect()` | Cliente | Sí | **Paquete 1** (`38512 → 12000`, `[SYN]`) enviado por el cliente; desencadena el **Paquete 2** (`12000 → 38512`, `[SYN, ACK]`) del kernel del servidor y el **Paquete 3** (`38512 → 12000`, `[ACK]`) del cliente que completa el *three-way handshake*. |
| `accept()` | Servidor | No (operación local del SO) | Ninguno generado directamente. Permanece bloqueada y retorna el nuevo socket `conexion` (`127.0.0.1:12000 ↔ 127.0.0.1:38512`) una vez que el kernel recibe el **Paquete 3** (`[ACK]`) que completa el *handshake*. |
| `sendall()` | Ambos (cliente y servidor) | Sí | En el cliente (`cliente.sendall()`): **Paquete 4** (`38512 → 12000`, `[PSH, ACK]`, `Len=22`). En el servidor (`conexion.sendall()`): **Paquete 6** (`12000 → 38512`, `[PSH, ACK]`, `Len=32`). *(Nota: los acuses **Paquete 5** `[ACK]` y **Paquete 7** `[ACK]` los envía automáticamente la pila TCP del extremo receptor al recibir los paquetes 4 y 6).* |
| `recv()` | Ambos (servidor y cliente) | No (operación local del SO) | Ninguno. Consume datos que ya fueron recibidos, confirmados y almacenados en el buffer de recepción del SO: en el servidor extrae los 22 bytes del **Paquete 4** (y en el bucle final retorna `b""` al haberse recibido el **Paquete 8** `[FIN, ACK]`); en el cliente extrae los 32 bytes del **Paquete 6**. |
| `close()` | Ambos (cliente y servidor) | Sí (en sockets conectados) / No (en el socket de escucha) | En el cliente (`cliente.close()`): genera el **Paquete 8** (`38512 → 12000`, `[FIN, ACK]`). En el servidor (`conexion.close()`): genera el **Paquete 9** (`12000 → 38512`, `[FIN, ACK]`), que es confirmado automáticamente por el kernel del cliente con el **Paquete 10** (`38512 → 12000`, `[ACK]`). El cierre del socket pasivo (`servidor.close()`) es una operación local que libera el puerto `12000` sin emitir segmentos. |

Como se observa en la tabla, no existe una relación uno a uno entre las llamadas a la API y los segmentos TCP en la red:

- Las primitivas de configuración inicial (`socket()`, `bind()`, `listen()`) y de lectura o desencolado (`accept()`, `recv()`) operan sobre estructuras y buffers locales del kernel sin transmitir paquetes propios.
- Los segmentos de confirmación pura (**Paquete 5** `[ACK]`, **Paquete 7** `[ACK]` y **Paquete 10** `[ACK]`) así como la respuesta **Paquete 2** (`[SYN, ACK]`) son emitidos de forma autónoma por la pila TCP del sistema operativo al procesar segmentos entrantes, independientemente del instante en que el proceso de usuario invoque `recv()` o `accept()`.
- Una llamada a `sendall()` entrega un bloque de bytes al buffer de salida de TCP; aunque en esta experiencia cada mensaje pequeño (22 y 32 bytes) viajó en un único segmento `[PSH, ACK]`, para volúmenes de datos mayores la pila TCP puede fragmentar el flujo en múltiples segmentos o agrupar escrituras sucesivas según el MSS y la ventana disponible.

---

## Conclusión

<!-- 
Sección a completar al finalizar todas las partes de la práctica.
-->

---

## Referencias

<!-- 
Bibliografía y fuentes consultadas.
-->
