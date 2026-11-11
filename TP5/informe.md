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

<!-- Respuesta a) -->

#### a) ¿Qué es ICMP y para qué se usa?

ICMP (Internet Control Message Protocol, RFC 792) es el protocolo de control y diagnóstico de la pila TCP/IP. Lo usan los hosts y routers para avisar de errores y para hacer consultas sobre la red. Sus principales usos son:

- **Mensajes de error:** Destination Unreachable (red, host o puerto inalcanzable), Time Exceeded (el TTL llegó a 0, que es lo que usa `traceroute`) y Redirect.
- **Mensajes de consulta:** Echo Request y Echo Reply, que son los que usa `ping`.

No transporta datos de aplicaciones ni ofrece servicio de transporte: no tiene puertos y solo lleva información sobre la red.

<!-- Respuesta b) -->

#### b) Relación entre ICMP e IP

ICMP viaja dentro de IP: el mensaje ICMP va como payload de un datagrama IPv4. Aun así se lo considera parte de la capa de red, porque su función es dar soporte a IP y no a las aplicaciones.

El receptor sabe qué hay adentro por el campo **Protocol** del encabezado IPv4. **Protocol = 1** significa ICMP.

<!-- Respuesta c) -->

#### c) Ping, Echo Request y Echo Reply

`ping` comprueba si un host es alcanzable a nivel de IP. Envía un **Echo Request** y espera el **Echo Reply** que devuelve el destino; con eso mide el tiempo de ida y vuelta (RTT) y el porcentaje de paquetes perdidos.

- **Echo Request:** el emisor le pide al destino que le devuelva el mensaje.
- **Echo Reply:** el destino responde devolviendo el mismo identificador, número de secuencia y datos.

Para distinguirlos se usan los siguientes campos:

- **Type:** 8 es Echo Request y 0 es Echo Reply. **Code** vale 0 en ambos.
- **Identifier:** identifica el proceso `ping` que envió el mensaje, por si hay varios corriendo a la vez.
- **Sequence number:** permite emparejar cada Request con su Reply y detectar pérdidas o desorden.

<!-- Respuesta d) -->

#### d) Información mínima de un mensaje ICMP Echo

Tiene un encabezado de **8 bytes** seguido de los datos:

|Campo|Tamaño|
|-----|-------|
|Type (8 o 0)|1 byte|
|Code (0)|1 byte|
|Checksum|2 bytes|
|Identifier|2 bytes|
|Sequence number|2 bytes|
|Data (payload, opcional)|variable|

### Configuración de red y captura de tráfico

<!-- 
Configuración de red local:
- IPv4, máscara, gateway por defecto y dirección MAC (ip addr / ip route / ipconfig).
- Capturas en Wireshark: ping al gateway y ping a 8.8.8.8.
- Filtros utilizados: icmp, icmp.type == 8, icmp.type == 0, icmp && ip.addr == 8.8.8.8.
-->

La configuración de red se obtuvo con `ip addr` e `ip route` en la computadora con Linux, conectada por Wi-Fi (interfaz `wlp1s0`):

|Parámetro|Valor|
|---------|-----|
|Dirección IPv4|192.168.1.64|
|Máscara|/24 (255.255.255.0)|
|Gateway por defecto|192.168.1.1|
|Dirección MAC|00:45:e2:09:bf:09|

![Configuración de red con ip addr e ip route](./assets/p1_ip_addr_route.png)

Con Wireshark capturando en `wlp1s0`, se hizo ping al gateway y a 8.8.8.8 (4 paquetes cada uno). Todos los pings recibieron respuesta:

![Ping al gateway y a 8.8.8.8 desde la terminal](./assets/p1_ping_terminal.png)

Luego se detuvo la captura y se aplicaron los filtros pedidos. Con `icmp` quedan 16 paquetes: un Request y su Reply por cada ping, primero con el gateway (paquetes 212 a 232) y después con 8.8.8.8 (paquetes 267 a 287). La captura de pantalla muestra los primeros 15; el último Reply (287) aparece en las capturas de los filtros siguientes:

![Filtro icmp](./assets/p1_filtro_icmp.png)

