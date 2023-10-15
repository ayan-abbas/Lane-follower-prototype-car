int m1a = 2;
int m1b = 3;
int m1e = 4;

int m2a = 5;
int m2b = 6;
int m2e = 7;

int pwm1;
int pwm2;

int base_pwm = 125;

int incoming_byte;

void setup() {
  // put your setup code here, to run once:
  pinMode(m1a, OUTPUT);
  pinMode(m1b, OUTPUT);
  pinMode(m1e, OUTPUT);
  pinMode(m2a, OUTPUT);
  pinMode(m2b, OUTPUT);
  pinMode(m2e, OUTPUT);
  
  digitalWrite(m1a, HIGH);
  digitalWrite(m1b, LOW);
  digitalWrite(m1e, LOW);
  digitalWrite(m2a, HIGH);
  digitalWrite(m2b, LOW);
  digitalWrite(m2e, LOW);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    incoming_byte = Serial.read();
    (float) incoming_byte;

    pwm1 = base_pwm + angle * sensitivity;
    pwm2 = base_pwm - angle * sensitivity;

    analogWrite(m1e, pwm1);
    analogWrite(m2e, pwm2);
  }
  digitalWrite(m1e, LOW);
  digitalWrite(m2e, LOW);
}
