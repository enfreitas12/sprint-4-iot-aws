\# Sprint 4 - IoT na AWS | Totem Flex Media



Projeto desenvolvido para a Sprint 4 do projeto integrado, com foco em integração IoT na AWS.



A solução simula um dispositivo IoT baseado em ESP32 com sensor ultrassônico/radar para monitorar o fluxo de pessoas em frente a um totem.



\## Objetivo



Criar uma solução capaz de:



\- simular leituras de distância de um sensor;

\- detectar presença/movimento;

\- contar passagens de pessoas;

\- enviar mensagens MQTT para o AWS IoT Core;

\- exibir os dados em um dashboard em tempo real.



\## Arquitetura



Fluxo da solução:



1\. O simulador Python gera leituras de distância.

2\. Quando a distância é menor ou igual a 100 cm, o sistema considera que houve presença.

3\. O contador de passagens é atualizado.

4\. Os dados são enviados ao AWS IoT Core via MQTT.

5\. Os dados também são salvos localmente.

6\. O dashboard em Streamlit exibe as informações em tempo real.



\## Tecnologias utilizadas



\- Python

\- AWS IoT Core

\- MQTT

\- Streamlit

\- Pandas

\- Certificados X.509



\## Estrutura do projeto



```text

sprint-4-iot-aws/

├── iot-simulator/

│   ├── certs/

│   ├── iot\_simulator.py

│   └── requirements.txt

├── dashboard/

│   ├── app.py

│   └── requirements.txt

├── .gitignore

└── README.md

```

## Exemplo de mensagem enviada

```json
{
  "device_id": "totem-flex-01",
  "timestamp": "2026-05-22T18:47:12.593680+00:00",
  "distance_cm": 85,
  "movement_detected": true,
  "passage_counter": 1
}
```

## Tópico MQTT

```text
totem-flex/sensor/passages
```

## Executar o simulador

```bash
cd iot-simulator
python -m pip install -r requirements.txt
python iot_simulator.py
```

## Executar o dashboard

```bash
cd dashboard
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Observação sobre certificados

Os certificados da AWS IoT Core não devem ser enviados ao GitHub.

A pasta `iot-simulator/certs` deve conter localmente os arquivos:

```text
certificate.pem.crt
private.pem.key
public.pem.key
AmazonRootCA1.pem
```

## Funcionalidades

- Simulação de sensor IoT
- Envio MQTT para AWS IoT Core
- Contador de passagens
- Dashboard em tempo real
- Gráfico de distância
- Gráfico de passagens
- Eventos recentes do sensor
- Horário com maior movimento

## Status

Projeto funcional para demonstração da Sprint 4.

