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
   ```bash
   git clone https://github.com/tu-usuario/blinkcare.git
   cd blinkcare
