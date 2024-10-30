import streamlit as st
from streamlit_gsheets import GSheetsConnection

from datetime import datetime, timedelta

conn = st.connection('gsheets', type=GSheetsConnection)

df = conn.read(worksheet='Página1')

if st.button('Vote no SO SANDRO'):
    df.loc[df.nome=='SO SANDRO', 'a'] += 1
    conn.update(worksheet='Página1', data=df)
    st.rerun()
