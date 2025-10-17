# Weekly Spotlights
This page is a collection of weekly spotlights that highlight the progress of the integration team. Each spotlight is a summary of the work done by the team in a week.

Member status:

- 🔍: Research
- 💻: Development
- 📝: Documentation
- 🔄: Refactoring
- 🔧: Bug fixing
- 🤝: Participation in other subteam

## 2025-3-6

| Name     | Stauts |
| -------- | ------ |
| Samuel       |    🔍    |
| Fregoso |     💻   |
| Melanie    |   🤝   |
| Ximena |    Paused  |
| Rogelio   |    Paused     |
| Rodrigo  |  🔍   |
| Daniel hinojosa |   💻  |


**Development**:


**On planning**:

-Review of the usefulness of the pudu batteries
-Review of how the dog's batteries are if you carry them
-Review of BMS papers

Proyecto: Desarrollo de un sistema de energía modular y de alta disponibilidad para alimentar una plataforma robótica compuesta por una Jetson AGX Orin, un brazo robótico XArm y motores de propulsión.

Objetivo: Diseñar e implementar un sistema de baterías intercambiables con una capacidad total de 400 Wh, compuesto por 8 bancos de ~100 Wh, con un sistema de carga centralizado y monitoreo en tiempo real.

**Diseño del banco de baterias**
Cada uno de los 8 bancos de baterías será una unidad independiente y reemplazable.

Celda Seleccionada: Se utilizarán celdas de Ion de Litio formato 18650 de alta tasa de descarga (High-Drain). Esta elección es crítica para suplir los picos de corriente que demandarán los motores y el brazo robótico.

Ejemplo de celdas: Molicel P26A, Sony/Murata VTC5A.

Configuración Eléctrica: 7S2P (7 celdas en serie y 2 en paralelo).

En Serie (7S): 7 celdas conectadas en serie para alcanzar el voltaje nominal del sistema.

7 celdas * 3.6V/celda = 25.2V (Voltaje nominal).

El rango de operación será de aprox. 21V (descargado) a 29.4V (cargado).


**Sistema de gestion**
Para un sistema modular e intercambiable, una topología centralizada es inviable. La elección correcta es una topología Descentralizada (o Distribuida) con arquitectura Maestro-Esclavo.

BMS Esclavo (Slave): Cada uno de los 8 bancos de baterías llevará integrada una pequeña placa BMS esclava.

Función: Monitorear voltajes y temperaturas de sus 14 celdas, realizar el balanceo activo/pasivo y comunicarse con el maestro.

BMS Maestro (Master): Una única placa controladora que gestiona todo el sistema.

Función: Recolectar datos de todos los esclavos conectados, calcular el estado de carga (SoC) global, controlar el contactor principal (interruptor de potencia) y gestionar el proceso de carga centralizada.

Justificación: Esta topología es la estándar en vehículos eléctricos y sistemas de almacenamiento de energía por su fiabilidad, escalabilidad y seguridad. Si un banco falla, su esclavo lo reporta y el maestro puede aislarlo sin comprometer todo el sistema.

**Monitoreo en la jetson**
El monitoreo se realizará desde la Jetson AGX Orin, que actuará como la unidad de control principal (Host). El flujo de datos será el siguiente:

Adquisición: Cada BMS Esclavo mide continuamente los voltajes y temperaturas de su banco y los envía al BMS Maestro a través del bus de comunicación CAN.

Centralización: El BMS Maestro recibe los datos de todos los bancos conectados. Agrega esta información, calcula el Estado de Carga (SoC) y el Estado de Salud (SoH) de cada banco y del sistema en general.

Interfaz Host: El BMS Maestro se conecta a la Jetson AGX Orin a través de una de sus interfaces de comunicación (preferiblemente CAN, pero también puede ser USB o UART). El Maestro enviará paquetes de datos estandarizados con toda la información relevante.

Visualización:

En la Jetson se ejecutará una aplicación (desarrollada en Python o C++) que:

Lee el puerto de comunicación para recibir los datos del BMS Maestro.

Decodifica los paquetes de datos para extraer la información.

Presenta la información en una Interfaz Gráfica de Usuario (GUI).

Datos a mostrar en la GUI:

SoC Global (%): El nivel de batería total del sistema.

Vista por Banco: Un listado de los 8 bancos, mostrando el SoC individual, voltaje y temperatura de cada uno.

Corriente del Sistema (A): Consumo actual en tiempo real.

Estado del Sistema: Indicadores de "Cargando", "Descargando", "Standby" o "FALLA".

Alertas: Notificaciones visuales para sobrecalentamiento, bajo voltaje o cualquier otra anomalía detectada por el BMS.

**Que necesita hacer los BMS**
Sección Analógica (para cada esclavo):

