import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

from awscrt import mqtt
from awsiot import mqtt_connection_builder


# =========================
# CONFIGURAÇÕES AWS IOT
# =========================

ENDPOINT = "a2bsol1aioqw1k-ats.iot.us-east-1.amazonaws.com"

CLIENT_ID = "totem-flex-01"

TOPIC = "totem-flex/sensor/passages"


# =========================
# LOCALIZAÇÃO DOS CERTIFICADOS
# =========================

BASE_DIR = Path(__file__).parent
CERTS_DIR = BASE_DIR / "certs"

CERTIFICATE_FILES = list(CERTS_DIR.glob("*-certificate.pem.crt"))
PRIVATE_KEY_FILES = list(CERTS_DIR.glob("*-private.pem.key"))
ROOT_CA_FILE = CERTS_DIR / "AmazonRootCA1.pem"

if not CERTIFICATE_FILES:
    raise FileNotFoundError("Certificado não encontrado dentro da pasta certs.")

if not PRIVATE_KEY_FILES:
    raise FileNotFoundError("Chave privada não encontrada dentro da pasta certs.")

if not ROOT_CA_FILE.exists():
    raise FileNotFoundError("AmazonRootCA1.pem não encontrado dentro da pasta certs.")

PATH_TO_CERTIFICATE = str(CERTIFICATE_FILES[0])
PATH_TO_PRIVATE_KEY = str(PRIVATE_KEY_FILES[0])
PATH_TO_AMAZON_ROOT_CA_1 = str(ROOT_CA_FILE)

print("Certificado encontrado:", PATH_TO_CERTIFICATE)
print("Chave privada encontrada:", PATH_TO_PRIVATE_KEY)
print("Root CA encontrada:", PATH_TO_AMAZON_ROOT_CA_1)


# =========================
# ARQUIVO DO DASHBOARD
# =========================

DASHBOARD_DIR = BASE_DIR.parent / "dashboard"
DASHBOARD_DIR.mkdir(exist_ok=True)

DATA_FILE = DASHBOARD_DIR / "sensor_data.jsonl"

print("Arquivo local para o dashboard:", DATA_FILE)


# =========================
# CONEXÃO MQTT COM AWS IOT
# =========================

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERTIFICATE,
    pri_key_filepath=PATH_TO_PRIVATE_KEY,
    ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("Conectando ao AWS IoT Core...")

connect_future = mqtt_connection.connect()
connect_future.result()

print("Conectado com sucesso!")


# =========================
# SIMULAÇÃO DO SENSOR
# =========================

passage_counter = 0


def generate_sensor_reading():
    global passage_counter

    distance_cm = random.randint(30, 200)

    movement_detected = distance_cm <= 100

    if movement_detected:
        passage_counter += 1

    data = {
        "device_id": CLIENT_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "distance_cm": distance_cm,
        "movement_detected": movement_detected,
        "passage_counter": passage_counter
    }

    return data


# =========================
# LOOP DE ENVIO
# =========================

while True:
    payload = generate_sensor_reading()

    message_json = json.dumps(payload, ensure_ascii=False)

    mqtt_connection.publish(
        topic=TOPIC,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(message_json + "\n")

    print(f"Mensagem enviada: {message_json}")

    time.sleep(3)
