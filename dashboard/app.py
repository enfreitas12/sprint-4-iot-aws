import time
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "sensor_data.jsonl"


st.set_page_config(
    page_title="Dashboard IoT - Totem Flex",
    layout="wide"
)


st.title("Dashboard IoT - Totem Flex Media")
st.caption("Monitoramento simulado do fluxo de pessoas em frente ao totem")


def load_data():
    if not DATA_FILE.exists():
        return pd.DataFrame()

    try:
        return pd.read_json(DATA_FILE, lines=True)
    except ValueError:
        return pd.DataFrame()


df = load_data()


if df.empty:
    st.warning("Aguardando dados do simulador...")
    st.info("Deixe o arquivo iot_simulator.py rodando em outro terminal.")
    time.sleep(2)
    st.rerun()


df["timestamp"] = pd.to_datetime(df["timestamp"])

latest = df.iloc[-1]

total_passages = int(df["passage_counter"].max())
latest_distance = int(latest["distance_cm"])
current_movement = bool(latest["movement_detected"])
total_events = len(df)

status_text = "Pessoa detectada" if current_movement else "Sem pessoa próxima"


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de pessoas detectadas", total_passages)
col2.metric("Última distância medida", f"{latest_distance} cm")
col3.metric("Status em tempo real", status_text)
col4.metric("Eventos recebidos", total_events)


st.divider()


st.subheader("Visualização em tempo real do sensor")

proximity_level = max(0, min(100, int((200 - latest_distance) / 170 * 100)))

st.write(f"Distância atual: **{latest_distance} cm**")
st.write(f"Movimento detectado: **{status_text}**")

st.progress(proximity_level)


if latest_distance <= 60:
    st.error("Pessoa muito próxima do totem")
elif latest_distance <= 100:
    st.warning("Pessoa detectada na área do sensor")
else:
    st.success("Área livre no momento")


st.divider()


col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Distância medida pelo sensor")
    st.line_chart(df.set_index("timestamp")["distance_cm"])

with col_chart2:
    st.subheader("Contador de passagens")
    st.line_chart(df.set_index("timestamp")["passage_counter"])


st.divider()


st.subheader("Eventos recentes recebidos do sensor")

st.dataframe(
    df.tail(10).sort_values("timestamp", ascending=False),
    use_container_width=True
)


df["hour"] = df["timestamp"].dt.hour
movement_df = df[df["movement_detected"] == True]

if not movement_df.empty:
    peak_hour = movement_df.groupby("hour").size().idxmax()
    st.info(f"Horário com maior movimento até agora: {peak_hour}:00")
else:
    st.info("Ainda não há dados suficientes para calcular o horário de pico.")


time.sleep(2)
st.rerun()
