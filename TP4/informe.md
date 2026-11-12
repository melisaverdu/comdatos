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

Las redes de computadoras y sistemas de comunicación de datos se clasifican fundamentalmente en función de su **alcance geográfico y escala de cobertura** [4]. Esta diferenciación espacial no solo define el área física que abarca la red, sino que también determina las tecnologías de transmisión empleadas, la latencia, las velocidades de transferencia y el esquema de administración o propiedad [1], [4].

| Acrónimo | Denominación | Alcance Típico | Entorno y Aplicación Principal | Tecnologías Frecuentes | Gestión |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BAN** | *Body Area Network* | $\le 2\text{ m}$ | Red corporal para sensores médicos y *wearables* | BLE, IEEE 802.15.6, NFC | Privada / Personal |
| **PAN** | *Personal Area Network* | $\le 10\text{ m}$ | Espacio de trabajo personal y periféricos | Bluetooth (802.15.1), Zigbee, USB | Privada / Personal |
| **LAN** | *Local Area Network* | $10\text{ m} - 1\text{ km}$ | Hogares, oficinas o plantas fabriles | Ethernet (802.3), Wi-Fi (802.11) | Privada |
| **CAN** | *Campus Area Network* | $1 - 5\text{ km}$ | Campus universitarios o complejos industriales | Enlaces de fibra óptica, Gigabit Ethernet, switches de núcleo  | Privada |
| **MAN** | *Metropolitan Area Network* | $5 - 50\text{ km}$ | Ámbito metropolitano o urbano (municipios) | Metro Ethernet, DWDM, fibra óptica | Proveedor / Consorcio |
| **WAN** | *Wide Area Network* | $> 50\text{ km}$ (Global) | Interconexión regional, interurbana y global (Internet) | Fibra submarina, satélites, MPLS, BGP | Proveedores / *Carriers* |

#### Resolución de la Figura (Asignación de Acrónimos por Cuadro)

En correspondencia con los alcances métricos de la tabla, se asigna el acrónimo correspondiente en cada cuadro de la figura jerárquica:

* **Cuadro 1 ($\le 10\text{ m}$):** **PAN** (*Personal Area Network*) [y **BAN** en escala corporal $\le 2\text{ m}$].
* **Cuadro 2 ($10\text{ m} - 1\text{ km}$):** **LAN** (*Local Area Network*).
* **Cuadro 3 ($1\text{ km} - 5\text{ km}$):** **CAN** (*Campus Area Network*).
* **Cuadro 4 ($5\text{ km} - 50\text{ km}$):** **MAN** (*Metropolitan Area Network*).
* **Cuadro 5 ($> 50\text{ km}$ / Global):** **WAN** (*Wide Area Network*).

<p align="center">
  <img src="./assets/clasificacion_acrónimos.png" alt="Figura de clasificación de redes según su alcance" width="80%" />
</p>

---

### Fundamentos y Clasificación de Redes LAN Virtuales (VLANs)

Una **VLAN** (*Virtual Local Area Network*) es un dominio de difusión (*broadcast domain*) lógico independiente creado sobre una infraestructura física de conmutación de Capa 2. Permite agrupar dispositivos de red en la misma subred lógica sin importar si están conectados al mismo switch físico o a conmutadores situados en ubicaciones distantes [2], [3].

### Propósitos y Beneficios Fundamentales

1. **Aislamiento del Dominio de Difusión:** En una red conmutada tradicional, las tramas de difusión (*broadcast*) y multidifusión (*multicast*) se entregan a todos los puertos del switch. Una VLAN delimita el alcance de estas tramas únicamente a los hosts que forman parte de dicha VLAN [2], [3], reduciendo la congestión y previniendo tormentas de difusión.
2. **Seguridad y Control de Acceso:** La comunicación directa en Capa 2 entre hosts de diferentes VLANs está completamente bloqueada. Para comunicar distintas VLANs se requiere obligatoriamente un dispositivo de Capa 3 (router o switch L3), lo que permite aplicar listas de control de acceso (ACLs) y políticas de seguridad estrictas [2], [3].
3. **Flexibilidad Organizativa:** Permite reorganizar la estructura lógica de los departamentos o usuarios mediante software de administración sin tener que modificar físicamente el cableado de la infraestructura [3], [4].

