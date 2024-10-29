import streamlit as st

from googleapiclient.discovery import build

from datetime import datetime, timedelta

drive_service = build('drive', 'v3', credentials=st.secrets['GOOGLE_API_KEY'])


st.title('Teste')

st.write('Caixa de teste:')

text = st.text_input('Digite algo para ser gravado:')

with open('./test.txt', 'a') as file:
    file.write(text)