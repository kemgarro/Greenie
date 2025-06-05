#include <DHT.h>
#include <Servo.h>

#define PIN_SERVO 8
#define PIN_LEDS 12
#define PIN_VENTILADOR 2
#define PIN_BOMBA 3
#define PIN_DHT 9
#define PIN_NIVEL_AGUA 7

#define DHTTYPE DHT11
DHT dht(PIN_DHT, DHTTYPE);
Servo servo;

String input;

void setup() {
  Serial.begin(9600);

  // Configurar pines
  pinMode(PIN_LEDS, OUTPUT);
  pinMode(PIN_VENTILADOR, OUTPUT);
  pinMode(PIN_BOMBA, OUTPUT);
  pinMode(PIN_NIVEL_AGUA, INPUT);

  // Inicializar actuadores
  digitalWrite(PIN_LEDS, LOW);           // LED apagado (lógica normal)
  digitalWrite(PIN_VENTILADOR, HIGH);    // Apagar relé (lógica invertida)
  digitalWrite(PIN_BOMBA, HIGH);         // Apagar relé (lógica invertida)

  servo.attach(PIN_SERVO);
  servo.write(0); // Cerrar techo

  dht.begin();
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("ACTIVAR:")) {
      String comp = input.substring(8);
      activar_componente(comp, true);
    } else if (input.startsWith("DESACTIVAR:")) {
      String comp = input.substring(11);
      activar_componente(comp, false);
    } else if (input.startsWith("SERVO:")) {
      int angulo = input.substring(6).toInt();
      servo.write(angulo);
    } else if (input == "LEER:NIVEL") {
      int nivel = digitalRead(PIN_NIVEL_AGUA);
      Serial.println(nivel == HIGH ? "BAJO" : "NORMAL");
    } else if (input == "LEER:DHT") {
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      if (isnan(t) || isnan(h)) {
        Serial.println("ERROR");
      } else {
        Serial.print("T:");
        Serial.print(t);
        Serial.print(" H:");
        Serial.println(h);
      }
    }
  }
}

void activar_componente(String comp, bool activar) {
  int estado;  

  if (comp == "VENTILADOR" || comp == "BOMBA") {
    estado = activar ? LOW : HIGH;  // Lógica invertida para relés
  } else {
    estado = activar ? HIGH : LOW;  // Lógica normal
  }

  if (comp == "LEDS") digitalWrite(PIN_LEDS, estado);
  else if (comp == "VENTILADOR") digitalWrite(PIN_VENTILADOR, estado);
  else if (comp == "BOMBA") digitalWrite(PIN_BOMBA, estado);
}