### Clasificación según el Método de Asignación (*Membership*)

* **VLANs Basadas en Puertos (Estáticas):** El administrador asigna manualmente cada puerto físico del switch a una VLAN específica [3], [4]. Es el método más utilizado debido a su simplicidad operativa.
* **VLANs Basadas en Direcciones MAC (Dinámicas):** Los puertos se asignan dinámicamente según la dirección MAC del dispositivo que se conecta. Cuando un host se enchufa a cualquier puerto, el switch consulta su base de datos y le asigna la VLAN correspondiente [3], [4].
* **VLANs Basadas en Protocolo (Capa 3):** Clasifican el tráfico evaluando el campo EtherType de la cabecera de la trama (por ejemplo, separando tráfico IPv4 de IPv6) [3], [4].
* **VLANs Basadas en Subred IP (Capa 3):** Evalúan la dirección IP de origen o la subred a la que pertenece el paquete para asignarle automáticamente la VLAN adecuada [4].

### Clasificación según el Rol Funcional del Tráfico

* **VLAN de Datos / Usuario:** Transporta exclusivamente el tráfico de datos generado por los usuarios finales (navegación web, correo electrónico, transferencia de archivos).
* **VLAN Por Defecto (** **Default VLAN** **):** Es la VLAN configurada de fábrica en el conmutador a la que pertenecen inicialmente todos los puertos (típicamente la VLAN 1) [3].
* **VLAN Nativa:** Utilizada en los enlaces troncales 802.1Q para transportar tramas que **no llevan etiqueta** (*untagged*). Garantiza la compatibilidad con dispositivos que no soportan etiquetado o para tráfico de control del switch.
* **VLAN de Administración (** **Management VLAN** **):** Red reservada específicamente para el acceso y gestión remota del conmutador (mediante SSH, SNMP o HTTPS) a través de una interfaz virtual de conmutación (SVI).
* **VLAN de Voz (** **Voice VLAN** **):** VLAN dedicada al tráfico de telefonía IP (VoIP), configurada con mecanismos de Calidad de Servicio (QoS) para priorizar el tráfico de voz y minimizar el *jitter* y la latencia.

---

### Estándar IEEE 802.1Q y Mecanismo de Tagging

El estándar **IEEE 802.1Q** especifica el mecanismo universal para la multiplexación de múltiples VLANs sobre una única línea física de interconexión entre switches o entre un switch y un router, proceso denominado troncalización de VLANs (VLAN trunking) [3], [4].

**Relación con las VLANs** 
Sin el estándar IEEE 802.1Q, conectar dos conmutadores que albergan $N$ VLANs requeriría utilizar $N$ enlaces físicos y $N$ puertos dedicados en cada switch (un cable por cada VLAN). El protocolo 802.1Q resuelve este problema de escalabilidad mediante la troncalización: un único puerto y cable físico se configuran como un enlace troncal (trunk link) que pertenece a todas las VLANs y transporta el tráfico multiplexado de todas ellas [3].

### Mecanismo de *Tagging* (Etiquetado) en IEEE 802.1Q

El **Tagging** es el procedimiento mediante el cual el conmutador emisor inserta una etiqueta especial de 4 bytes (32 bits) dentro de la cabecera de la trama Ethernet original antes de transmitirla a través de un enlace troncal [3].

Al recibir la trama etiquetada en el extremo opuesto del enlace troncal, el conmutador receptor examina el identificador de la VLAN (**VLAN ID**) dentro de la etiqueta para determinar a qué VLAN pertenece la trama, encamina la información internamente y **remueve la etiqueta** (*untagging*) antes de entregarla al puerto de acceso del destinatario final. De este modo, los sistemas terminales reciben tramas Ethernet estándar sin modificaciones [3], [4].

