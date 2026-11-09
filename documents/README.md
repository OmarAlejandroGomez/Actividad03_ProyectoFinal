# Sistema de Transporte TransMetro

Proyecto final de la **Actividad Colaborativa N.° 3 

## Integrantes

- Omar Alejandro Gómez Rocha
- Juan Carlos Girón Sanabria
- Cristhian Mauricio Hernández Gaviria

## Problema que resuelve

En un sistema de transporte masivo (del tipo de TransMilenio o MIO), los pasajeros ingresan con una tarjeta personal, abordan distintos tipos de vehículo y recorren rutas que operan en un horario determinado. El sistema administra esa operación así:

- Registra estaciones, rutas con su programación horaria y la flota de vehículos.
- Registra pasajeros y les vincula una tarjeta que se puede recargar, bloquear y desbloquear.
- Valida cada viaje antes de cobrarlo: que la ruta opere a esa hora, que las estaciones pertenezcan a la ruta, que la tarjeta no esté bloqueada y que tenga saldo suficiente.
- Cobra la tarifa según el tipo de vehículo, calcula el tiempo estimado y registra el viaje.
- Genera informes de recaudo total, ingresos por estación y próximas salidas de cada ruta.

## Requisitos y ejecución

- Python **3.10 o superior** (el menú usa `match`/`case`).
- No requiere librerías externas.

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

Se abre un menú de 19 opciones. La opción **18. Ejecutar demostración** crea automáticamente los objetos de prueba, ejecuta los casos normales y excepcionales y muestra los informes. 

## Estructura del proyecto

```
Actividad03_ProyectoFinal/
├── main.py                        # Programa principal: menú, demostración y captura de excepciones
├── controllers/
│   ├── pasajero_controller.py     # Registro y búsqueda de pasajeros
│   └── tarjeta_controller.py      # Registro, búsqueda y vinculación de tarjetas
├── models/
│   ├── sistema_transporte.py      # Coordina estaciones, rutas, flota y viajes
│   ├── vehiculo.py                # Clase abstracta Vehiculo
│   ├── bus_troncal.py             # Hija: bus troncal
│   ├── bus_alimentador.py         # Hija: bus alimentador
│   ├── cable_bus.py               # Hija: cable bus
│   ├── ruta.py                    # Ruta (compone ProgramacionHoraria)
│   ├── programacion_horaria.py    # Horario y frecuencia de una ruta
│   ├── estacion.py                # Estación y conteo de ingresos
│   ├── pasajero.py                # Pasajero titular de una tarjeta
│   ├── tarjeta.py                 # Saldo, bloqueo y cobro
│   ├── viaje.py                   # Registro de un viaje realizado
│   ├── excepciones.py             # Excepciones personalizadas del dominio
│   └── utilidades.py              # Conversión de texto HH:MM a hora
└── docs/
    ├── diagrama_clases.drawio     # Diagrama UML editable (draw.io)
    ├── diagrama_clases.png        # Diagrama UML en imagen
    └── Documento_Decisiones_Diseno.docx
```

## Diagrama de clases

El archivo editable está en [`docs/diagrama_clases.drawio`](docs/diagrama_clases.drawio). Se abre en [app.diagrams.net](https://app.diagrams.net) 

## Cómo se cumplen los requerimientos

| Requerimiento | Dónde se evidencia |
|---|---|
| Seis clases concretas | `SistemaTransporte`, `Estacion`, `Ruta`, `ProgramacionHoraria`, `Pasajero`, `Tarjeta`, `Viaje`, `BusTroncal`, `BusAlimentador`, `CableBus`, `PasajeroController`, `TarjetaController` |
| Una clase abstracta | `Vehiculo(ABC)`, con los métodos abstractos `calcular_tarifa()` y `tiempo_estimado()` |
| Tres clases que heredan de una común | `BusTroncal`, `BusAlimentador` y `CableBus` heredan de `Vehiculo` |
| Constructores | Todas las clases tienen `__init__`. Las hijas invocan `super().__init__(codigo, capacidad)` |
| Encapsulamiento | Los atributos de las entidades usan prefijo `_` y se acceden mediante métodos `get_`/`set_`