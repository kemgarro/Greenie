#include <Servo.h>
Servo miServo;

int pinServo = 9;    // Pin PWM para el servo (usa ~9, ~10, ~11 en Arduino Uno)
int pinPot = A0;     // Pin del potenciómetro

void setup() {
  miServo.attach(pinServo);  // Inicializa el servo
  Serial.begin(9600);        // Inicia comunicación serial
  Serial.println("Iniciando control de servo con potenciómetro...");
}

void loop() {
  int valorPot = analogRead(pinPot);            // Lee el potenciómetro (0-1023)
  int angulo = map(valorPot, 0, 1023, 0, 180); // Convierte a ángulo (0-180°)
  
  miServo.write(angulo);                       // Mueve el servo
  Serial.print("Valor Pot: ");
  Serial.print(valorPot);
  Serial.print(" | Ángulo: ");
  Serial.println(angulo);
  
  delay(100);  // Pequeña pausa para estabilidad y lectura serial
}