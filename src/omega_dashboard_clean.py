import streamlit as st
import sys, os, datetime

sys.path.append(os.path.dirname(__file__))

from signal_engine import get_price_data, generate_signals
from strategy_backtest import compare_strategies

st.set_page_config(page_title="Omega Finance Dashboard", layout="wide")
st.title("📈 Omega Finance Dashboard")
st.caption("Realtime Signale mit Strategie-Backtest & Sentimentanalyse")

symbol = st.selectbox("📊 Markt auswählen:", ["BTC-USD", "GC=F", "ES=F"])

try:
    data = get_price_data(symbol)
    signals = generate_signals(data)

    is_open = not data.empty and data.index[-1].date() == datetime.date.today()
    if is_open:
        st.success("🟢 Markt ist offen – Signale aktiv")
    else:
        st.warning(f"🔒 Markt geschlossen – letzte Daten: {data.index[-1].date()}")

    if not signals.empty:
        sig = signals.iloc[-1]
        st.markdown(f"### 📢 Signal: **{sig['signal']}**")
        st.markdown(f"""
        - Einstieg: `{sig['entry_price']:.2f} USD`  
        - 🎯 T1: {sig['T1']} ({sig['T1_hitrate']}%)  
        - 🎯 T2: {sig['T2']} ({sig['T2_hitrate']}%)  
        - 🎯 T3: {sig['T3']} ({sig['T3_hitrate']}%)  
        - 🎯 T4: {sig['T4']} ({sig['T4_hitrate']}%)  
        """)

    with st.expander("🔬 Strategievergleich"):
        df = compare_strategies(symbol)
        st.dataframe(df)

except Exception as e:
    st.error(f"❌ Fehler beim Laden der Daten: {e}")
