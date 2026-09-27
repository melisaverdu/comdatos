![](/assets/2_1_Isologotipo_FCEFyN_y_UNC-_blanco_Sin_fondo-Con_bajada.png)

# Trabajo Práctico N.º 4: Capas de Acceso en Redes Locales, Protocolos y Fundamentos

**Alumnos**
- García, Lautaro Misael 
- Pastrana Lizárraga, Iván
- Peretti, Federico Ariel
- Renaudo Gaggioli, Valentino
- Verdú, Melisa Noel

---

### Índice

1. [Alcance de Redes y Virtualización](#alcance-de-redes-y-virtualización)
2. [Implementación Básica de Conmutación y Segmentación por VLANs](#implementación-básica-de-conmutación-y-segmentación-por-vlans)
3. [Despliegue y Arquitectura de Red LAN a Bordo de una Aeronave](#despliegue-y-arquitectura-de-red-lan-a-bordo-de-una-aeronave)
4. [Conclusión](#conclusión)
5. [Referencias](#referencias)

---

## Alcance de Redes y Virtualización

### Clasificación de Redes según su Alcance

Las redes de datos se clasifican fundamentalmente a partir de su **alcance geográfico y escala de cobertura**, lo cual condiciona los medios físicos de transmisión, las velocidades, la latencia y si la administración es privada o provista por un operador de telecomunicaciones (*Carrier*):

| Acrónimo | Denominación | Alcance Típico | Entorno y Aplicación Principal | Tecnologías Frecuentes | Gestión |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BAN** | *Body Area Network* | $\approx 1\text{ m}$ | Red corporal para sensores médicos y *wearables* | BLE, IEEE 802.15.6, NFC | Privada / Personal |
| **PAN** | *Personal Area Network* | $\le 10\text{ m}$ | Espacio de trabajo personal y periféricos | Bluetooth (802.15.1), Zigbee, USB | Privada / Personal |
| **LAN** | *Local Area Network* | $10\text{ m} - 1\text{ km}$ | Hogares, oficinas o plantas fabriles | Ethernet (802.3), Wi-Fi (802.11) | Privada |
| **CAN** | *Campus Area Network* | $1 - 5\text{ km}$ | Campus universitarios o complejos industriales | Dorsales de Fibra Óptica (10G/40G) | Privada |
| **MAN** | *Metropolitan Area Network* | $5 - 50\text{ km}$ | Ámbito metropolitano o urbano (municipios) | Metro Ethernet, DWDM, fibra óptica | Proveedor / Consorcio |
| **WAN** | *Wide Area Network* | $> 50\text{ km}$ (Global) | Interconexión regional, interurbana y global (Internet) | Fibra submarina, satélites, MPLS, BGP | Proveedores / *Carriers* |

#### Resolución de la Figura (Asignación de Acrónimos por Cuadro)

En correspondencia con los alcances métricos de la tabla, se asigna el acrónimo correspondiente en cada cuadro de la figura jerárquica:

* **Cuadro 1 ($\le 10\text{ m}$):** **PAN** (*Personal Area Network*) [y **BAN** en escala corporal $< 2\text{ m}$].
* **Cuadro 2 ($10\text{ m} - 1\text{ km}$):** **LAN** (*Local Area Network*).
* **Cuadro 3 ($1\text{ km} - 5\text{ km}$):** **CAN** (*Campus Area Network*).
* **Cuadro 4 ($5\text{ km} - 50\text{ km}$):** **MAN** (*Metropolitan Area Network*).
* **Cuadro 5 ($> 50\text{ km}$ / Global):** **WAN** (*Wide Area Network*).

```
+-----------------------------------------------------------------------------------------------+
|  CUADRO 5: WAN (Wide Area Network)                                                            |
|  Alcance: > 50 km (Regional, Nacional, Global / Internet)                                     |
|                                                                                               |
|      +---------------------------------------------------------------------------------+      |
|      |  CUADRO 4: MAN (Metropolitan Area Network)                                      |      |
|      |  Alcance: 5 km a 50 km (Ámbito Urbano / Metropolitano)                          |      |
|      |                                                                                 |      |
|      |      +-------------------------------------------------------------------+      |      |
|      |      |  CUADRO 3: CAN (Campus Area Network)                              |      |      |
|      |      |  Alcance: 1 km a 5 km (Campus Universitario / Complejo Industrial)|      |      |
|      |      |                                                                   |      |      |
|      |      |      +-----------------------------------------------------+      |      |      |
|      |      |      |  CUADRO 2: LAN (Local Area Network)                 |      |      |      |
|      |      |      |  Alcance: 10 m a 1 km (Edificio / Oficina / Residencia)|   |      |      |
|      |      |      |                                                     |      |      |      |
|      |      |      |      +---------------------------------------+      |      |      |      |
|      |      |      |      |  CUADRO 1: PAN (Personal Area Network)|      |      |      |      |
|      |      |      |      |  Alcance: <= 10 m (Espacio Personal)  |      |      |      |      |
|      |      |      |      |                                       |      |      |      |      |
|      |      |      |      |    +-----------------------------+    |      |      |      |      |
|      |      |      |      |    |  BAN (Body Area Network)    |    |      |      |      |      |
|      |      |      |      |    |  Alcance: < 2 m (Corporal)  |    |      |      |      |      |
|      |      |      |      |    +-----------------------------+    |      |      |      |      |
|      |      |      |      +---------------------------------------+      |      |      |      |
|      |      |      +-----------------------------------------------------+      |      |      |
|      |      +-------------------------------------------------------------------+      |      |
|      +---------------------------------------------------------------------------------+      |
+-----------------------------------------------------------------------------------------------+
```

---

### Fundamentos y Clasificación de Redes LAN Virtuales (VLANs)

Una **VLAN** (*Virtual Local Area Network*) es una subred lógica independiente configurada sobre una infraestructura de conmutación física común (switches de Capa 2), **con independencia de la ubicación física o del puerto al que se conecten los equipos**.

* **Propósitos Principales:**
  1. **Segmentación de Broadcast:** Limita el tráfico de difusión a los miembros de la misma VLAN, reduciendo la saturación de la red.
  2. **Seguridad y Aislamiento:** Impide el tráfico directo entre distintas VLANs en Capa 2, requiriendo un router o switch Capa 3 para comunicarse (donde se aplican ACLs y firewalls).
  3. **Flexibilidad:** Permite reagrupar usuarios lógicamente sin alterar el cableado físico.

* **Clasificación según Método de Asignación (*Membership*):**
  * **Basadas en puerto (Estáticas):** Cada puerto físico del switch se asocia a un *VLAN ID*. Es el método estándar y más difundido.
  * **Dinámicas (MAC, Protocolo o 802.1X):** La VLAN se asigna por dirección MAC, protocolo L3 o mediante autenticación centralizada RADIUS.

* **Clasificación según Rol Funcional del Tráfico:**
  * **VLAN de Datos:** Tráfico ordinario de usuarios (web, archivos, correo).
  * **VLAN por Defecto:** VLAN a la que pertenecen todos los puertos al salir de fábrica (típicamente VLAN 1).
  * **VLAN Nativa:** En enlaces troncales 802.1Q, es la VLAN asignada al tráfico que viaja **sin etiqueta (*untagged*)** para mantener compatibilidad con protocolos de control (STP, CDP).
  * **VLAN de Administración:** Dedicada a la gestión remota del conmutador (SSH, HTTPS, SNMP) mediante una interfaz virtual (*SVI*, e.g., `interface vlan 99`).
  * **VLAN de Voz:** Reservada para telefonía IP (VoIP), garantizando prioridad de Calidad de Servicio (QoS).

---

### Estándar IEEE 802.1Q y Mecanismo de Tagging

Para transportar múltiples VLANs a través de un único enlace físico entre conmutadores (**enlace troncal o *trunk link***), el estándar abierto **IEEE 802.1Q** define un mecanismo universal de **etiquetado de tramas (*frame tagging*)**:

* **Tagging:** El conmutador emisor inserta una etiqueta de 4 bytes (32 bits) dentro de la cabecera Ethernet al salir por un puerto troncal para identificar la VLAN de origen.
* **Untagging:** El conmutador receptor remueve la etiqueta antes de entregar la trama al host final por un puerto de acceso, garantizando que el receptor reciba una trama Ethernet II normal.

```
Trama Ethernet II Original (Untagged):
+-------------------+-------------------+--------------------+------------------------+----------+
|  MAC Destino (6B) |   MAC Origen (6B) | EtherType/Len (2B) |     Datos / Carga Útil | FCS (4B) |
+-------------------+-------------------+--------------------+------------------------+----------+

Trama Etiquetada IEEE 802.1Q (Tagged):
+-------------------+-------------------+----------------+--------------------+------------------------+----------+
|  MAC Destino (6B) |   MAC Origen (6B) | Tag 802.1Q(4B) | EtherType/Len (2B) |     Datos / Carga Útil | FCS (4B) |
+-------------------+-------------------+----------------+--------------------+------------------------+----------+
                                                |
            +-----------------------------------+-----------------------------------+
            |   TPID (16 bits)   |  PCP (3 bits)  | DEI (1 bit)     |  VID (12 bits)    |
            |       0x8100       | Prioridad QoS  | Descarte eleg.  |  VLAN ID (0-4095) |
            +--------------------+----------------+-----------------+-------------------+
```

* **Estructura del Tag 802.1Q (4 bytes / 32 bits):**
  1. **TPID (16 bits):** Valor fijo `0x8100` que identifica la presencia de una etiqueta 802.1Q.
  2. **TCI (16 bits):**
     - **PCP (3 bits):** Prioridad de Calidad de Servicio (QoS) bajo IEEE 802.1p (8 niveles, 0 a 7).
     - **DEI (1 bit):** Indicador de trama elegible para descarte en situaciones de congestión.
     - **VID (12 bits):** Identificador numérico de VLAN ($2^{12} = 4096$ identificadores posibles, rangos operativos 1 a 4094).

* **Consideraciones Operativas:**
  - **Tamaño de trama:** La etiqueta incrementa la longitud máxima de 1518 a **1522 bytes** (*Baby Giant Frames*), forzando al switch a **recalcular el FCS (CRC-32)**.
  - **Tráfico sin etiqueta (*Untagged*):** El tráfico de la VLAN nativa transita sin etiqueta por el troncal. Si un switch recibe una trama sin etiqueta en un troncal, la asigna a su VLAN nativa.

---

## Implementación Básica de Conmutación y Segmentación por VLANs

Topología de Red y Tabla de Direccionamiento a implementar:

![Topología](./assets/topologia.png)
![Tabla de direccionamiento](./assets/tabla_ruteo.png)

---

Topología implementada:

![Topología](./assets/topologia_implementada.png)

### Configuración de Seguridad Básica y Direccionamiento en Switches

Se realizó la configuración inicial y el endurecimiento (*hardening*) de la seguridad en los switches `SW-1` y `SW-2` aplicando las convenciones de administración estándar de Cisco IOS.

#### 1. Protección de Accesos y Cifrado de Credenciales
Se configuraron las credenciales de administración para restringir el acceso local y remoto en ambos dispositivos:
- **Modo EXEC Privilegiado:** Se asignó la contraseña protegida `class` mediante el comando `enable secret`.
- **Líneas de Consola y VTY (`0 15`):** Se aseguró el acceso físico por puerto serial y el acceso remoto por red mediante la clave `cisco` y la directiva `login`.

![Configuración de contraseñas de consola y VTY en SW-1](./assets/puntos_a_b.png)

Para evitar la exposición de credenciales en texto plano al inspeccionar el archivo de configuración activa (`running-config`), se habilitó la función global `service password-encryption`. Este mecanismo aplica un algoritmo de cifrado reversible sobre todas las contraseñas almacenadas no encriptadas.

![Visualización de contraseñas en texto plano en show running-config](./assets/punto_c_sinEncriptar.png)
![Visualización de contraseñas cifradas tras aplicar service password-encryption](./assets/punto_c_encriptado.png)

#### 2. Configuración de redes VLAN

Se habilitó la Interfaz Virtual de Switch (SVI) sobre la VLAN 1 por defecto para permitir la administración remota Nivel 3 de los switches según la tabla de direccionamiento provista.

![Configuración IP de la SVI VLAN 1 en SW-1](./assets/punto_d_sw1.png)
![Configuración IP de la SVI VLAN 1 en SW-2](./assets/punto_d_sw2.png)


#### 3. Desactivación Preventiva de Puertos Inactivos

Como principio fundamental de seguridad en la Capa de Enlace, se apagaron administrativamente todas las interfaces físicas que no intervienen en la topología mediante la orden shutdown. Esta medida previene conexiones no autorizadas o ataques de acceso físico a la red.

![SW-1](./assets/punto_e_sw1.png)
![SW-1](./assets/punto_e_sw1(1).png)

Para el caso de SW-2:
```
sw2(config)# interface range FastEthernet 0/2 - 17, FastEthernet 0/19 - 24, GigabitEthernet 0/1 - 2
sw2(config-if-range)# shutdown
sw2(config-if-range)# exit
```

![SW-2](./assets/punto_e_sw2.png)

Posteriormente, se respaldaron las configuraciones en la memoria NVRAM de ambos conmutadores ejecutando la orden: `sw1# copy running-config startup-config`

se realizó una prueba de conectividad ICMP (`ping`) desde la PC-A (`192.168.10.3`) hacia la PC-B (`192.168.10.4`).
- Resultado: Exitoso (0% de pérdida de paquetes).

![Prueba de ping entre PC-A y PC-B](./assets/punto_g_pca.png)

- Justificación Técnica: Al inicio del laboratorio, los puertos `F0/6` (SW-1), `F0/18` (SW-2) y la interfaz inter-switch `F0/1` formaban parte de la VLAN 1 por defecto. Al pertenecer a un único dominio de broadcast a Nivel 2 y compartir la subred IP `192.168.10.0/24`, las tramas Ethernet se conmutaron entre switches sin impedimentos.

#### Creación e identificación de VLANs

Con el objeto de aislar los dominios de broadcast y segmentar el tráfico, se definieron tres VLANs independientes y se reasignaron las interfaces físicas y virtuales.

Se crearon e identificaron las siguientes VLANs en ambos switches:
- VLAN 10 (Laboratorio)
- VLAN 20 (Bar)
- VLAN 99 (Management)

![Creación e identificación de VLANs en SW-1](./assets/punto_h_i_sw1.png)

#### Asignación de Puertos de Acceso

Se asociaron los puertos donde se encuentran conectadas las computadoras a la VLAN 10 en modo acceso (`access`), garantizando que las tramas ingresadas por dichos puertos pertenezcan únicamente a ese dominio de broadcast:

![Configuración en SW-1](./assets/punto_j_sw1.png)

Para el caso de SW-2:
```
sw2(config)# interface FastEthernet 0/18
sw2(config-if)# switchport mode access
sw2(config-if)# switchport access vlan 10
```

#### Migración de la SVI a la VLAN 99

Para evitar el uso de la VLAN 1 nativa en la gestión de red, se removió la dirección IP asignada a la `interface vlan 1` y se reconfiguró la SVI dentro de la VLAN 99:

![Verificación de creación de VLANs y puertos asignados mediante show vlan brief](./assets/punto_k_l_sw1.png)
![Verificación del estado operativo de las interfaces virtuales SVI mediante show ip interface brief](./assets/punto_l.png)

1. **Análisis de la Tabla de VLANs (`show vlan brief`):**
   - **Segmentación Lógica:** Se confirma la presencia de las VLANs `10` (*Laboratorio*), `20` (*Bar*) y `99` (*Management*) en estado activo dentro de la base de datos de conmutación.
   - **Asignación de Puertos de Acceso:** La interfaz física `F0/6` en `SW-1` (y `F0/18` en `SW-2`) figura asignada correctamente a la **VLAN 10**, habiendo sido desvinculada de la VLAN 1 nativa.
   * **Ausencia de Puertos en VLAN 99:** La **VLAN 99** se encuentra dada de alta pero no registra ningún puerto físico de acceso mapeado directamente a ella.

2. **Análisis del Estado de Interfaces (`show ip interface brief`):**
   - **SVI VLAN 1:** Muestra su estado en `unassigned` y `administratively down`, confirmando que se removió con éxito la IP de gestión de la VLAN por defecto para reducir vulnerabilidades.
   - **SVI VLAN 99:** La interfaz virtual registra asignada la dirección IP de administración de Nivel 3 (`192.168.1.11` en `SW-1` / `192.168.1.12` en `SW-2`) con estado administrativo encendido (`Status: up`). Sin embargo, su protocolo de línea figura como **`down`** (`Protocol: down`). Una Interfaz Virtual de Switch (**SVI**) requiere cumplir la condición de **asociación física activa** para pasar al estado operacional `up/up`. Esto significa que el switch debe detectar al menos un puerto físico en estado activo (*up/up*) que pertenezca a la VLAN 99. Al no existir puertos de acceso asignados a la VLAN 99, la SVI 99 carece de una Capa de Enlace subyacente activa, por lo que su protocolo de comunicación permanece en estado **`down`** e impide procesar paquetes IP.

### Análisis de Conectividad y Verificación de la Capa de Enlace
Tras reasignar los puertos de los hosts a la VLAN 10 y migrar las IP de gestión a la VLAN 99, se repitieron las pruebas de transmisión ICMP:

1. Prueba entre PC-A $\rightarrow$ PC-B:
   - Comando en PC-A: ping 192.168.10.4
   - Resultado: Fallido (Request timed out - 100% de pérdida).
    ![Prueba de ping entre PC-A y PC-B](./assets/punto_n.png)

2. Prueba entre SW-1 $\rightarrow$ SW-2:
   - Comando en SW-1: ping 192.168.1.12
   - Resultado: Fallido (Success rate is 0 percent).
    ![Prueba de ping entre SW-1 y SW-2](./assets/punto_n2.png)

#### Diagnóstico de la Falla de Conectividad entre PC-A y PC-B (VLAN 10)

Al reasignar los puertos de **PC-A** y **PC-B** a la **VLAN 10** (*Laboratorio*), ambas computadoras quedaron aisladas en un nuevo dominio de broadcast virtual, separándose de la red por defecto (**VLAN 1**). 

Para que dos computadoras ubicadas en switches distintos puedan comunicarse dentro de una misma VLAN, el cable físico de interconexión (`FastEthernet 0/1`) debe estar habilitado para transportar el tráfico de ese grupo específico.

Sin embargo, la interfaz `F0/1` permanece configurada en **modo acceso dentro de la VLAN 1**. Esto provoca que el puerto funcione como una barrera para cualquier otra VLAN:

- **Bloqueo en el switch de origen:** Cuando la **PC-A** genera un paquete hacia la **PC-B**, el switch `SW-1` recibe los datos pertenecientes a la **VLAN 10**.
- **Incompatibilidad en el puerto de salida:** Al intentar reenviar la información hacia `SW-2` por la interfaz `F0/1`, `SW-1` detecta que dicho puerto solo permite el paso de tráfico de la **VLAN 1**.
- **Descarte de tráfico:** Al no coincidir las VLANs, `SW-1` descarta el paquete inmediatamente antes de que pueda salir por el cable físico.

En consecuencia, el tráfico de la **VLAN 10** nunca llega a cruzar hacia `SW-2`, dejando a las computadoras completamente incomunicadas.

#### Diagnóstico de la Falla de Conectividad entre Switches (VLAN 99)

Las direcciones IP de administración (`192.168.1.11` y `192.168.1.12`) se configuraron en las interfaces virtuales de la **VLAN 99** en ambos switches. Sin embargo, la prueba de `ping` entre `SW-1` y `SW-2` falla por lo siguiente:

- **Sin puertos físicos asignados:** Ninguno de los dos switches tiene un puerto físico donde haya dispositivos conectados asignado a la **VLAN 99**.
- **El cable de enlace no la transporta:** El puerto inter-switch (`F0/1`) sigue operando en modo acceso para la **VLAN 1**, por lo que no puede enviar tráfico de la **VLAN 99** hacia el otro switch.
- **La interfaz virtual permanece caída:** Para que la interfaz virtual de un switch (`interface vlan 99`) se active operativamente, necesita tener al menos un puerto físico activo asociado a esa misma VLAN. Al no haber ningún puerto funcionando en la VLAN 99, la interfaz lógica se mantiene en estado **caído (`line protocol is down`)**.

Al estar la interfaz de gestión inactiva por falta de conexión física, el conmutador no puede procesar paquetes IP en esa red, haciendo imposible la comunicación de administración entre `SW-1` y `SW-2`.

---

## Despliegue y Arquitectura de Red LAN a Bordo de una Aeronave

### Diseño Arquitectónico, VLANs y Servidor de Entretenimiento Local

### Ruteo Inter-VLAN (Router-on-a-Stick), Servicio DHCP y Traducción NAT

### Políticas de Control de Acceso mediante Listas de Control de Acceso (ACL)

### Matriz de Pruebas, Validación de Tráfico y Resultados

---

## Conclusión

---

## Referencias