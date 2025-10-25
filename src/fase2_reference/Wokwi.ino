#include <DHT.h>

// === Pinos ===
#define LDR_PIN   34
#define DHT_PIN   15
#define RELAY_PIN 23
#define BTN_N     21
#define BTN_P     19
#define BTN_K     18

// === DHT22 ===
#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

// === Threshold base ===
float BASE_ON  = 35.0;           // base p/ ligar (sem faltas)
float STEP_PER_MISSING = 3.0;    // +% por nutriente faltando
float HYST = 5.0;                // OFF = ON + HYST

// === pH (via LDR) ===
float PH_MIN = 5.5;
float PH_MAX = 7.5;
float PH_PENALTY = 2.0;          // +% se pH fora da faixa

// === Anti-pisca (tempos mínimos) ===
const unsigned long MIN_ON_MS  = 8000; // 8s ligado
const unsigned long MIN_OFF_MS = 5000; // 5s desligado

// === Integração externa ===
float rain_mm_forecast = 0.0f;   // RAIN=<mm> vindo do Python
int   pop_forecast = 0;          // POP=<0..100> vindo do Python
bool  followR = true;            // FOLLOWR=1/0 (seguir decisão do R?)
int   rdec = -1;                 // RDEC=1 (ligar) / 0 (desligar) / -1 (sem decisão)
unsigned long rdecMs = 0;
const unsigned long RDEC_TTL_MS = 15000; // 15s de validade da decisão do R

// Janela para “segurar” irrigação se tiver chuva prevista
bool rainHold = false;
unsigned long rainHoldMs = 0;
const unsigned long RAIN_HOLD_MS = 15000; // 15s de hold (ajuste livre)

bool relayState = false;
unsigned long lastChangeMs = 0;

void applyRelay(bool desired) {
  unsigned long now = millis();

  if (desired && !relayState) {
    if (now - lastChangeMs >= MIN_OFF_MS) {
      relayState = true;
      digitalWrite(RELAY_PIN, HIGH);
      lastChangeMs = now;
      Serial.println(">> Acionando irrigacao (respeitado tempo minimo OFF).");
    } else {
      Serial.println(".. Aguardando tempo minimo OFF para ligar.");
    }
  } else if (!desired && relayState) {
    if (now - lastChangeMs >= MIN_ON_MS) {
      relayState = false;
      digitalWrite(RELAY_PIN, LOW);
      lastChangeMs = now;
      Serial.println(">> Desligando irrigacao (respeitado tempo minimo ON).");
    } else {
      Serial.println(".. Aguardando tempo minimo ON para desligar.");
    }
  }
}

