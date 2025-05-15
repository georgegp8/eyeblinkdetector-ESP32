#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define LED 4
#define BUZZER 18

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Tareas y semáforo
TaskHandle_t TareaAlertaVisual;
SemaphoreHandle_t lcdSemaphore;

// Variables compartidas
volatile int conteoParpadeos = 0;
volatile bool alerta = false;
unsigned long tiempoUltimaActualizacion = 0;
const unsigned long TIEMPO_ESPERA_LCD = 5000; // 5 segundos

void setup() {
  Serial.begin(115200);
  Wire.begin();
  lcd.init();
  lcd.backlight();

  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  lcdSemaphore = xSemaphoreCreateBinary();
  xSemaphoreGive(lcdSemaphore);  // inicializa como disponible

  // Crear tareas
  xTaskCreatePinnedToCore(TareaSerial, "TareaSerial", 2048, NULL, 1, NULL, 1);
  xTaskCreatePinnedToCore(TareaAlerta, "TareaAlerta", 2048, NULL, 1, &TareaAlertaVisual, 0);
  xTaskCreatePinnedToCore(TareaLCDIdle, "TareaLCDIdle", 2048, NULL, 1, NULL, 0);
}

void loop() {
  // Nada aquí, todo está en tareas
}

void TareaSerial(void *param) {
  String buffer = "";
  for (;;) {
    if (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {
        if (buffer.startsWith("PARPADEOS:")) {
          conteoParpadeos = buffer.substring(10).toInt();
          alerta = false;

          if (xSemaphoreTake(lcdSemaphore, (TickType_t)10) == pdTRUE) {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Parpadeos:");
            lcd.setCursor(0, 1);
            lcd.print(conteoParpadeos);
            xSemaphoreGive(lcdSemaphore);
          }
          tiempoUltimaActualizacion = millis();

        } else if (buffer == "ALERTA") {
          alerta = true;
          xTaskNotifyGive(TareaAlertaVisual);  // notifica a la tarea de alerta
        }

        buffer = "";
      } else {
        buffer += c;
      }
    }
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void TareaAlerta(void *param) {
  for (;;) {
    ulTaskNotifyTake(pdTRUE, portMAX_DELAY);  // espera notificación
    if (alerta) {
      digitalWrite(LED, HIGH);
      tone(BUZZER, 1000);

      if (xSemaphoreTake(lcdSemaphore, (TickType_t)10) == pdTRUE) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("ALERTA FATIGA!");
        xSemaphoreGive(lcdSemaphore);
      }

      tiempoUltimaActualizacion = millis();
      vTaskDelay(2000 / portTICK_PERIOD_MS);  // espera 2 segundos

      digitalWrite(LED, LOW);
      noTone(BUZZER);
      alerta = false;

      if (xSemaphoreTake(lcdSemaphore, (TickType_t)10) == pdTRUE) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Parpadeos:");
        lcd.setCursor(0, 1);
        lcd.print(conteoParpadeos);
        xSemaphoreGive(lcdSemaphore);
      }

      tiempoUltimaActualizacion = millis();
    }
  }
}

void TareaLCDIdle(void *param) {
  for (;;) {
    if (millis() - tiempoUltimaActualizacion > TIEMPO_ESPERA_LCD) {
      if (xSemaphoreTake(lcdSemaphore, (TickType_t)10) == pdTRUE) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Esperando...");
        xSemaphoreGive(lcdSemaphore);
      }
    }
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}

