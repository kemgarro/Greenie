#include <DHT.h>
#include <Servo.h>

// Pines de componentes
#define PIN_SERVO        8   // Techo
#define PIN_LEDS         12  // Luz artificial
#define PIN_BOMBA        3   // Riego
#define PIN_VENTILADOR   2   // Ventilación
#define PIN_DHT          9   // Sensor DHT

// Tipo de sensor: DHT11 o DHT22
#define TIPO_DHT DHT11

DHT dht(PIN_DHT, TIPO_DHT);
Servo servo;
String input;

void setup() {
  Serial.begin(9600);
  dht.begin();

  // Luz artificial
  pinMode(PIN_LEDS, OUTPUT);
  digitalWrite(PIN_LEDS, LOW);  // Apagado

  // Riego (lógica invertida)
  pinMode(PIN_BOMBA, OUTPUT);
  digitalWrite(PIN_BOMBA, HIGH);  // Apagado

  // Ventilador (lógica invertida)
  pinMode(PIN_VENTILADOR, OUTPUT);
  digitalWrite(PIN_VENTILADOR, HIGH);  // Apagado

  // Servo (techo)
  servo.attach(PIN_SERVO);
  servo.write(0); // Techo cerrado
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();

    // 🔆 Luz
    if (input == "ACTIVAR:LEDS") {
      digitalWrite(PIN_LEDS, HIGH);
      Serial.println("LUZ:ENCENDIDA");
    } 
    else if (input == "DESACTIVAR:LEDS") {
      digitalWrite(PIN_LEDS, LOW);
      Serial.println("LUZ:APAGADA");
    }

    // 💧 Riego
    else if (input == "ACTIVAR:BOMBA") {
      digitalWrite(PIN_BOMBA, HIGH);
      Serial.println("RIEGO:ENCENDIDO");
    } 
    else if (input == "DESACTIVAR:BOMBA") {
      digitalWrite(PIN_BOMBA, LOW);
      Serial.println("RIEGO:APAGADO");
    }

    // 🌬️ Ventilador
    else if (input == "ACTIVAR:VENTILADOR") {
      digitalWrite(PIN_VENTILADOR, HIGH);
      Serial.println("VENTILADOR:ENCENDIDO");
    } 
    else if (input == "DESACTIVAR:VENTILADOR") {
      digitalWrite(PIN_VENTILADOR, LOW);
      Serial.println("VENTILADOR:APAGADO");
    }

    // 🪟 Techo (servo)
    else if (input.startsWith("SERVO:")) {
      int angulo = input.substring(6).toInt();
      angulo = constrain(angulo, 0, 180);
      servo.write(angulo);
      Serial.print("TECHO:MOVIDO_A:");
      Serial.println(angulo);
    }

    // 🌡️ Lectura temperatura y humedad
    else if (input == "LEER:DHT") {
      float temperatura = dht.readTemperature();
      float humedad = dht.readHumidity();

      if (isnan(temperatura) || isnan(humedad)) {
        Serial.println("ERROR:LECTURA");
      } else {
        Serial.print("T:");
        Serial.print(temperatura);
        Serial.print(" H:");
        Serial.println(humedad);
      }
    }

    // 💦 Lectura solo de humedad (para gráfico humedad)
    else if (input == "LEER:HUMEDAD") {
      float humedad = dht.readHumidity();

      if (isnan(humedad)) {
        Serial.println("ERROR:HUMEDAD");
      } else {
        // Aquí puedes cambiar el estado "cerrado" por "abierto" si lees el ángulo real del servo
        Serial.print(humedad);
        Serial.println("|cerrado");
      }
    }
  }
}