Con `icmp.type == 8` quedan solo los 8 Echo Request, todos con origen 192.168.1.64:

![Filtro icmp.type == 8](./assets/p1_filtro_request.png)

Con `icmp.type == 0` quedan solo los 8 Echo Reply, todos con destino 192.168.1.64:

![Filtro icmp.type == 0](./assets/p1_filtro_reply.png)

Con `icmp && ip.addr == 8.8.8.8` queda el intercambio con 8.8.8.8 en ambos sentidos:

![Filtro icmp && ip.addr == 8.8.8.8](./assets/p1_filtro_8888.png)

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

La siguiente tabla corresponde al Echo Request **267**, enviado a 8.8.8.8:

|Capa|Origen|Destino|Campo que indica protocolo|
|----|------|-------|-------------------------|
|Ethernet II|00:45:e2:09:bf:09|f0:c4:78:ba:88:40|Type: IPv4 (0x0800)|
|Internet Protocol Version 4|192.168.1.64|8.8.8.8|Protocol: ICMP (1)|
|Internet Control Message Protocol|—|—|— (los datos van directo como payload)|
|Datos / payload|—|—|—|

ICMP no tiene direcciones propias: el mensaje se identifica con Type 8 / Code 0 y con el Identifier `0x615b` (24923), pero esos campos no indican ningún protocolo superior.

Aunque la captura se hizo sobre Wi-Fi (`wlp1s0`), Wireshark muestra la capa de enlace como **Ethernet II** y no como 802.11. Esto se debe a que, fuera del modo monitor, el driver de la placa inalámbrica convierte las tramas 802.11 al formato Ethernet II antes de entregárselas al sistema operativo, así que Wireshark recibe tramas con encabezado Ethernet de 14 bytes.

<!-- Respuesta a) -->

#### a) MAC destino del Echo Request a 8.8.8.8

La MAC destino del Echo Request enviado a 8.8.8.8 (paquete 267) es `f0:c4:78:ba:88:40` (Wireshark la muestra como `HuaweiTechno_ba:88:40`), que **no es la MAC de 8.8.8.8** sino la del **router (gateway por defecto)** de nuestra red. En el intercambio con el gateway (192.168.1.1) aparece exactamente la misma MAC: es la MAC destino de los Request y la MAC origen de los Reply.

![MAC destino del Echo Request a 8.8.8.8](./assets/p1_mac_destino_8888.png)

![MAC del gateway en el intercambio con 192.168.1.1](./assets/p1_mac_gateway.png)

Esto ocurre porque 8.8.8.8 no pertenece a nuestra subred: el sistema operativo consulta la tabla de rutas, ve que el paquete debe salir por el gateway y arma la trama Ethernet dirigida a la MAC del router. La IP destino, en cambio, sigue siendo 8.8.8.8.

**Conclusión:** la dirección MAC tiene **alcance local** (un solo salto, dentro del mismo enlace) y se reescribe en cada router del camino. La dirección IP tiene **alcance extremo a extremo**: identifica al origen y al destino final y se mantiene durante todo el recorrido.

<!-- Respuesta b) -->

#### b) Comparación Echo Request vs. Echo Reply

Wireshark vincula cada Request con su Reply mediante el campo `[Response frame: …]`: por ejemplo, el Request 267 a 8.8.8.8 se responde en el paquete 268, y el Request 212 al gateway en el 213. Se compararon los bytes de los paquetes 212 y 213 en el panel hexadecimal (capturas de los filtros `icmp.type == 8` e `icmp.type == 0`):