### Estructura de la Trama Ethernet Etiquetada (IEEE 802.1Q)

**Figura 6.27. Trama Ethernet original (arriba), trama Ethernet con etiquetado 802.1Q (abajo).**
*Fuente: Kurose y Ross, sección 6.4.4.*

<p align="center">
  <img src="./assets/trama_8021q_kurose.png" alt="Trama Ethernet original y trama Ethernet con etiquetado 802.1Q" width="80%" />
</p>

**Campos de la Etiqueta 802.1Q (4 Bytes / 32 Bits)**
1. **TPID (Tag Protocol Identifier - 16 bits):** Contiene el valor hexadecimal fijo 0x8100, el cual indica la presencia de una cabecera de etiquetado VLAN IEEE 802.1Q [3], [4].

2. **TCI (Tag Control Information - 16 bits):** 
    * **PCP (Priority Code Point - 3 bits):** Especifica la prioridad de la trama bajo el estándar IEEE 802.1p para aplicar políticas de Calidad de Servicio (QoS) en Capa 2 (ofrece 8 niveles de prioridad, de 0 a 7) [3], [4].
    
    - **DEI (Drop Eligible Indicator - 1 bit):** Anteriormente conocido como CFI (Canonical Format Indicator) [4], indica si la trama puede ser descartada en presencia de congestión en la red.
    
    * **VID (VLAN Identifier - 12 bits):** Identifica de manera unívoca la VLAN a la que pertenece la trama. Al disponer de 12 bits, permite definir hasta $2^{12} = 4096$ VLANs [3], [4] (con un rango operativo útil de 1 a 4094).
    
**Consideraciones Operativas de la Cabecera 802.1Q**
* **Extensión de Tamaño de Trama:** La inclusión de la etiqueta de 4 bytes incrementa el tamaño máximo de la trama Ethernet de 1518 a 1522 bytes [4].
- **Recálculo del FCS:** Puesto que la cabecera de la trama se modifica al insertar la etiqueta, el switch emisor debe recalcular la secuencia de comprobación de trama (FCS / CRC-32) antes de enviarla por el puerto troncal [3].

---

## Implementación Básica de Conmutación y Segmentación por VLANs

Topología de Red y Tabla de Direccionamiento a implementar:

<p align="center">
  <img src="./assets/topologia.png" alt="Topología" width="80%" />
</p>

<p align="center">
  <img src="./assets/tabla_ruteo.png" alt="Tabla de direccionamiento" width="80%" />
</p>

---

Topología implementada:

<p align="center">
  <img src="./assets/topologia_implementada.png" alt="Topología" width="80%" />
</p>

### Configuración de Seguridad Básica y Direccionamiento en Switches

Se realizó la configuración inicial y el endurecimiento (*hardening*) de la seguridad en los switches `SW-1` y `SW-2` aplicando las convenciones de administración estándar de Cisco IOS.

#### 1. Protección de Accesos y Cifrado de Credenciales
Desde la terminal de cada computadora, conectada por cable de consola, se ingresó al modo de configuración global de cada switch y se configuraron su nombre y las credenciales de administración para restringir el acceso local y remoto:
- **Nombre del dispositivo:** Se asignaron los nombres `sw1` y `sw2` mediante el comando `hostname`.
- **Modo EXEC Privilegiado:** Se asignó la contraseña protegida `class` mediante el comando `enable secret`.
- **Líneas de Consola y VTY (`0 15`):** Se aseguró el acceso físico por puerto serial y el acceso remoto por red mediante la clave `cisco` y la directiva `login`.

<p align="center">
  <img src="./assets/puntos_a_b.png" alt="Configuración del nombre y de las contraseñas de consola y VTY en SW-1" width="50%" />
</p>

