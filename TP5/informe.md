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

<!-- Respuesta a) -->

Las direcciones IP sirven para identificar a un host de extremo a extremo, pero dentro de una red local las tramas Ethernet (o Wi-Fi) se entregan usando direcciones **MAC**. Cuando un host quiere enviar un datagrama IP a otro equipo de su misma red, conoce su IP pero necesita su MAC para armar la trama. **ARP** (Address Resolution Protocol, RFC 826) resuelve ese problema: traduce una dirección IPv4 a la dirección MAC correspondiente dentro del mismo enlace.

Su ubicación en el modelo de capas es discutible porque tiene características de las dos capas entre las que trabaja:

- **Parece de capa 2 (enlace):** sus mensajes viajan directamente dentro de una trama Ethernet (EtherType `0x0806`), sin encabezado IP, y nunca salen de la red local: los routers no los reenvían.
- **Parece de capa 3 (red):** maneja direcciones IP y existe solo para darle servicio a IP.

Por eso muchas veces se lo ubica "entre" ambas capas, como un protocolo de capa 2,5.

<!-- Respuesta b) -->

- **ARP Request (Opcode 1):** es la pregunta *"¿Quién tiene la IP X? Respondele a la IP Y"*. Como el emisor todavía no sabe la MAC del destino, la envía en **broadcast** (MAC destino `ff:ff:ff:ff:ff:ff`), de modo que la reciben todos los equipos de la red local. Incluye la MAC e IP del emisor y la IP buscada; el campo de MAC buscada va en ceros.
- **ARP Reply (Opcode 2):** es la respuesta *"La IP X está en la MAC Z"*. La envía únicamente el equipo que tiene la IP buscada, y la manda en **unicast** directamente al que preguntó, ya que conoce su MAC gracias al Request.

<!-- Respuesta c) -->

La **caché ARP** es una tabla temporal que mantiene el sistema operativo con las asociaciones IP → MAC ya resueltas. Existe para no tener que hacer un Request antes de cada paquete: si cada envío requiriera un broadcast, se agregaría demora a la comunicación y se cargaría a todos los equipos de la red, que deben procesar cada broadcast.

Las entradas no son permanentes: vencen después de un tiempo o se vuelven a confirmar, porque una IP puede pasar a otro equipo (por ejemplo, al reasignarse por DHCP). En Linux, `ip neigh show` muestra el estado de cada entrada; los más comunes son `REACHABLE` (confirmada recientemente), `STALE` (vieja, se reconfirma la próxima vez que se use), `INCOMPLETE` (se envió un Request y se espera la respuesta) y `FAILED` (nadie respondió).

<!-- Respuesta d) -->

Cuando un host quiere enviar un paquete IP, el proceso es el siguiente:

1. Usando su máscara, decide si el destino está en su misma red. Si está, la MAC que necesita es la del destino; si no, es la del **gateway**, que va a reenviar el paquete. Por eso en el punto anterior la trama dirigida a 8.8.8.8 llevaba como MAC destino la del router.
2. Busca esa IP en su caché ARP. Si la encuentra, arma la trama con esa MAC y la envía.
3. Si no la encuentra, deja el paquete en espera y envía un ARP Request en broadcast preguntando por esa IP.
4. Todos los equipos de la red reciben el Request, pero solo el que tiene esa IP responde, con un ARP Reply unicast que contiene su MAC.
5. El host guarda la asociación en su caché y recién ahí envía el paquete que tenía en espera. El que respondió también aprovecha el Request para guardar la MAC del que preguntó.

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

En la captura también se observa que el broadcast solo es necesario cuando la MAC es desconocida. Los Requests del router (paquetes 2704, 7322, 12350, 18142, 24256 y 26943) preguntan por 192.168.1.95, pero van dirigidos directamente a nuestra MAC: el router ya la tiene en su caché y solo está verificando que siga siendo válida. Por eso ninguno de ellos aparece con el filtro `eth.dst == ff:ff:ff:ff:ff:ff`.

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

Los campos *Hardware type* y *Protocol type* indican qué tipo de direcciones se están traduciendo (Ethernet e IPv4), y *Hardware size* y *Protocol size* su longitud (6 bytes una MAC, 4 bytes una IPv4).

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
