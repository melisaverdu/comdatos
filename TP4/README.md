# Trabajo Práctico N.º 4: Capas de Acceso en Redes Locales, Protocolos y Fundamentos

Trabajo práctico correspondiente a la asignatura **Comunicaciones de Datos** (FCEFyN - UNC).

## Estructura

```text
TP4/
├── assets/
├── pkt/
├── src/
├── informe.md
└── README.md
```

### `informe.md`

Documento principal del trabajo práctico. Contiene el desarrollo teórico y práctico de:
* Clasificación de redes según su alcance (BAN, PAN, LAN, CAN, MAN y WAN).
* Fundamentos de VLANs: propósitos, métodos de asignación, roles funcionales y estándar IEEE 802.1Q (estructura de la trama etiquetada y mecanismo de *tagging*).
* Implementación básica de conmutación en Packet Tracer: seguridad de switches, creación de VLANs, asignación de puertos, migración de la SVI de gestión a la VLAN 99 y diagnóstico de las fallas de conectividad.
* Despliegue de una red LAN a bordo de una aeronave: VLANs por clase de pasajero, servidor de entretenimiento local, Router-on-a-Stick, DHCP, NAT Overload, ACLs y matriz de pruebas.

### `pkt/`

Archivos de simulación de Cisco Packet Tracer:
* `TP4_punto2.pkt`: topología de dos switches con segmentación por VLANs.
* `Tp4_punto3.pkt`: red LAN de la aeronave.

### `assets/`

Recursos gráficos y capturas de pantalla utilizadas en el informe:
* Figura de clasificación de redes por alcance.
* Topología, tabla de direccionamiento y capturas de configuración y verificación de los switches (`show running-config`, `show vlan brief`, `show ip interface brief`).
* Capturas de las pruebas de conectividad (`ping`) entre PCs y entre switches.
* Capturas de la red de la aeronave: asignación por DHCP, acceso web al servidor local y pruebas de salida a Internet por clase.
