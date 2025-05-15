# BlinkCare 👁️🧠

> Proyecto desarrollado por estudiantes de **Tecsup** - 4to Ciclo de Diseño y Desarrollo de Software.

## 📌 Descripción

**BlinkCare** es un sistema de monitoreo de parpadeo en tiempo real diseñado para prevenir la fatiga ocular, especialmente en personas que trabajan largas horas frente a una pantalla. Utiliza **visión por computadora**, inteligencia artificial con **MediaPipe**, y comunicación serial con un **ESP32**, que activa alertas físicas como un LED, un buzzer y un display LCD I2C.

---

## 🎯 Objetivos

- Detectar el parpadeo humano usando la cámara con precisión.
- Emitir una alerta si no se detecta parpadeo durante un tiempo crítico.
- Enviar el conteo de parpadeos al microcontrolador ESP32.
- Mostrar la información en un LCD I2C y activar una alarma visual/auditiva.

---

## 🛠️ Tecnologías Utilizadas

### 💻 Python (PC)

- [MediaPipe](https://google.github.io/mediapipe/)
- OpenCV
- PySerial
- NumPy

### 🔌 ESP32 (Microcontrolador)

- Arduino IDE con FreeRTOS integrado
- Manejo de tareas (`xTaskCreate`)
- Comunicación serial USB
- Salidas: LED, buzzer, LCD I2C

---

## 📦 Instalación (PC)

1. Clona el repositorio:
   git clone https://github.com/tu-usuario/blinkcare.git
   cd blinkcare
2. Crea entorno virtual
   python -m venv blinkvenv
   blinkvenv\Scripts\activate  # En Windows
3. Instala dependencias
   pip install -r requirements.txt
4. Ejecuta el script principal
   python blink_detector.py

## ⚙️ Comunicación con ESP32
El script envía:
- "PARPADEOS:X" → Muestra en LCD.
- "ALERTA" → Enciende LED y buzzer durante 2 segundos.
- El ESP32 ejecuta tareas simultáneas con FreeRTOS:
- TareaSerial: escucha comandos.
- TareaAlerta: maneja alerta visual/auditiva.
- TareaLCDIdle: muestra "Esperando..." tras 5s de inactividad.

## 🧪 Pruebas Realizadas
- Validación de EAR (Eye Aspect Ratio) para diferentes personas.
- Simulación de no parpadear (alerta activa).
- Comunicación serial robusta con el ESP32.
- Verificación física de LED, buzzer y LCD con código separado.
