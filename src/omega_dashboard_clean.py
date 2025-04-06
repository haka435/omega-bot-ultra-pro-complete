import streamlit as st
from signal_engine import get_price_data, generate_signals
from strategy_backtest import compare_strategies
import datetime

st.set_page_config(page_title="Omega Finance Dashboard", layout="wide")

st.title("📈 Omega Finance Dashboard")
st.caption("Echtzeit Day-Trading-Signale mit T1–T4, Trefferquoten und News")

# --- MARKTAUSWAHL
symbol = st.selectbox("📊 Markt auswählen:", ["BTC-USD", "GC=F", "ES=F"])

# --- DATENLADEN
try:
    data = get_price_data(symbol)
    signal_data = generate_signals(data)

    market_open = not data.empty and data.index[-1].date() == datetime.date.today()
    if market_open:
        st.success("🟢 Markt ist offen – Signale aktiv")
    else:
        st.warning("🔒 Markt ist geschlossen – letzte Daten von {}".format(data.index[-1].date()))

    # --- SIGNALANZEIGE
    if not signal_data.empty:
        sig = signal_data.iloc[-1]
        st.markdown(f"""### 💡 Signal: **{sig['signal']}**  
        ⏱️ Einstieg: `{sig['entry_price']:.2f} USD`  
        🎯 T1: {sig['T1']} ({sig['T1_hitrate']}%)  
        🎯 T2: {sig['T2']} ({sig['T2_hitrate']}%)  
        🎯 T3: {sig['T3']} ({sig['T3_hitrate']}%)  
        🎯 T4: {sig['T4']} ({sig['T4_hitrate']}%)  
        """)

    # --- STRATEGIE-VERGLEICH
    with st.expander("📊 Strategievergleich (Backtest)"):
        stats = compare_strategies(symbol=symbol)
        st.dataframe(stats)

except Exception as e:
    st.error(f"❌ Fehler beim Laden der Daten: {e}")
