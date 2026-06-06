from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ApartmentOps IT Ops Hub", layout="wide")

DATA_FILE = Path("data/requests.csv")

st.title("ApartmentOps IT Ops Hub")
st.caption("Incident tickets, AI summaries, assets, and KB guidance.")

if not DATA_FILE.exists():
    st.warning("No requests.csv found yet. Run the alert bridge or use sample data.")
    st.stop()

df = pd.read_csv(DATA_FILE)

st.metric("Total Tickets", len(df))

if "status" in df.columns:
    open_count = len(df[df["status"].astype(str).str.lower() == "open"])
    st.metric("Open Tickets", open_count)

st.subheader("Incidents")
st.dataframe(df, use_container_width=True)