void handleSerial() {
  if (!Serial.available()) return;
  String s = Serial.readStringUntil('\n');
  s.trim();

  if (s.startsWith("RAIN=")) {
    rain_mm_forecast = s.substring(5).toFloat();
    Serial.print(">> RAIN(mm) recebido: "); Serial.println(rain_mm_forecast);
    if (rain_mm_forecast >= 2.0f || pop_forecast >= 60) {
      rainHold = true; rainHoldMs = millis();
      Serial.println(">> Ativando hold por chuva prevista.");
    }
  } else if (s.startsWith("POP=")) {
    pop_forecast = s.substring(4).toInt();
    Serial.print(">> POP(%) recebido: "); Serial.println(pop_forecast);
    if (rain_mm_forecast >= 2.0f || pop_forecast >= 60) {
      rainHold = true; rainHoldMs = millis();
      Serial.println(">> Ativando hold por chuva prevista.");
    }
  } else if (s.startsWith("RDEC=")) {       // decisão do R: 1 ligar, 0 desligar
    rdec = s.substring(5).toInt();
    rdecMs = millis();
    Serial.print(">> RDEC recebido (R): "); Serial.println(rdec);
  } else if (s.startsWith("FOLLOWR=")) {
    followR = (s.substring(8).toInt() != 0);
    Serial.print(">> FOLLOWR: "); Serial.println(followR ? "ON" : "OFF");
  } else if (s == "STATUS") {
    Serial.print("STATUS rain="); Serial.print(rain_mm_forecast);
    Serial.print(" pop="); Serial.print(pop_forecast);
    Serial.print(" rdec="); Serial.print(rdec);
    Serial.print(" followR="); Serial.print(followR);
    Serial.print(" hold="); Serial.println(rainHold);
  } else if (s == "CLEAR") {
    rain_mm_forecast = 0; pop_forecast = 0; rdec = -1; rainHold = false;
    Serial.println(">> Limpou variaveis externas.");
  } else {
    Serial.print("Comando desconhecido: "); Serial.println(s);
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(LDR_PIN, INPUT);
  pinMode(BTN_N, INPUT_PULLUP);
  pinMode(BTN_P, INPUT_PULLUP);
  pinMode(BTN_K, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  lastChangeMs = millis();

  Serial.println("ESP32 pronto: NPK + pH + anti-pisca + comandos Serial (RAIN/POP/RDEC/FOLLOWR).");
  Serial.println("Exemplos: RAIN=3   POP=70   RDEC=0   FOLLOWR=1   STATUS");
}

void loop() {
  handleSerial();

  // Leituras
  int   ldrRaw      = analogRead(LDR_PIN);
  float humidity    = dht.readHumidity();
  float temperature = dht.readTemperature();
  float ph = (ldrRaw / 4095.0f) * 14.0f;

  // Botoes (pressionado=1)
  bool N_ok = !digitalRead(BTN_N);
  bool P_ok = !digitalRead(BTN_P);
  bool K_ok = !digitalRead(BTN_K);
  int missing = (N_ok ? 0 : 1) + (P_ok ? 0 : 1) + (K_ok ? 0 : 1);

  // Threshold dinâmico (NPK + pH)
  float ON  = BASE_ON + missing * STEP_PER_MISSING;
  float OFF = ON + HYST;
  bool phOff = (ph < PH_MIN || ph > PH_MAX);
  if (phOff) { ON += PH_PENALTY; OFF = ON + HYST; }

  if (ON  < 15) ON  = 15;
  if (ON  > 70) ON  = 70;
  if (OFF > 90) OFF = 90;

  // Decide desejado
  bool desired = relayState;
  if (!isnan(humidity)) {
    if (humidity < ON)  desired = true;
    if (humidity > OFF) desired = false;
  }

  // 1) Janela de "suspender por chuva"
  unsigned long now = millis();
  if (rainHold && (now - rainHoldMs) < RAIN_HOLD_MS) {
    desired = false; // suspende irrigação temporariamente
  } else if (rainHold && (now - rainHoldMs) >= RAIN_HOLD_MS) {
    rainHold = false; // fim da janela
  }

  // 2) Decisão do R (se FOLLOWR=1 e decisão recente)
  if (followR && rdec != -1 && (now - rdecMs) < RDEC_TTL_MS) {
    desired = (rdec == 1);
  }

  // Aplica com anti-pisca
  applyRelay(desired);

  // Log
  Serial.println("===== Estado Atual =====");
  Serial.print("Umidade: "); Serial.print(humidity); Serial.println(" %");
  Serial.print("Temp: ");    Serial.print(temperature); Serial.println(" C");
  Serial.print("LDR: ");     Serial.print(ldrRaw);
  Serial.print("  pH(sim): "); Serial.println(ph, 2);
  Serial.print("pH_OK: "); Serial.println(phOff ? "NAO" : "SIM");
  Serial.print("N(OK): "); Serial.print(N_ok);
  Serial.print("  P(OK): "); Serial.print(P_ok);
  Serial.print("  K(OK): "); Serial.println(K_ok);
  Serial.print("Faltando: "); Serial.println(missing);
  Serial.print("ON: "); Serial.print(ON);
  Serial.print("  OFF: "); Serial.println(OFF);
  Serial.print("Rain(mm): "); Serial.print(rain_mm_forecast);
  Serial.print("  POP(%): "); Serial.print(pop_forecast);
  Serial.print("  HoldChuva: "); Serial.print(rainHold ? "ATIVO" : "NAO");
  Serial.print("  RDEC: "); Serial.print(rdec);
  Serial.print("  FOLLOWR: "); Serial.println(followR ? "ON" : "OFF");
  Serial.print("Irrigacao: "); Serial.println(relayState ? "LIGADA" : "DESLIGADA");
  Serial.println("========================\n");

  delay(2000);
}