Para evitar la exposición de credenciales en texto plano al inspeccionar el archivo de configuración activa (`running-config`), se habilitó la función global `service password-encryption`. Este mecanismo aplica un algoritmo de cifrado reversible sobre todas las contraseñas almacenadas no encriptadas.

<p align="center">
  <img src="./assets/punto_c_sinEncriptar.png" alt="Visualización de contraseñas en texto plano en show running-config" width="40%" />
</p>

<p align="center">
  <img src="./assets/punto_c_encriptado.png" alt="Visualización de contraseñas cifradas tras aplicar service password-encryption" width="40%" />
</p>

#### 2. Configuración de redes VLAN

Se habilitó la Interfaz Virtual de Switch (SVI) sobre la VLAN 1 por defecto para permitir la administración remota Nivel 3 de los switches según la tabla de direccionamiento provista.

<p align="center">
  <img src="./assets/punto_d_sw1.png" alt="Configuración IP de la SVI VLAN 1 en SW-1" width="60%" />
</p>

<p align="center">
  <img src="./assets/punto_d_sw2.png" alt="Configuración IP de la SVI VLAN 1 en SW-2" width="60%" />
</p>

#### 3. Desactivación Preventiva de Puertos Inactivos

Como principio fundamental de seguridad en la Capa de Enlace, se apagaron administrativamente todas las interfaces físicas que no intervienen en la topología mediante la orden shutdown. Esta medida previene conexiones no autorizadas o ataques de acceso físico a la red.

<p align="center">
  <img src="./assets/punto_e_sw1.png" alt="Desactivación de las interfaces sin uso en SW-1" width="70%" />
</p>

<p align="center">
  <img src="./assets/punto_e_sw1(1).png" alt="Verificación del estado de las interfaces de SW-1 mediante show ip interface brief" width="60%" />
</p>

Para el caso de SW-2:
```
sw2(config)# interface range FastEthernet 0/2 - 17, FastEthernet 0/19 - 24, GigabitEthernet 0/1 - 2
sw2(config-if-range)# shutdown
sw2(config-if-range)# exit
```

<p align="center">
  <img src="./assets/punto_e_sw2.png" alt="Verificación de las interfaces de SW-2 y guardado de la configuración" width="60%" />
</p>

#### 4. Guardado de la Configuración y Prueba de Conectividad Inicial

Posteriormente, se respaldaron las configuraciones en la memoria NVRAM de ambos conmutadores ejecutando la orden `copy running-config startup-config`, equivalente a `write memory`.

Se realizó una prueba de conectividad ICMP (`ping`) desde la PC-A (`192.168.10.3`) hacia la PC-B (`192.168.10.4`).

- **Resultado:** Exitoso (0% de pérdida de paquetes).

<p align="center">
  <img src="./assets/punto_g_pca.png" alt="Prueba de ping entre PC-A y PC-B" width="40%" />
</p>

**Justificación técnica:** Al inicio del laboratorio, los puertos `F0/6` (SW-1), `F0/18` (SW-2) y la interfaz inter-switch `F0/1` formaban parte de la VLAN 1 por defecto. Al pertenecer a un único dominio de broadcast a Nivel 2 y compartir la subred IP `192.168.10.0/24`, las tramas Ethernet se conmutaron entre switches sin impedimentos.

#### Creación e identificación de VLANs

Con el objeto de aislar los dominios de broadcast y segmentar el tráfico, se definieron tres VLANs independientes y se reasignaron las interfaces físicas y virtuales.

Se crearon e identificaron las siguientes VLANs en ambos switches:
- VLAN 10 (Laboratorio)
- VLAN 20 (Bar)
- VLAN 99 (Management)

<p align="center">
  <img src="./assets/punto_h_i_sw1.png" alt="Creación e identificación de VLANs en SW-1" width="60%" />
</p>

**VLAN utilizada por defecto:** La salida de `show vlan brief` muestra que la **VLAN 1** (`default`) es la VLAN por defecto. En este punto todos los puertos del switch (`Fa0/1` a `Fa0/24` y `Gig0/1` a `Gig0/2`) siguen perteneciendo a ella, mientras que las VLANs 10, 20 y 99 recién creadas aún no tienen puertos asignados.

