# Omega Bot Ultra Pro – FIXED VERSION

📈 Realtime Signale & Strategievergleich mit:
- RSI, MACD, Volumen
- EMA-Trendanalyse
- Breakout & Sentiment (optional)
- Daytrading mit Zielzonen & Trefferquoten
- Börsenstatusprüfung (offen/geschlossen)

## Start (lokal)

```bash
pip install -r requirements.txt
streamlit run src/omega_dashboard_clean.py

---

## 🔧 src/omega_dashboard_clean.py

```python
import streamlit as st
import datetime
from signal_engine import get_price_data, generate_signals
from strategy_backtest import compare_strategies

st.set_page_config(page_title="Omega Finance Dashboard", layout="wide")
st.title("📈 Omega Finance Dashboard")
st.caption("Realtime Signale mit Strategie-Backtest & Sentimentanalyse")

symbol = st.selectbox("📊 Markt auswählen:", ["BTC-USD", "GC=F", "ES=F"])

try:
    data = get_price_data(symbol)

    if data.empty:
        st.error("🚫 Keine Daten verfügbar – Börse eventuell geschlossen.")
    else:
        last_date = data.index[-1].date()
        is_open = last_date == datetime.date.today()

        if is_open:
            st.success("🟢 Markt ist offen – Signale aktiv")
        else:
            st.warning(f"🔒 Markt geschlossen – letzte Daten: {last_date}")

        signals = generate_signals(data)
        last_signal = signals.iloc[-1]

        st.markdown(f"### 📢 Signal: **{last_signal['signal']}**")
        st.markdown(f"""
        - Einstieg: `{last_signal['entry_price']:.2f} USD`  
        - 🎯 T1: {last_signal['T1']} ({last_signal['T1_hitrate']}%)  
        - 🎯 T2: {last_signal['T2']} ({last_signal['T2_hitrate']}%)  
        - 🎯 T3: {last_signal['T3']} ({last_signal['T3_hitrate']}%)  
        - 🎯 T4: {last_signal['T4']} ({last_signal['T4_hitrate']}%)  
        """)

        with st.expander("📊 Strategievergleich"):
            result = compare_strategies(symbol)
            st.dataframe(result)

except Exception as e:
    st.error(f"❌ Fehler beim Laden: {e}")
