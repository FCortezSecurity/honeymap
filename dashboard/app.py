import sys

sys.path.insert(0, "src")

import pandas as pd
import plotly.express as px
import streamlit as st

from honeymap.db import connect

st.set_page_config(page_title="HoneyMap", layout="wide")
st.title("🍯 HoneyMap")
st.caption("IP geolocation is an estimate, not a physical location.")

CHOICES = {
    "Live honeypot data": ["live"],
    "Demo data (synthetic)": ["demo"],
    "Both": ["live", "demo"],
}
choice = st.sidebar.radio("Data shown", list(CHOICES), index=2)
sources = CHOICES[choice]

if "demo" in sources:
    st.warning(
        "Demo data is included. These events are synthetic, generated from random IP "
        "addresses. They are not real attackers."
    )


def load(sql, params=None):
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        columns = [c.name for c in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=columns)


stats = load(
    "SELECT count(*) AS events, count(DISTINCT src_ip) AS sources, "
    "count(lat)::float / NULLIF(count(*), 0) AS coverage "
    "FROM events WHERE source = ANY(%s)",
    (sources,),
)
alerts = load(
    "SELECT first_seen, severity, rule, src_ip, service, event_count, source "
    "FROM alerts WHERE source = ANY(%s) ORDER BY first_seen DESC",
    (sources,),
)
events = load(
    "SELECT ts, src_ip, service, event_type, username, password, country, city, lat, lon, source "
    "FROM events WHERE source = ANY(%s) ORDER BY ts DESC LIMIT 2000",
    (sources,),
)
places = load(
    "SELECT country, city, lat, lon, count(*) AS events, count(DISTINCT src_ip) AS sources "
    "FROM events WHERE lat IS NOT NULL AND source = ANY(%s) "
    "GROUP BY country, city, lat, lon",
    (sources,),
)
timeline = load(
    "SELECT date_trunc('hour', ts) AS hour, service, count(*) AS events "
    "FROM events WHERE source = ANY(%s) GROUP BY 1, 2 ORDER BY 1",
    (sources,),
)

coverage = stats.loc[0, "coverage"]
coverage = 0 if pd.isna(coverage) else coverage

col1, col2, col3, col4 = st.columns(4)
col1.metric("Events", int(stats.loc[0, "events"]))
col2.metric("Sources", int(stats.loc[0, "sources"]))
col3.metric("Alerts", len(alerts))
col4.metric("Coverage", f"{coverage:.0%}", help="Share of events with a location")

st.subheader("Global activity")
if places.empty:
    st.info("No located events in this selection. Private addresses have no location.")
else:
    places["city"] = places["city"].fillna("Unknown city")
    fig = px.scatter_geo(
        places,
        lat="lat",
        lon="lon",
        size="events",
        hover_name="city",
        hover_data={"country": True, "events": True, "sources": True, "lat": False, "lon": False},
        projection="natural earth",
        size_max=35,
        template="plotly_dark",
    )
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, width="stretch")

left, right = st.columns([3, 2])
with left:
    st.subheader("Activity over time")
    if timeline.empty:
        st.info("No events in this selection.")
    else:
        st.plotly_chart(
            px.bar(timeline, x="hour", y="events", color="service", template="plotly_dark"),
            width="stretch",
        )
with right:
    st.subheader("Top countries")
    if places.empty:
        st.info("Nothing to rank yet.")
    else:
        top = (
            places.groupby("country", as_index=False)["events"].sum()
            .sort_values("events", ascending=False).head(8)
        )
        st.dataframe(top, hide_index=True)

st.subheader("Detection alerts")
st.dataframe(alerts, hide_index=True)

st.subheader("Recent events")
st.dataframe(events, hide_index=True)