import streamlit as st
from streamlit_gsheets import GSheetsConnection

from datetime import datetime, timedelta

conn = st.connection('gsheets', type=GSheetsConnection)

df = conn.read()

st.write(df)