#### Asignación de Puertos de Acceso

Se asociaron los puertos donde se encuentran conectadas las computadoras a la VLAN 10 en modo acceso (`access`), garantizando que las tramas ingresadas por dichos puertos pertenezcan únicamente a ese dominio de broadcast:

<p align="center">
  <img src="./assets/punto_j_sw1.png" alt="Configuración en SW-1" width="50%" />
</p>

Para el caso de SW-2:
```
sw2(config)# interface FastEthernet 0/18
sw2(config-if)# switchport mode access
sw2(config-if)# switchport access vlan 10
```

#### Migración de la SVI a la VLAN 99

Para evitar el uso de la VLAN 1 nativa en la gestión de red, se removió la dirección IP asignada a la `interface vlan 1` y se reconfiguró la SVI dentro de la VLAN 99:

<p align="center">
  <img src="./assets/punto_k_l_sw1.png" alt="Verificación de creación de VLANs y puertos asignados mediante show vlan brief" width="60%" />
</p>

<p align="center">
  <img src="./assets/punto_l.png" alt="Verificación del estado operativo de las interfaces virtuales SVI mediante show ip interface brief" width="60%" />
</p>

1. **Análisis de la Tabla de VLANs (`show vlan brief`):**
   - **Segmentación Lógica:** Se confirma la presencia de las VLANs `10` (*Laboratorio*), `20` (*Bar*) y `99` (*Management*) en estado activo dentro de la base de datos de conmutación.
   - **Asignación de Puertos de Acceso:** La interfaz física `F0/6` en `SW-1` (y `F0/18` en `SW-2`) figura asignada correctamente a la **VLAN 10**, habiendo sido desvinculada de la VLAN 1 nativa.
   - **Ausencia de Puertos en VLAN 99:** La **VLAN 99** se encuentra dada de alta pero no registra ningún puerto físico de acceso mapeado directamente a ella.

2. **Análisis del Estado de Interfaces (`show ip interface brief`):**
   - **SVI VLAN 1:** Figura como `unassigned`, confirmando que se removió con éxito la IP de gestión de la VLAN por defecto. La interfaz continúa en estado `up/up` porque el comando `no ip address` solo elimina la dirección IP, sin desactivar la interfaz; para apagarla debería aplicarse `shutdown`.
   - **SVI VLAN 99:** La interfaz virtual registra asignada la dirección IP de administración de Nivel 3 (`192.168.1.11` en `SW-1` / `192.168.1.12` en `SW-2`) con estado administrativo encendido (`Status: up`). Sin embargo, su protocolo de línea figura como **`down`** (`Protocol: down`). Una Interfaz Virtual de Switch (**SVI**) requiere cumplir la condición de **asociación física activa** para pasar al estado operacional `up/up`. Esto significa que el switch debe detectar al menos un puerto físico en estado activo (*up/up*) que pertenezca a la VLAN 99. Al no existir puertos de acceso asignados a la VLAN 99, la SVI 99 carece de una Capa de Enlace subyacente activa, por lo que su protocolo de comunicación permanece en estado **`down`** e impide procesar paquetes IP.

### Análisis de Conectividad y Verificación de la Capa de Enlace

Tras reasignar los puertos de los hosts a la VLAN 10 y migrar las IP de gestión a la VLAN 99, se repitieron las pruebas de transmisión ICMP:

| Prueba | Comando | Resultado |
| :--- | :--- | :--- |
| PC-A → PC-B | `ping 192.168.10.4` (desde PC-A) | ❌ Fallido (*Request timed out*, 100% de pérdida) |
| SW-1 → SW-2 | `ping 192.168.1.12` (desde SW-1) | ❌ Fallido (*Success rate is 0 percent*) |

<p align="center">
  <img src="./assets/punto_n.png" alt="Prueba de ping entre PC-A y PC-B" width="40%" />
