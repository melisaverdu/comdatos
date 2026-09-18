# Trabajo Práctico N.º 2: Capa Física y Capa de Enlace de Datos

Trabajo práctico correspondiente a la asignatura **Comunicaciones de Datos** (FCEFyN - UNC).

## Estructura

```text
TP2/
├── assets/
├── informe.md
├── README.md
└── src/
```

### `informe.md`

Documento principal del trabajo práctico. Contiene el desarrollo teórico de los fenómenos de propagación (Doppler), degradación de señal (ruido, interferencia, SNR vs. BER), estrategias de compensación/sincronización y el análisis de la decodificación de tramas en la capa de enlace.

### `assets/`

Recursos gráficos y archivos de datos utilizados en el informe:
* Figuras de consigna (`figura_propagacion.png`, `figura_interferencia.png`).
* Capturas del proceso de análisis y decodificación (`decode.png`, `decode1.png`, `decode2.png`).
* `frames.bin`: Archivo binario con el flujo de tramas serializadas para su procesamiento.

### `src/`

Código fuente en Python para el procesamiento y análisis de tramas:
* `decode.py`: Script utilizado para la lectura, filtrado, extracción y reensamblado secuencial de las tramas contenidas en `frames.bin`.
