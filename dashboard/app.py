# dashboard/app.py
import streamlit as st
import plotly.graph_objects as go
import time
from crew.swarm import run_hour, trades, total_kwh, total_usd
from simulator.microgrid import households

st.set_page_config(page_title="EnerGPT", layout="wide")
st.title("EnerGPT — AI Agents Trading Energy Live")
st.caption("20 Claude-powered houses negotiating P2P energy right now")

if st.button("START 24-HOUR SIMULATION", type="primary"):
    st.session_state.hour = 6
    trades.clear()

col1, col2 = st.columns([2, 1])
chart = col1.empty()
log = col2.empty()
m1, m2 = st.columns(2)

for hour in range(st.session_state.get("hour", 6), 30):
    run_hour(hour)
    time.sleep(1)

    # Sankey (simplified but beautiful)
    fig = go.Figure(go.Sankey(
        node = dict(label = [h.persona for h in households[:10]]),
        link = dict(source = [0]*len(trades[-20:]), target = [1]*len(trades[-20:]), value = [1]*len(trades[-20:]))
    ))
    chart.plotly_chart(fig, use_container_width=True)

    log.markdown("### Live Trades\n" + "\n\n".join(reversed(trades[-20:])))
    m1.metric("Total kWh Traded", f"{total_kwh:.1f}")
    m2.metric("Total $ Value", f"${total_usd:.2f}")

    st.session_state.hour = hour + 1
    st.rerun()

st.balloons()