</p>

<p align="center">
  <img src="./assets/punto_n2.png" alt="Prueba de ping entre SW-1 y SW-2" width="50%" />
</p>

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

<p align="center">
  <img src="./assets/Punto3_topologia.png" alt="Topología de la red LAN de la aeronave implementada en Packet Tracer" width="80%" />
</p>

La topología se diseñó bajo una arquitectura jerárquica en estrella respaldada por un Switch principal (**Sw**) y un Router principal (**Router Aircraft**). La red fue segmentada lógicamente mediante IEEE 802.1Q en tres VLANs para separar el tráfico según el perfil del usuario:

- **VLAN 10 (Turista - Red 10.10.10.0/24)**: Asignada a los puertos de acceso **Fa0/3** a **Fa0/5** para los pasajeros de clase turista.

- **VLAN 20 (Business - Red 10.10.20.0/24)**: Asignada a los puertos de acceso **Fa0/6** a **Fa0/7** para pasajeros de clase ejecutiva.

- **VLAN 99 (Administración - Red 10.10.99.0/24)**: Asignada a los puertos de acceso **Fa0/2** y **Fa0/8** para la infraestructura y gestión de la aeronave. En esta red se conectó el **Servidor de entretenimiento** mediante el puerto **Fa0/2** con la IP estática **10.10.99.10**, publicando un servicio web local HTTP para la reproducción de contenido multimedia, y la estación de trabajo de administración mediante el puerto **Fa0/8**.

La configuración del switch se verificó con `show interfaces trunk` y `show vlan brief`: el puerto **Fa0/1** opera como troncal con encapsulación 802.1Q y transporta las VLANs 1, 10, 20 y 99, mientras que cada puerto de acceso figura asignado a la VLAN correspondiente.

<p align="center">
  <img src="./assets/Punto3_sw_trunk_vlan.png" alt="Verificación del enlace troncal y de las VLANs en el switch" width="80%" />
</p>

### Ruteo Inter-VLAN (Router-on-a-Stick), Servicio DHCP y Traducción NAT

El enlace entre el puerto **Fa0/1** del Switch y la interfaz **GigabitEthernet0/1** del Router se configuró en modo troncal, permitiendo la transmisión etiquetada de todas las VLANs.

El enrutamiento inter-VLAN se implementó mediante **Router-on-a-Stick**, creando tres subinterfaces lógicas en el Router (**Gi0/1.10**, **Gi0/1.20** y **Gi0/1.99**), las cuales actúan como los gateways predeterminados (`.1`) de cada segmento [2], [3]. Asimismo, el Router se configuró como servidor DHCP centralizado para asignar direcciones IP dinámicas a los clientes de las tres clases [3].

Para el acceso a Internet, la interfaz WAN GigabitEthernet0/0 (`200.0.0.1/30`) se vinculó al enlace del proveedor (ISP) en `200.0.0.2`, aplicando **NAT Overload** (PAT - Traducción de Direcciones de Red con sobrecarga) sobre las redes autorizadas para compartir la dirección IP pública de salida [3].

Para simular Internet, en el router **ISP** se configuró una interfaz **Loopback0** con la dirección `8.8.8.8`, que responde a los pings como si fuera un servidor externo. El Router Aircraft reenvía hacia el ISP (`200.0.0.2`) el tráfico con destino externo. Como el NAT traduce las direcciones privadas a la IP pública `200.0.0.1`, que pertenece a la red directamente conectada al ISP, este puede devolver las respuestas sin conocer las subredes internas `10.10.x.x` [3].

<p align="center">
  <img src="./assets/Punto3_isp_loopback.png" alt="Interfaces del router ISP: enlace con la aeronave y Loopback0 que simula Internet" width="70%" />
</p>

### Políticas de Control de Acceso mediante Listas de Control de Acceso (ACL)

