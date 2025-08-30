# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# import your existing modules (names exactly as you provided)
from weather_API import get_current_weather
from forecast_model import get_weather_forecast
from weather_db import (
    insert_weather,
    get_latest_weather,
    get_weather_history,
    update_weather,
    delete_weather,
)

# --------------------------
# Helper utilities
# --------------------------
def weather_emoji(description: str) -> str:
    """Return a small emoji depending on the description text."""
    d = description.lower()
    if "cloud" in d or "overcast" in d:
        return "☁️"
    if "rain" in d or "shower" in d:
        return "🌧️"
    if "snow" in d:
        return "❄️"
    if "storm" in d or "thunder" in d:
        return "⛈️"
    if "clear" in d or "sun" in d:
        return "☀️"
    if "mist" in d or "fog" in d:
        return "🌫️"
    return "🌤️"

def history_to_df(history: list) -> pd.DataFrame:
    """Convert list[dict] returned by get_weather_history into a pandas DataFrame."""
    if not history:
        return pd.DataFrame(
            columns=["id", "city", "temperature_celsius", "humidity", "condition", "timestamp"]
        )
    df = pd.DataFrame(history)
    # Ensure timestamp is datetime for plotting and sorting
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        # provide a display-friendly date column
        df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        df["date"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return df

# --------------------------
# Streamlit page setup
# --------------------------
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("🌤️ Weather Dashboard")

# --------------------------
# Sidebar - user actions
# --------------------------
st.sidebar.header("➕ Add / Get Weather")
city_input = st.sidebar.text_input("Enter city name (e.g. Cairo)")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Get Current Weather"):
        if not city_input.strip():
            st.sidebar.warning("Please enter a valid city name.")
        else:
            # fetch current weather from your API function
            current = get_current_weather(city_input.strip())
            if current and "city" in current:
                # insert into DB using your insert_weather schema
                # note: your get_current_weather returns keys:
                # "city", "temperature_celsius", "humidity", "condition"
                insert_weather(
                    current["city"],
                    current["temperature_celsius"],
                    int(current["humidity"]),
                    current["condition"],
                )
                st.sidebar.success(f"✅ Saved current weather for {current['city']}")
            else:
                st.sidebar.error("⚠️ City not found or API error.")

with col2:
    if st.button("Get Forecast (5d)"):
        if not city_input.strip():
            st.sidebar.warning("Please enter a valid city name to fetch forecast.")
        else:
            # we will display forecast in the main area below when available
            st.session_state["forecast_city"] = city_input.strip()

# Quick helper to choose city from history (if any)
st.sidebar.markdown("---")
st.sidebar.header("🔎 Show History for City")
city_for_history = st.sidebar.text_input("City for history", key="hist_city")
if st.sidebar.button("Load History"):
    st.session_state["history_city"] = city_for_history.strip()

# --------------------------
# Main area: Latest + History + Forecast
# --------------------------
st.subheader("📌 Latest Saved Weather (by selected city)")

# prefer city_for_history -> session history_city -> sidebar input -> fallback None
city_to_show = (
    st.session_state.get("history_city")
    or city_for_history.strip()
    or city_input.strip()
)

if city_to_show:
    latest = get_latest_weather(city_to_show)
    if latest:
        # latest is a dict with keys id, city, temperature_celsius, humidity, condition, timestamp
        emoji = weather_emoji(latest["condition"])
        st.metric(
            label=f"{latest['city']} — {pd.to_datetime(latest['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}",
            value=f"{latest['temperature_celsius']} °C {emoji}",
            delta=f"Humidity: {latest['humidity']}% | {latest['condition']}",
        )
    else:
        st.info("No saved records for this city yet. Click 'Get Current Weather' to save one.")
else:
    st.info("Enter a city in the sidebar, then press 'Get Current Weather' or load history.")

# --------------------------
# Weather History table & charts
# --------------------------
st.subheader("📊 Weather History")

if city_to_show:
    raw_history = get_weather_history(city_to_show, limit=500)
    df_history = history_to_df(raw_history)
else:
    # if no city specified, show empty df
    df_history = history_to_df([])

if df_history.empty:
    st.write("No historical data to show.")
else:
    # show the table
    st.dataframe(df_history[["id", "city", "date", "temperature_celsius", "humidity", "condition"]], use_container_width=True)

    # charts: temperature & humidity over time
    chart_df = df_history.set_index("timestamp").sort_index()
    if not chart_df.empty:
        st.subheader("📈 Temperature & Humidity Over Time")
        st.line_chart(chart_df[["temperature_celsius", "humidity"]])

    # Update & Delete UI for records
    st.subheader("✏️ Update a record")
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        upd_id = st.number_input("Record ID", min_value=int(chart_df["id"].min()), max_value=int(chart_df["id"].max()), step=1) if not chart_df.empty else st.number_input("Record ID", min_value=1, step=1)
    with cols[1]:
        upd_temp = st.number_input("New Temperature (°C)", value=0.0, format="%.2f")
    with cols[2]:
        upd_hum = st.number_input("New Humidity (%)", value=0)
    with cols[3]:
        upd_cond = st.text_input("New Condition")
    with cols[4]:
        if st.button("Update Record"):
            success = update_weather(
                int(upd_id),
                temperature_celsius=float(upd_temp),
                humidity=int(upd_hum),
                condition=upd_cond if upd_cond.strip() else None,
            )
            if success:
                st.success(f"Record {upd_id} updated.")
            else:
                st.error("Update failed (check ID).")

    st.subheader("🗑️ Delete a record")
    del_id = st.number_input("Record ID to delete", min_value=1, step=1, key="del_id")
    if st.button("Delete Record"):
        ok = delete_weather(int(del_id))
        if ok:
            st.success(f"Record {del_id} deleted.")
        else:
            st.error("Delete failed (check ID).")

# --------------------------
# Forecast display
# --------------------------
forecast_city = st.session_state.get("forecast_city")
if forecast_city:
    st.subheader(f"🔮 5-day Forecast — {forecast_city}")
    fc = get_weather_forecast(forecast_city)
    if fc and "forecasts" in fc:
        # convert list of forecasts into DataFrame
        df_fc = pd.DataFrame(fc["forecasts"])
        # ensure datetime column is parsed
        df_fc["datetime"] = pd.to_datetime(df_fc["datetime"])
        df_fc["date_only"] = df_fc["datetime"].dt.strftime("%Y-%m-%d %H:%M")
        # show table and chart
        st.dataframe(df_fc[["date_only", "temperature_celsius", "humidity", "condition"]], use_container_width=True)
        # chart (temperature)
        st.subheader("Forecast Temperature (next points)")
        st.line_chart(df_fc.set_index("datetime")[["temperature_celsius", "humidity"]])
    else:
        st.info("Forecast not available or API error.")

# --------------------------
# Footer / Info
# --------------------------
st.markdown("---")
st.markdown("Made with ❤️ — shows current weather saved to a local SQLite DB. Use the sidebar to request weather or load history.")