|Capa|Campo|Request (212)|Reply (213)|
|----|-----|-------------|-----------|
|Ethernet II|MAC origen|00:45:e2:09:bf:09|f0:c4:78:ba:88:40|
|Ethernet II|MAC destino|f0:c4:78:ba:88:40|00:45:e2:09:bf:09|
|Ethernet II|Type|0x0800|0x0800|
|IPv4|Total length|84|84|
|IPv4|Identification|0xbb5f|0x222f|
|IPv4|Flags|0x40 (Don't fragment)|0x00|
|IPv4|TTL|64|64|
|IPv4|Protocol|1 (ICMP)|1 (ICMP)|
|IPv4|Header checksum|0xfbb7|0xd4e8|
|IPv4|IP origen|192.168.1.64|192.168.1.1|
|IPv4|IP destino|192.168.1.1|192.168.1.64|
|ICMP|Type|8 (Echo Request)|0 (Echo Reply)|
|ICMP|Code|0|0|
|ICMP|Checksum|0xc1ef|0xc9ef|
|ICMP|Identifier|0x615a|0x615a|
|ICMP|Sequence number|1|1|
|ICMP|Data|56 bytes|56 bytes (idénticos)|

En resumen:

|Capa|Campos que cambian|Campos que se mantienen|
|----|------------------|-----------------------|
|Ethernet II|MAC origen y MAC destino (se invierten)|Type: IPv4 (0x0800)|
|IPv4|IP origen y IP destino (se invierten), Identification, Flags, Header checksum y, con 8.8.8.8, también el TTL (64 → 118)|Version, Header length, Total length, Protocol: ICMP (1)|
|ICMP|Type (8 → 0), Checksum|Code (0), Identifier, Sequence number, Data|

Justificación de cada cambio:

- **Direcciones MAC e IP:** la respuesta viaja en sentido contrario, por lo que origen y destino se intercambian.
- **TTL:** lo fija el sistema que genera cada paquete (cada SO usa su propio valor inicial) y lo decrementa cada router del camino. Con el gateway coincide (ambos usan 64 y no hay routers en el medio), pero con 8.8.8.8 no (ver punto d).
- **Identification y Flags (IP):** los asigna de forma independiente cada host al crear su datagrama. Linux marca sus Request con *Don't fragment* y el router no lo hace en su respuesta.
- **Type ICMP:** pasa de 8 (Echo Request) a 0 (Echo Reply) porque el mensaje ahora es una respuesta.
- **Checksums (IP e ICMP):** se recalculan porque cambió el contenido que protegen. En ICMP la diferencia es exactamente 0x0800 (0xc1ef → 0xc9ef), porque lo único que cambió en el mensaje es el Type, de 8 a 0.

El **Identifier** y el **Sequence number** se mantienen porque el destino debe copiarlos tal cual en la respuesta: así `ping` puede emparejar cada Reply con el Request que lo originó, calcular el RTT de cada uno y detectar paquetes perdidos o desordenados. El Identifier distingue qué proceso `ping` envió el mensaje y el Sequence number distingue cada envío dentro de ese proceso.

<!-- Respuesta c) -->

#### c) Payload de ping

El payload está al final del mensaje ICMP, en el campo **Data**. Tiene **56 bytes**, que es el tamaño por defecto del `ping` de Linux. Su contenido es:

- Los primeros **16 bytes** son una marca de tiempo (*timestamp*, segundos y microsegundos) del momento en que se envió el Request. `ping` la usa para calcular el RTT cuando vuelve la respuesta. En el paquete 212 son `6a d3 e4 6a 00 00 00 00 c4 a3 02 00 00 00 00 00`.
- Los **40 bytes** restantes son un patrón de relleno con valores consecutivos (`0x10, 0x11, 0x12, … 0x37`), que en el panel hexadecimal se ve desde el offset 0x003a (14 + 20 + 8 + 16 = 58 bytes) hasta el final de la trama: en la fila `0030`, el `10` es el byte número 11.

En el Echo Reply (paquete 213) el payload es **idéntico**, byte por byte, ya que el destino lo devuelve sin modificarlo. Se puede comprobar comparando el panel hexadecimal de las capturas de los filtros `icmp.type == 8` e `icmp.type == 0`.

En Windows, en cambio, el payload por defecto es de **32 bytes** con el texto `abcdefghijklmnopqrstuvwabcdefghi`. Que sean distintos sugiere que el contenido no lo define el protocolo ICMP sino **la implementación de `ping` de cada sistema operativo**. Por eso, observando el payload (junto con el TTL inicial), se puede inferir qué SO generó el tráfico.

<!-- Respuesta d) -->