Para garantizar la seguridad de la información y la política comercial del vuelo, se implementó una **Lista de Control de Acceso Extendida (ACL 100)** aplicada de forma entrante (`in`) en la subinterfaz **Gi0/1.10** (Turista) [3]:

```
Extended IP access list 100
    5 permit udp any any eq bootps
    10 permit ip 10.10.10.0 0.0.0.255 10.10.0.0 0.0.255.255
    20 deny ip 10.10.10.0 0.0.0.255 any
```

- **DHCP**: La regla 5 permite las solicitudes DHCP de los clientes Turista. Estas se envían con origen `0.0.0.0` y destino `255.255.255.255` [3], por lo que no coinciden con la regla 10 y, sin esta excepción, serían descartadas por la ACL, dejando a las PCs con una dirección autoconfigurada (`169.254.x.x`).
- **Permisos**: Se permite el tráfico interno originado en la red Turista hacia las demás subredes para dar acceso al Servidor de Entretenimiento (`10.10.99.10`) y permitir la comunicación interna (`10.10.0.0/16`).
- **Restricciones**: La regla 20 deniega todo el resto del tráfico originado en la red Turista, es decir, el dirigido a redes externas e Internet. Asimismo, la lista de acceso estándar 1, asociada al proceso de **NAT Overload**, solo incluye a las subredes Business (`10.10.20.0/24`) y Administración (`10.10.99.0/24`), por lo que la subred Turista tampoco sería traducida para salir a Internet.
- Las redes Business (VLAN 20) y Administración (VLAN 99) cuentan con acceso sin restricciones a Internet y recursos locales.

### Matriz de Pruebas, Validación de Tráfico y Resultados

Luego de configurar la red se realizaron las pruebas propuestas en la consigna, cuyos resultados se resumen a continuación:

| Prueba | Desde | Hacia | Resultado esperado | Resultado obtenido |
| :--- | :--- | :--- | :--- | :--- |
| Ping al servidor de entretenimiento | PC Turista | `10.10.99.10` | ✅ Responde | ✅ Responde |
| Acceso HTTP a servidor local | PC Turista | `http://10.10.99.10` | ✅ Carga la página | ✅ Carga la página |
| Ping a Internet | PC Turista | `8.8.8.8` | ❌ Bloqueado | ❌ Bloqueado (*Destination host unreachable*) |
| Acceso HTTP a servidor local | PC Business | `http://10.10.99.10` | ✅ Carga | ✅ Carga |
| Ping a Internet | PC Business | `8.8.8.8` | ✅ Funciona | ✅ Funciona |
| Ping entre Admin y todos | PC Admin | Turista, Business, servidor e Internet | ✅ Todos | ✅ Todos |

#### Asignación Dinámica de Direcciones (DHCP)

Las tres PCs Turista obtuvieron sus direcciones por DHCP (`10.10.10.11` a `10.10.10.13`). Mediante el comando `ipconfig /all` en la Pc-Turista1 se validó la correcta asignación automática de la dirección IP (`10.10.10.11`), máscara de subred (`255.255.255.0`), gateway predeterminado (`10.10.10.1`) y servidor DHCP configurado en el router.

<p align="center">
  <img src="./assets/Punto3_dhcp_ipconfig.png" alt="Verificación de configuración IP por DHCP en cliente Turista" width="80%" />
</p>

#### Acceso Web al Servidor Local (Turista y Business)