Medición de Voltaje: Divisores de tensión de alta precisión para cada una de las 7 series de celdas, conectados a un multiplexor y un convertidor Analógico-Digital (ADC) de alta resolución (mínimo 12 bits).

Medición de Temperatura: Entradas para termistores NTC estratégicamente colocados en el paquete de baterías.

Circuito de Balanceo: Un conjunto de MOSFETs y resistencias de potencia para cada serie de celdas, que permitan "drenar" una pequeña cantidad de energía de las celdas con mayor voltaje para igualarlas con las demás.

Sección de Control (Microcontrolador - MCU):

Un MCU (ej. de las familias STM32, PIC, o ESP32) que lea los datos del ADC, ejecute los algoritmos de protección y balanceo, y gestione la comunicación.

Sección de Comunicación:

Transceptor CAN (CAN Transceiver): Un chip como el MCP2551 o TJA1050 que traduce las señales del MCU al protocolo físico del bus CAN, el cual es muy robusto contra el ruido eléctrico de los motores.

Sección de Potencia y Protección (para el Maestro):

Medición de Corriente: Un sensor de efecto Hall o una resistencia "shunt" de alta potencia para medir la corriente total del sistema.

Control de Contactores/MOSFETs: Circuitos para activar relés de estado sólido (contactores) o bancos de MOSFETs de alta potencia que puedan conectar o desconectar físicamente la batería del resto del robot en caso de una falla.

**Materiales**
Banco de baterias x8
Celdas 18650:

Cantidad: 7 celdas por banco.

Especificación clave: Deben ser de alta tasa de descarga (High-Drain) de una marca reconocida (ej. Molicel, Murata/Sony, LG, Samsung).

BMS Esclavo (Slave Board):

Cantidad: 1 por banco.

Función: Es la pequeña placa que se monta directamente en el banco de baterías para monitorear sus celdas y comunicarse con el BMS Maestro.

Portapilas (Cell Holders):

Cantidad: Suficientes para 7 celdas (1x7).

Función: Dan estructura al paquete y mantienen las celdas separadas para una mejor refrigeración y seguridad.

Tiras de Níquel Puro (Pure Nickel Strips):

Función: Para conectar las terminales de las celdas entre sí mediante soldadura por puntos. Es crucial que sea níquel puro, no acero niquelado, para una mejor conductividad.

Conector de Potencia y Comunicación:

Cantidad: 1 por banco.

Función: Un conector robusto que lleve tanto la energía (positivo y negativo) como las líneas de comunicación (CAN-H y CAN-L) hacia el sistema principal. Un conector tipo XT90 para la potencia y un conector más pequeño para la comunicación es una buena opción.

Material de Aislamiento y Montaje:

Aisladores autoadhesivos ("fish paper") para los terminales positivos de las celdas.

Cinta Kapton para aislar conexiones.

Cable de silicona (12 AWG para potencia, 22-24 AWG para balanceo y comunicación).

Tubo termorretráctil grande para envolver y proteger todo el banco terminado.

Cargador de Baterías de Ion de Litio:

Especificación clave: Debe ser un cargador para sistemas 7S, lo que significa que su voltaje máximo de salida debe ser de 29.4V.

Potencia: La corriente de salida (en Amperios) determinará qué tan rápido se cargan todos los bancos. Un cargador de 10A o 20A sería adecuado para cargar los 8 bancos en un tiempo razonable.

Recomendación: Un cargador que pueda ser controlado por el BMS (si el BMS Maestro tiene esa función) para una carga más segura e inteligente.

SISTEMA CENTRAL
BMS Maestro (Master Board):

Cantidad: 1 para todo el sistema.

Función: El cerebro del sistema. Recibe la información de todos los esclavos, controla el contactor principal y se comunica con tu Jetson.

Contactor o Relé de Estado Sólido:

Cantidad: 1.

Función: Es un interruptor electromecánico de alta potencia controlado por el BMS Maestro. Es el encargado de conectar o desconectar de forma segura toda la energía de las baterías al resto del robot. Debe soportar al menos 50V y más de 100A.

Fusible Principal:

Cantidad: 1.

Función: Un fusible de alta corriente (100A) que se coloca justo después del contactor

Bus de Conexión (Busbar) o Placa de Distribución de Potencia (PDB):

Función: Un punto de conexión común donde los conectores de los 8 bancos de baterías se conectan en paralelo. Puede ser una simple barra de cobre o una placa de circuito impreso (PCB) diseñada para alta corriente.

Cableado del Bus de Comunicación:

Cable de par trenzado para conectar todos los BMS esclavos y el maestro en una red CAN bus.

Ejemplos de BMS

Batrium BMS (Serie WatchMon), viene con interfaz de usuario y esclavos pero mas caro, pero nos podemos basar en eso

Open source
https://enaccess.org/materials/battery-management-system/