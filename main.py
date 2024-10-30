import streamlit as st
from streamlit_gsheets import GSheetsConnection

from datetime import datetime, timedelta

conn = st.connection('gsheets', type=GSheetsConnection)

df = conn.read()

for row in df.itertuples():
    st.write(f'{row.name} has a {row.pet}')