Desde los navegadores web de las PCs Turista y Business se accedió exitosamente a [http://10.10.99.10](http://10.10.99.10), cargando el portal de entretenimiento a bordo.

<p align="center">
  <img src="./assets/Punto3_accesso_PC_turista_HTML.png" alt="Acceso de PC Turista a sitio web local" width="80%" />
</p>

<p align="center">
  <img src="./assets/Punto3_accesso_PC_bussiness_HTML.png" alt="Acceso de PC Business a sitio web local" width="80%" />
</p>

#### Ping al Servidor y Aislamiento de Internet (Turista)

El ping desde la PC Turista hacia el Servidor de Entretenimiento (`10.10.99.10`) obtuvo respuesta, ya que la ACL 100 permite el tráfico hacia las redes internas. En cambio, el ping a `8.8.8.8` devolvió un mensaje de *Destination host unreachable* emitido por el Gateway (`10.10.10.1`), ratificando el bloqueo correcto de Internet por la ACL 100.

<p align="center">
  <img src="./assets/Punto3_ping_PC_turista_internet.png" alt="Ping al servidor y a Internet (8.8.8.8) desde PC Turista" width="60%" />
</p>

#### Salida a Internet (Business)

La ejecución de ping a `8.8.8.8` desde la estación de Business resultó en trazas de eco exitosas, confirmando el funcionamiento del NAT Overload. El primer paquete se pierde mientras se resuelven las direcciones MAC por ARP.

<p align="center">
  <img src="./assets/Punto3_ping_PC_bussiness_internet.png" alt="Ping a Internet (8.8.8.8) desde PC Business" width="80%" />
</p>

#### Conectividad de Administración

La PC de Administración ejecutó pings exitosos hacia una PC Turista (`10.10.10.11`), una PC Business (`10.10.20.11`), el Servidor de Entretenimiento (`10.10.99.10`) e Internet (`8.8.8.8`), demostrando alcance total sobre la red local y salida a Internet mediante NAT Overload. Al igual que en la prueba anterior, el primer paquete hacia las otras VLANs se pierde mientras se resuelve ARP. Además, el TTL de las respuestas permite distinguir el tráfico conmutado dentro de la misma VLAN (servidor, TTL 128) del enrutado entre VLANs por el router (PCs Turista y Business, TTL 127) [3].

<p align="center">
  <img src="./assets/Punto3_ping_PC_admin_todos.png" alt="Ping a todos los segmentos desde PC Admin" width="80%" />
</p>

---

## Conclusión

El trabajo permitió pasar de la teoría de las redes locales a su implementación y validación práctica. Primero se clasificaron las redes según su alcance y se estudiaron las **VLANs** y el estándar **IEEE 802.1Q**, que permite crear dominios de broadcast lógicos independientes y transportarlos por un único enlace troncal.

En la implementación con dos switches, las fallas de conectividad que aparecieron al segmentar la red sin un enlace troncal confirmaron que una VLAN aísla efectivamente el tráfico y que se necesita un trunk 802.1Q para extenderla entre equipos. Luego, la red a bordo de la aeronave integró **VLANs, Router-on-a-Stick, DHCP, NAT Overload y ACLs** para ofrecer servicios diferenciados por clase de pasajero.

La matriz de pruebas validó el diseño. Los clientes obtuvieron su configuración IP por DHCP, todas las clases accedieron al servidor de entretenimiento local, Business y Administración salieron a Internet mediante NAT Overload, Turista quedó bloqueado por la ACL 100 y Administración alcanzó todos los segmentos. Además, el análisis del TTL permitió distinguir el tráfico conmutado dentro de una misma VLAN (TTL 128) del enrutado entre VLANs (TTL 127). En síntesis, se demostró que es posible construir una red segura, ordenada y escalable sobre una única infraestructura física.

---

## Referencias

[1] William Stallings, Comunicaciones y redes de computadores, 7.ª edición, capítulo 1 “Introducción a las comunicaciones de datos y redes”.

[2] Douglas E. Comer, Internetworking with TCP/IP Volume One: Principles, Protocols, and Architecture, 6.ª edición, capítulo 2 “Overview Of Underlying Network Technologies”.

[3] James F. Kurose y Keith W. Ross, Redes de computadoras: Un enfoque descendente, 7.ª edición, capítulos 4 “La capa de red: el plano de datos”, 6 “La capa de enlace y las redes de área local” y 8 “Seguridad en las redes de computadoras”.

[4] Andrew S. Tanenbaum, Redes de computadoras, 4.ª edición, capítulos 1 “Introducción” y 4 “La subcapa de control de acceso al medio”.
