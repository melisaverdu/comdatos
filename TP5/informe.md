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
      - [a) ¿Qué significa "establecer una conexión"? ¿Dónde "existe" una conexión TCP (cables, routers o extremos)?](#a-qué-significa-establecer-una-conexión-dónde-existe-una-conexión-tcp-cables-routers-o-extremos)
      - [b) ¿Qué es un puerto? ¿Qué identifica el par (IP, puerto)?](#b-qué-es-un-puerto-qué-identifica-el-par-ip-puerto)
      - [c) ¿Qué significa que un proceso esté "escuchando" en un puerto?](#c-qué-significa-que-un-proceso-esté-escuchando-en-un-puerto)
    - [Experimento TCP en Loopback](#experimento-tcp-en-loopback)
    - [Experimento UDP en Loopback](#experimento-udp-en-loopback)
    - [Comparación detallada TCP vs. UDP](#comparación-detallada-tcp-vs-udp)
      - [a) ¿Qué pasó en la red cuando ejecutaron el comando del cliente, antes de escribir el primer mensaje? Compárenlo con TCP.](#a-qué-pasó-en-la-red-cuando-ejecutaron-el-comando-del-cliente-antes-de-escribir-el-primer-mensaje-compárenlo-con-tcp)
      - [b) ¿Cuántos datagramas generó cada mensaje? ¿Hay algo parecido a un ACK?](#b-cuántos-datagramas-generó-cada-mensaje-hay-algo-parecido-a-un-ack)
      - [c) Comparen el encabezado UDP con el encabezado TCP de un segmento con datos: ¿qué campos tiene cada uno? ¿Cuántos bytes ocupa cada encabezado?](#c-comparen-el-encabezado-udp-con-el-encabezado-tcp-de-un-segmento-con-datos-qué-campos-tiene-cada-uno-cuántos-bytes-ocupa-cada-encabezado)
      - [d) ¿Qué pasó en la red al cerrar el cliente con Ctrl+C? ¿Y en TCP?](#d-qué-pasó-en-la-red-al-cerrar-el-cliente-con-ctrlc-y-en-tcp)
      - [e) Para enviar la misma frase, ¿cuántos paquetes necesitaron en total con TCP y cuántos con UDP? ¿Qué "compran" con los paquetes extra de TCP?](#e-para-enviar-la-misma-frase-cuántos-paquetes-necesitaron-en-total-con-tcp-y-cuántos-con-udp-qué-compran-con-los-paquetes-extra-de-tcp)
      - [f) ¿Y si nadie escucha? Con Wireshark capturando en loopback y el filtro `tcp.port == 12000 || udp.port == 12001 || icmp`, sin servidores corriendo:](#f-y-si-nadie-escucha-con-wireshark-capturando-en-loopback-y-el-filtro-tcpport--12000--udpport--12001--icmp-sin-servidores-corriendo)
  - [Servidor TCP mínimo](#servidor-tcp-mínimo)
    - [Análisis de sockets TCP y correlación código-red](#análisis-de-sockets-tcp-y-correlación-código-red)
    - [Ejecución e inspección en Loopback](#ejecución-e-inspección-en-loopback)
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

#### a) ¿Qué significa "establecer una conexión"? ¿Dónde "existe" una conexión TCP (cables, routers o extremos)?
Establecer una conexión implica que dos extremos ejecutan un procedimiento previo de señalización y sincronización antes de transferir datos. En TCP, esto se realiza mediante el acuerdo en tres fases (*Three-Way Handshake*: SYN, SYN-ACK, ACK), donde cliente y servidor sincronizan sus números de secuencia iniciales (ISN), acuerdan opciones como el MSS y asignan buffers y variables de control en el sistema operativo.

La conexión TCP es puramente **lógica** y reside exclusivamente en los **extremos terminales** (en las entidades TCP de los hosts). La infraestructura intermedia (routers y switches) no mantiene ningún estado de la conexión ni es consciente de ella; opera en capas inferiores conmutando y reenviando datagramas IP independientes.

#### b) ¿Qué es un puerto? ¿Qué identifica el par (IP, puerto)?
Un **puerto** es un identificador numérico de 16 bits (0 a 65535) en la capa de transporte (denominado TSAP según Tanenbaum) cuyo fin es la **multiplexación y demultiplexación**: permite que múltiples procesos en un mismo host compartan la interfaz de red, entregando cada segmento entrante al socket correspondiente.

El par **(IP, puerto)** identifica de manera unívoca un **socket** o punto final (*endpoint*) de comunicación en la red: la IP direcciona al host y el puerto al proceso o servicio local. Una conexión TCP establecida queda luego unívocamente individualizada por la 4-tupla $(\text{IP}_{\text{orig}}, \text{Puerto}_{\text{orig}}, \text{IP}_{\text{dest}}, \text{Puerto}_{\text{dest}})$.

#### c) ¿Qué significa que un proceso esté "escuchando" en un puerto?
Significa que un proceso ha instanciado un socket, lo ha vinculado a un puerto mediante `bind()` y lo ha puesto en modo pasivo mediante la primitiva `listen()`. En este estado, el proceso no emite datos activamente; la pila TCP del sistema operativo queda a la espera de solicitudes entrantes de conexión (SYN) dirigidas a ese puerto y las encola hasta que la aplicación las procese con `accept()`.


### Experimento TCP en Loopback

Para analizar el comportamiento de TCP en la interfaz de bucle invertido (*loopback* `lo`), se ejecutó una sesión cliente-servidor utilizando `ncat` en el puerto `12000`, monitoreando el tráfico con Wireshark mediante el filtro `tcp.port == 12000`.

1. **Servidor pasivo (en escucha):**
   ```bash
   ncat -v -l 12000
   ```
2. **Cliente activo:**
   ```bash
   ncat -v 127.0.0.1 12000
   ```

Una vez establecida la conexión, se transmitieron mensajes de texto bidireccionales y finalmente se terminó la sesión enviando una señal de interrupción (`Ctrl + C`) desde el cliente.

| Terminal Servidor | Terminal Cliente |
| :---: | :---: |
| ![Consola Servidor TCP](assets/punto3_tcp_servidor.png) | ![Consola Cliente TCP](assets/punto3_tcp_cliente.png) |

A nivel de red, la captura en Wireshark evidencia las tres etapas fundamentales del ciclo de vida de una conexión TCP orientada a la conexión:

![Captura Wireshark de la sesión TCP en Loopback](assets/punto3_tcp_wireshark.png)

1. **Establecimiento de conexión (*Three-Way Handshake*):**
   - **Segmento 1 (`SYN`):** El cliente (`127.0.0.1:41024`) envía un flag `SYN` con un Número de Secuencia Inicial aleatorio (`Seq=0` relativo, ISN = `3013143511`), solicitando sincronización y negociando opciones como MSS (`65495`), SACK permitido, Timestamps y escala de ventana (`WS=1024`).
   - **Segmento 2 (`SYN, ACK`):** El servidor (`127.0.0.1:12000`) responde con sus flags `SYN` y `ACK`, asignando su propio ISN (`Seq=0` relativo, ISN = `480945039`) y confirmando la recepción del cliente (`Ack=1` relativo, `3013143512`).
   - **Segmento 3 (`ACK`):** El cliente confirma la recepción (`Seq=1 Ack=1`, raw: `Seq=3013143512`, `Ack=480945040`), quedando la conexión formalmente en estado `ESTABLISHED`.
2. **Transferencia de datos confiable:**
   - Cada línea de texto enviada viaja en un segmento con flags `[PSH, ACK]`, indicando a la capa de transporte receptora que entregue los datos de inmediato a la aplicación sin esperar a llenar el buffer.
   - Cada segmento de datos es seguido inmediatamente por un segmento de confirmación pura `[ACK]` sin payload (`Len=0`) generado por el receptor, validando la entrega confiable y actualizando el control de flujo.
3. **Finalización de la conexión (*Teardown*):**
   - Al pulsar `Ctrl + C` en el cliente, la aplicación cierra su socket y el sistema operativo emite un segmento `[FIN, ACK]`.
   - El servidor responde confirmando la recepción y cerrando su extremo con `[FIN, ACK]`, y el cliente emite el último `[ACK]`, concluyendo el cierre ordenado de la sesión.

---

### Experimento UDP en Loopback

En contraposición, se evaluó el protocolo de datagramas de usuario (UDP) bajo el mismo esquema en el puerto `12001`, aplicando en Wireshark el filtro `udp.port == 12001`.

1. **Receptor UDP:**
   ```bash
   ncat -v -u -l 12001
   ```
2. **Emisor UDP:**
   ```bash
   ncat -v -u 127.0.0.1 12001
   ```

Se enviaron las mismas 6 frases interactivas en ambos sentidos y se interrumpió la ejecución mediante `Ctrl + C`.

| Terminal Servidor UDP | Terminal Cliente UDP |
| :---: | :---: |
| ![Consola Servidor UDP](assets/punto3_udp_servidor.png) | ![Consola Cliente UDP](assets/punto3_udp_cliente.png) |

La captura de tráfico evidencia las características de un servicio no orientado a la conexión y no confiable:

![Captura Wireshark de la sesión UDP en Loopback](assets/punto3_udp_wireshark.png)

- **Ausencia de señalización previa:** El cliente no emite ningún paquete de saludo ni sincronización al iniciar el proceso; el primer paquete en circular por la red es el que ya contiene el primer mensaje de aplicación (`"Hola Servidor UDP\n"`).
- **Transmisión de datagramas independientes:** Cada mensaje viaja encapsulado en un único datagrama UDP aislado. No existe ningún segmento de asentimiento (`ACK`) de retorno por parte del receptor. *(Nota: en la columna Protocol de Wireshark se visualiza `LLC` debido a que el disector heurístico intenta interpretar el payload sobre el puerto 12001, observándose en el árbol inferior el encabezado `User Datagram Protocol` completo).*
- **Terminación sin aviso:** Al presionar `Ctrl + C`, el proceso simplemente finaliza en el espacio de usuario. En la red no se genera ningún paquete de notificación ni cierre; la comunicación concluye en silencio absoluto.

---

### Comparación detallada TCP vs. UDP

A partir de los experimentos prácticos y las capturas obtenidas en Wireshark, se analizan y responden las preguntas de la consigna:

#### a) ¿Qué pasó en la red cuando ejecutaron el comando del cliente, antes de escribir el primer mensaje? Compárenlo con TCP.
- **En UDP:** Al ejecutar `ncat -v -u 127.0.0.1 12001`, antes de escribir el primer mensaje **no circuló ningún paquete en la red**. UDP carece de estado y de fase de establecimiento de conexión; la red permanece en reposo hasta que el usuario escribe un mensaje y presiona `Enter`.
- **Comparación con TCP:** En TCP, apenas se ejecuta `ncat -v 127.0.0.1 12000` (antes de escribir cualquier texto), se intercambian de inmediato en la red los **3 paquetes del *Three-Way Handshake*** (`[SYN]`, `[SYN, ACK]` y `[ACK]`).

#### b) ¿Cuántos datagramas generó cada mensaje? ¿Hay algo parecido a un ACK?
- **En UDP:** Cada mensaje escrito generó **1 único datagrama** (6 datagramas en total para los 6 mensajes). No existe ningún paquete de confirmación o `ACK`.
- **En TCP:** Cada mensaje enviado generó **2 paquetes**: el segmento de datos con flags `[PSH, ACK]` y el segmento inmediato de confirmación `[ACK]` (`Len=0`) en sentido inverso.

#### c) Comparen el encabezado UDP con el encabezado TCP de un segmento con datos: ¿qué campos tiene cada uno? ¿Cuántos bytes ocupa cada encabezado?
A partir de la inspección del panel de detalles de Wireshark en las capturas obtenidas (ambos paquetes seleccionados transportando los 18 bytes de `"Hola Servidor ...\n"`):

| Característica | Encabezado TCP | Encabezado UDP |
| :--- | :--- | :--- |
| **Tamaño del encabezado** | **32 bytes**<br>Visible en `1000 .... = Header Length: 32 bytes (8)` (que incluye 12 bytes del campo `Options`). | **8 bytes**<br>Visible al restar al campo `Length: 26` los `18 bytes` de `UDP payload (18 bytes)`. |
| **Campos observados en la captura** | • `Source Port: 41024`<br>• `Destination Port: 12000`<br>• `Sequence Number: 1` (raw: `3013143512`)<br>• `Acknowledgment Number: 1` (raw: `480945040`)<br>• `Header Length: 32 bytes (8)`<br>• `Flags: 0x018 (PSH, ACK)`<br>• `Window: 64` (`[Calculated window size: 65536]`)<br>• `Checksum: 0xfe3a`<br>• `Urgent Pointer: 0`<br>• `Options: (12 bytes), No-Operation (NOP), No-Operation (NOP), Timestamps` | • `Source Port: 36095`<br>• `Destination Port: 12001`<br>• `Length: 26`<br>• `Checksum: 0xfe2d` |

#### d) ¿Qué pasó en la red al cerrar el cliente con Ctrl+C? ¿Y en TCP?
- **En UDP:** El cierre es **completamente silencioso**: al presionar `Ctrl+C` no se genera ningún paquete en la red y el servidor siquiera se entera de que el cliente finalizó.
- **En TCP:** Al presionar `Ctrl+C` se enviaron **3 paquetes de cierre (*Teardown*)**: el cliente envía `[FIN, ACK]`, el servidor responde `[FIN, ACK]` y el cliente confirma con `[ACK]`, cerrándose también el proceso servidor.

#### e) Para enviar la misma frase, ¿cuántos paquetes necesitaron en total con TCP y cuántos con UDP? ¿Qué "compran" con los paquetes extra de TCP?
- **Para una frase individual:** UDP necesita **1 paquete**, mientras que TCP utiliza **2 paquetes** (`[PSH, ACK]` + `[ACK]`), más los **3 paquetes** iniciales del *Handshake* y los **3 paquetes** finales del *Teardown* (8 paquetes para una sesión de una sola frase). En nuestra prueba de 6 frases totales (3 de ida y 3 de vuelta), **UDP necesitó 6 paquetes en total** frente a **18 paquetes en total de TCP** (3 de handshake + 12 de transferencia + 3 de cierre).
- **¿Qué se "compra" con los paquetes extra de TCP?**  
  Se compra **confiabilidad y control de la comunicación**: confirmación de recepción (`ACK`) y retransmisión ante pérdidas, ordenamiento secuencial de los datos (`Seq`), control de flujo (`Window`) y gestión de sesión (apertura y cierre formal).

#### f) ¿Y si nadie escucha? Con Wireshark capturando en loopback y el filtro `tcp.port == 12000 || udp.port == 12001 || icmp`, sin servidores corriendo:
Al ejecutar los clientes hacia puertos donde no hay ningún proceso escuchando:

| Terminal Ejecución | Wireshark Puertos Cerrados |
| :---: | :---: |
| ![Consola Puertos Cerrados](assets/punto3_cerrados.png) | ![Wireshark Puertos Cerrados](assets/punto3_cerrados_wireshark.png) |

1. **En TCP (`ncat -v 127.0.0.1 12000` con puerto cerrado):**
   - Apenas se ejecuta el comando, el cliente (`52590`) envía un segmento `[SYN]` para abrir la conexión.
   - La pila TCP del sistema operativo destino comprueba que ningún socket está en estado `LISTEN` en el puerto `12000` y responde de inmediato con un segmento con flags **`[RST, ACK]`** (*Reset*).
   - **Mecanismo:** El rechazo se resuelve dentro de la **misma Capa de Transporte**, abortando la conexión en el acto y mostrando `Ncat: Connection refused.` en la consola.
2. **En UDP (`ncat -v -u 127.0.0.1 12001` con puerto cerrado):**
   - Al ejecutar el comando, `ncat` muestra `Ncat: Connected to 127.0.0.1:12001.` y **no se envía ningún paquete a la red** porque UDP no tiene handshake.
   - Recién cuando se escribe el texto (`Hola`) y se presiona `Enter`, el cliente transmite el datagrama UDP hacia el puerto `12001`.
   - Al llegar a destino, el sistema operativo comprueba que no existe ningún socket UDP asociado al puerto `12001`. Al carecer UDP de flags o paquetes de control propios, la notificación es delegada a la **Capa de Red**, que emite un mensaje **ICMP Destination unreachable (Port unreachable)** (Tipo 3, Código 3), provocando que `ncat` imprima `Ncat: Connection refused.` y finalice el proceso.

---

## Servidor TCP mínimo

### Análisis de sockets TCP y correlación código-red

<!-- 
- Tabla de primitivas de Sockets (socket, bind, listen, connect, accept, sendall, recv, close):
  * Dónde se ejecuta (cliente / servidor / ambos).
  * ¿Genera tráfico de red o es operación local del SO?
  * Segmentos y flags observados en Wireshark (SYN, SYN-ACK, ACK, PSH-ACK, FIN-ACK).
- Relación entre código en Python y eventos en la red (creación de socket dedicado en accept, detección de FIN con recv retornando b"").
-->

### Ejecución e inspección en Loopback

<!-- 
- Ejecución de tcp_server.py y tcp_client.py en loopback (127.0.0.1:12000).
- Captura de Wireshark con filtro tcp.port == 12000.
- Registro de salidas de consola y trazabilidad con los paquetes capturados.
-->

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