#### d) TTL

El Echo Request que enviamos tiene **TTL = 64**, el valor inicial que usa Linux. El Echo Reply que llegó de 8.8.8.8 tiene **TTL = 118**, como se ve en la salida de `ping` (`ttl=118`). En cambio, el Reply del gateway llegó con `ttl=64`.

No son iguales por dos motivos:

1. Cada sistema operativo o equipo elige su propio TTL inicial (valores típicos: 64, 128 o 255).
2. **Cada router que reenvía el paquete decrementa el TTL en 1.** Si llega a 0, el router lo descarta y envía al origen un ICMP *Time Exceeded*. Esto evita que un paquete circule indefinidamente si hay un bucle de enrutamiento.

El TTL que recibimos es entonces el valor inicial del servidor menos la cantidad de routers atravesados. Como 118 es mayor que 64, el servidor de Google debe haber usado un valor inicial de 128: la respuesta atravesó aproximadamente **128 − 118 = 10 routers** hasta llegar a nuestra red. El Reply del gateway, en cambio, llega con TTL 64 sin decrementar, porque el router es el que lo genera y está a un solo salto de nuestra computadora.

<!-- Respuesta e) -->

#### e) Encapsulación del Echo Request

```text
┌──────────────── Trama Ethernet II: 98 bytes ────────────────┐
│ Encabezado Ethernet (14 B)                                  │
│ ┌──────────── Datagrama IPv4: 84 bytes ───────────────────┐ │
│ │ Encabezado IP (20 B)                                    │ │
│ │ ┌──────────── Mensaje ICMP: 64 bytes ─────────────────┐ │ │
│ │ │ Encabezado ICMP (8 B)                               │ │ │
│ │ │ ┌───────── Datos: 56 bytes ───────────────────────┐ │ │ │
│ │ │ │ timestamp (16 B) + patrón de relleno (40 B)     │ │ │ │
│ │ │ └─────────────────────────────────────────────────┘ │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

|Caja|Encabezado|Contenido|Total|
|----|----------|---------|-----|
|Trama Ethernet II|14 bytes|84 bytes (datagrama IP)|98 bytes|
|Datagrama IPv4|20 bytes|64 bytes (mensaje ICMP)|84 bytes|
|Mensaje ICMP|8 bytes|56 bytes (datos)|64 bytes|
|Datos (payload)|—|56 bytes|56 bytes|

Los 98 bytes son los que informa Wireshark (`98 bytes on wire`) y no incluyen el preámbulo (8 bytes) ni el FCS (4 bytes) de la trama, porque la placa de red los procesa y los descarta antes de entregarle la trama al sistema operativo, así que Wireshark no los captura.

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

<!-- Respuesta a) -->

Las direcciones IP sirven para identificar a un host de extremo a extremo, pero dentro de una red local las tramas Ethernet (o Wi-Fi) se entregan usando direcciones **MAC**. Cuando un host quiere enviar un datagrama IP a otro equipo de su misma red, conoce su IP pero necesita su MAC para armar la trama. **ARP** (Address Resolution Protocol, RFC 826) resuelve ese problema: traduce una dirección IPv4 a la dirección MAC correspondiente dentro del mismo enlace.

Su ubicación en el modelo de capas es discutible porque tiene características de las dos capas entre las que trabaja:

- **Parece de capa 2 (enlace):** sus mensajes viajan directamente dentro de una trama Ethernet (EtherType `0x0806`), sin encabezado IP, y nunca salen de la red local: los routers no los reenvían.
- **Parece de capa 3 (red):** maneja direcciones IP y existe solo para darle servicio a IP.

Por eso muchas veces se lo ubica "entre" ambas capas, como un protocolo de capa 2,5 [1].

<!-- Respuesta b) -->

- **ARP Request (Opcode 1):** es la pregunta *"¿Quién tiene la IP X? Respondele a la IP Y"*. Como el emisor todavía no sabe la MAC del destino, la envía en **broadcast** (MAC destino `ff:ff:ff:ff:ff:ff`), de modo que la reciben todos los equipos de la red local. Incluye la MAC e IP del emisor y la IP buscada; el campo de MAC buscada va en ceros.
- **ARP Reply (Opcode 2):** es la respuesta *"La IP X está en la MAC Z"*. La envía únicamente el equipo que tiene la IP buscada, y la manda en **unicast** directamente al que preguntó, ya que conoce su MAC gracias al Request [1] [3].

<!-- Respuesta c) -->

La **caché ARP** es una tabla temporal que mantiene el sistema operativo con las asociaciones IP → MAC ya resueltas. Existe para no tener que hacer un Request antes de cada paquete: si cada envío requiriera un broadcast, se agregaría demora a la comunicación y se cargaría a todos los equipos de la red, que deben procesar cada broadcast [2].

Las entradas no son permanentes: vencen después de un tiempo o se vuelven a confirmar, porque una IP puede pasar a otro equipo (por ejemplo, al reasignarse por DHCP). En Linux, `ip neigh show` muestra el estado de cada entrada; los más comunes son `REACHABLE` (confirmada recientemente), `STALE` (vieja, se reconfirma la próxima vez que se use), `INCOMPLETE` (se envió un Request y se espera la respuesta) y `FAILED` (nadie respondió).

<!-- Respuesta d) -->

Cuando un host quiere enviar un paquete IP, el proceso es el siguiente:

1. Usando su máscara, decide si el destino está en su misma red. Si está, la MAC que necesita es la del destino; si no, es la del **gateway**, que va a reenviar el paquete. Por eso en el punto anterior la trama dirigida a 8.8.8.8 llevaba como MAC destino la del router.
2. Busca esa IP en su caché ARP. Si la encuentra, arma la trama con esa MAC y la envía.
3. Si no la encuentra, deja el paquete en espera y envía un ARP Request en broadcast preguntando por esa IP.
4. Todos los equipos de la red reciben el Request, pero solo el que tiene esa IP responde, con un ARP Reply unicast que contiene su MAC.
5. El host guarda la asociación en su caché y recién ahí envía el paquete que tenía en espera. El que respondió también aprovecha el Request para guardar la MAC del que preguntó [1].

<!-- Respuesta e) -->

Las pruebas de esta sección se hicieron en una computadora con Linux conectada por Wi-Fi a la misma red que la del punto anterior:

|Parámetro|Valor|
|---------|-----|
|Interfaz|`wlx7cc2c627ffa4` (Wi-Fi USB TP-Link)|
|Dirección IPv4|192.168.1.95/24|
|Dirección MAC|7c:c2:c6:27:ff:a4|
|Gateway por defecto|192.168.1.1|

Con `ip neigh show` se inspeccionó la caché ARP:

![Caché ARP con ip neigh show](./assets/p2_cache_arp.png)

La entrada `192.168.1.1 ... lladdr f0:c4:78:ba:88:40 REACHABLE` indica que el gateway tiene la MAC **`f0:c4:78:ba:88:40`** y que la asociación fue confirmada recientemente. Es la misma MAC que apareció como destino de las tramas hacia 8.8.8.8 en el punto anterior, lo que confirma que es la del router. La segunda línea (`fe80::1`) es la entrada IPv6 del mismo router; IPv6 no usa ARP sino NDP (Neighbor Discovery), por lo que no se analiza aquí.

### Generación y captura de tráfico ARP

<!-- 
- Procedimiento para generar tráfico ARP nuevo (Opción A: IP inexistente en LAN, Opción B: borrado de caché del gateway, Opción C: ping a otro host LAN).
- Captura de tráfico con filtros: arp, arp.opcode, arp.dst.proto_ipv4, arp || icmp, eth.dst == ff:ff:ff:ff:ff:ff.
-->

Todas las pruebas se hicieron en una única captura de Wireshark sobre la interfaz Wi-Fi `wlx7cc2c627ffa4`. No se usó la interfaz de loopback porque ARP solo se usa cuando hay que entregar tramas en un enlace físico: el tráfico hacia 127.0.0.1 nunca necesita una dirección MAC. Para generar tráfico ARP nuevo se usaron las opciones A y B de la consigna.

#### Opción B: borrado de la entrada del gateway

Con Wireshark capturando, se borró de la caché la entrada del gateway y se le hizo ping, todo en una sola línea:

```bash
sudo ip neigh del 192.168.1.1 dev wlx7cc2c627ffa4; ip neigh show; ping -4 -c 4 192.168.1.1; ip neigh show
```

Los comandos se encadenaron con `;` porque, en un primer intento hecho de a uno, la computadora volvió a resolver la MAC del gateway por su propio tráfico (navegación, actualizaciones) en los segundos que pasaron entre el borrado y el `ip neigh show`. Ejecutados juntos, se ve el ciclo completo:

![Borrado de la entrada del gateway y nueva resolución](./assets/p2_borrado_cache.png)

1. Después del borrado, el gateway aparece como `INCOMPLETE`: la entrada existe pero sin MAC, porque ya se envió un ARP Request y se está esperando la respuesta.
2. El ping funciona normalmente (4 de 4 respuestas).
3. Al final, el gateway vuelve a figurar como `REACHABLE`, con la misma MAC `f0:c4:78:ba:88:40`.

Con el filtro `arp` se observan los mensajes ARP de toda la captura. En Wireshark, `TPLink_27:ff:a4` corresponde a nuestra computadora y `HuaweiTechno_ba:88:40` al router: Wireshark reemplaza los primeros 3 bytes de la MAC por el nombre del fabricante.

![Filtro arp](./assets/p2_filtro_arp.png)

|Paquetes|Quién pregunta|MAC destino del Request|Descripción|
|--------|--------------|-----------------------|-----------|
|513 / 514|Nuestra computadora, por 192.168.1.1|Broadcast|Resolución del primer intento, disparada por el tráfico propio|
|2704 / 2705|El router, por 192.168.1.95|Nuestra MAC (unicast)|El router reconfirma su propia entrada ARP|
|7322 / 7323|El router, por 192.168.1.95|Nuestra MAC (unicast)|Ídem|
|7763 / 7764|Nuestra computadora, por 192.168.1.1|Broadcast|Resolución correspondiente a la terminal anterior|

El par **7763 / 7764** es el que se analiza en detalle en la sección siguiente. Para aislar cada uno se usaron los filtros `arp.opcode == 1` (solo Requests) y `arp.opcode == 2` (solo Replies).

#### Opción A: ping a una IP inexistente

Se hizo ping a 192.168.1.253, una dirección de la subred que no está asignada a ningún equipo, y luego se inspeccionó la caché:

```bash
ping -4 -c 4 192.168.1.253
ip neigh show
```

![Ping a una IP inexistente y caché ARP](./assets/p2_ping_inexistente.png)

Los cuatro pings fallan con `Destination Host Unreachable`, informado por **nuestra propia computadora** (`From 192.168.1.95`) y no por el router. La caché registra la dirección como `192.168.1.253 ... FAILED`, sin MAC.

Con el filtro `arp.dst.proto_ipv4 == 192.168.1.253`, que selecciona los mensajes ARP cuyo *Target IP address* es esa dirección, quedan solamente los Requests hacia la IP inexistente:

![Filtro arp.dst.proto_ipv4 == 192.168.1.253](./assets/p2_filtro_inexistente.png)

Con el filtro `arp || icmp` se ven juntos el tráfico ARP y los pings, para comprobar si algún Echo Request llegó a salir hacia esa dirección:

![Filtro arp || icmp](./assets/p2_filtro_arp_icmp.png)

#### Tráfico broadcast

Por último, con el filtro `eth.dst == ff:ff:ff:ff:ff:ff` se muestran todas las tramas Ethernet enviadas a broadcast, de cualquier protocolo:

![Filtro eth.dst == ff:ff:ff:ff:ff:ff](./assets/p2_filtro_broadcast.png)

Las 8 tramas que aparecen son ARP Requests enviados por nuestra computadora: 2 hacia el gateway (513 y 7763) y 6 hacia 192.168.1.253. Ninguno de los Requests del router aparece en este filtro, porque todos fueron enviados en unicast.

### Análisis de tramas ARP Request y Reply

<!-- 
- Tabla comparativa de campos de ARP Request y Reply (MAC destino/origen Ethernet, Opcode, Sender MAC/IP, Target MAC/IP).
- Preguntas de análisis:
  a) Por qué Request es broadcast y Reply unicast; valor de Target MAC en Request.
  b) Campo EtherType en Ethernet (0x0806) y ausencia de encabezado IP (dónde vive ARP).
  c) Observación con IP inexistente (reintentos de ARP, presencia/ausencia de ICMP).
  d) Reintento de ping tras 1 minuto (comportamiento de caché, ventajas y riesgos de entradas desactualizadas).
-->

Se analizaron el ARP Request 7763 y su ARP Reply 7764, correspondientes a la Opción B. Para cada uno se desplegaron en Wireshark los encabezados Ethernet II y ARP:

![Detalle del ARP Request 7763](./assets/p2_request_detalle.png)

![Detalle del ARP Reply 7764](./assets/p2_reply_detalle.png)

|Campo|ARP Request (7763)|ARP Reply (7764)|
|-----|------------------|----------------|
|MAC destino (Ethernet)|ff:ff:ff:ff:ff:ff (Broadcast)|7c:c2:c6:27:ff:a4|
|MAC origen (Ethernet)|7c:c2:c6:27:ff:a4|f0:c4:78:ba:88:40|
|Opcode|1 (request)|2 (reply)|
|Sender MAC|7c:c2:c6:27:ff:a4|f0:c4:78:ba:88:40|
|Sender IP|192.168.1.95|192.168.1.1|
|Target MAC|00:00:00:00:00:00|7c:c2:c6:27:ff:a4|
|Target IP|192.168.1.1|192.168.1.95|

En el Reply, los campos Sender y Target se invierten respecto del Request, y el Target MAC pasa de estar en ceros a contener nuestra MAC.

<!-- Respuesta a) -->

#### a) Request broadcast y Reply unicast

El Request se envía en broadcast porque lo que se busca es justamente la MAC del destino: sin conocerla, no hay otra forma de hacerle llegar la pregunta que enviarla a todos los equipos de la red. Por eso el **Target MAC del Request vale `00:00:00:00:00:00`**: es la incógnita, y el campo se completa con ceros porque no tiene un valor útil.

El Reply, en cambio, se envía en unicast porque quien responde ya sabe a quién contestarle: el Request trae la MAC del que pregunta en el campo *Sender MAC*. Enviarlo a broadcast molestaría innecesariamente a los demás equipos de la red.

En la captura también se observa que el broadcast solo es necesario cuando la MAC es desconocida. Los Requests del router (paquetes 2704, 7322, 12350, 18142, 24256 y 26943) preguntan por 192.168.1.95, pero van dirigidos directamente a nuestra MAC: el router ya la tiene en su caché y solo está verificando que siga siendo válida [2]. Por eso ninguno de ellos aparece con el filtro `eth.dst == ff:ff:ff:ff:ff:ff`.

<!-- Respuesta b) -->

#### b) EtherType y ausencia de encabezado IP

En el encabezado Ethernet II de ambas tramas, el campo **Type vale `0x0806`**, que identifica a ARP. Es el mismo campo que en el punto anterior valía `0x0800` para IPv4: le indica al receptor qué protocolo viene a continuación. En el panel hexadecimal de las capturas aparece resaltado como los bytes `08 06`.

Inmediatamente después del encabezado Ethernet viene el mensaje ARP, **sin ningún encabezado IP en el medio**. Esto muestra que ARP no viaja dentro de IP, sino directamente sobre la capa de enlace. Una consecuencia de esto es que los mensajes ARP no tienen IP de origen ni de destino en un encabezado, ni TTL, y por lo tanto no pueden ser enrutados: nunca salen de la red local.

Cada trama ocupa 42 bytes: 14 del encabezado Ethernet y 28 del mensaje ARP.

|Campo ARP|Tamaño|Valor en el Request|
|---------|------|-------------------|
|Hardware type|2 bytes|1 (Ethernet)|
|Protocol type|2 bytes|0x0800 (IPv4)|
|Hardware size|1 byte|6|
|Protocol size|1 byte|4|
|Opcode|2 bytes|1 (request)|
|Sender MAC|6 bytes|7c:c2:c6:27:ff:a4|
|Sender IP|4 bytes|192.168.1.95|
|Target MAC|6 bytes|00:00:00:00:00:00|
|Target IP|4 bytes|192.168.1.1|

Los campos *Hardware type* y *Protocol type* indican qué tipo de direcciones se están traduciendo (Ethernet e IPv4), y *Hardware size* y *Protocol size* su longitud (6 bytes una MAC, 4 bytes una IPv4) [2].

<!-- Respuesta c) -->

#### c) IP inexistente

En las capturas de la Opción A se observa que:

- **Se enviaron 6 ARP Requests** preguntando por 192.168.1.253 (paquetes 12600 y 12603 a 12607), todos a broadcast y separados por aproximadamente un segundo. La computadora reintenta porque un Request o su respuesta podrían haberse perdido.
- **No hubo ningún ARP Reply**, ya que ningún equipo tiene esa dirección.
- **No salió ningún paquete ICMP** hacia 192.168.1.253. Con el filtro `arp || icmp`, los únicos Echo Request y Echo Reply de la captura son los del ping al gateway.

Esto ocurre porque, sin la MAC del destino, no es posible armar la trama Ethernet que llevaría el Echo Request. Los pings quedaron en espera mientras se intentaba la resolución (`pipe 4` en la salida de `ping`) y, al no recibir respuesta, el sistema operativo marcó la entrada como `FAILED` y descartó los paquetes. Por eso el mensaje `Destination Host Unreachable` lo informa nuestra propia computadora (`From 192.168.1.95`) y no aparece en la captura: se genera localmente y nunca viaja por la red.

<!-- Respuesta d) -->

#### d) Ping repetido después de 1 minuto

Pasado más de un minuto desde la resolución de la Opción B, se repitió el ping al gateway:

![Ping al gateway repetido](./assets/p2_ping_1min.png)

![Filtro arp después del ping repetido](./assets/p2_filtro_1min.png)

Antes del ping, el gateway ya figuraba como `REACHABLE` con su MAC, y en la captura **no aparece ningún ARP Request nuevo de nuestra computadora** después del 7763: la MAC se tomó directamente de la caché. Los únicos mensajes ARP nuevos (24256 / 24257) son otra verificación unicast iniciada por el router. La entrada seguía siendo válida aunque pasaron varios minutos desde su resolución porque la computadora usa el gateway constantemente para salir a Internet, y ese tráfico permite confirmar que la asociación sigue siendo correcta sin necesidad de volver a preguntar.

**Ventajas de la caché:**

- Se evita la demora de resolver la MAC antes de cada paquete.
- Se reduce el tráfico broadcast, que todos los equipos de la red deben recibir y procesar.

**Riesgos de las entradas desactualizadas:**

- Si una IP pasa a otro equipo (por ejemplo, al reemplazar el router o al reasignarse una dirección por DHCP), los hosts siguen enviando las tramas a la MAC vieja hasta que la entrada vence o se reconfirma, y esos paquetes se pierden.
- ARP no tiene autenticación: un host acepta un Reply sin poder verificar quién lo envió. Un atacante puede enviar Replies falsos asociando la IP del gateway a su propia MAC (*ARP spoofing*). La víctima guarda esa asociación en su caché y empieza a enviarle todo su tráfico al atacante, que puede leerlo o modificarlo (ataque de intermediario o *man-in-the-middle*).

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

- Postel, J. (1981). *RFC 792: Internet Control Message Protocol*. IETF. <https://www.rfc-editor.org/rfc/rfc792>
- Postel, J. (1981). *RFC 791: Internet Protocol*. IETF. <https://www.rfc-editor.org/rfc/rfc791>
- Wireshark Foundation. *Wireshark User's Guide: Building Display Filter Expressions*. <https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html>
- *ping(8), manual de iputils*. <https://man7.org/linux/man-pages/man8/ping.8.html>
