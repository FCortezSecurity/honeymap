import sys

sys.path.insert(0, "src")

import pandas as pd
import streamlit as st

from honeymap.db import connect

st.set_page_config(page_title="HoneyMap", layout="wide")
st.title("🍯 HoneyMap")


def load(sql):
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql)
        columns = [c.name for c in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=columns)


events = load(
    "SELECT ts, src_ip, service, event_type, username, password "
    "FROM events ORDER BY ts DESC LIMIT 1000"
)
alerts = load(
    "SELECT first_seen, severity, rule, src_ip, service, event_count "
    "FROM alerts ORDER BY first_seen DESC"
)

col1, col2, col3 = st.columns(3)
col1.metric("Events", len(events))
col2.metric("Sources", events["src_ip"].nunique())
col3.metric("Alerts", len(alerts))

st.subheader("Detection alerts")
st.dataframe(alerts, hide_index=True)

st.subheader("Recent events")
st.dataframe(events, hide_index=True)