import streamlit as st

from googleapiclient.discovery import build
from google.oauth2 import service_account

from datetime import datetime, timedelta

creds = service_account.Credentials.from_service_account_info(
    {'key':st.secrets['GOOGLE_API_KEY']},
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=creds)


st.title('Teste')

st.write('Caixa de teste:')

text = st.text_input('Digite algo para ser gravado:')

with open('./test.txt', 'a') as file:
    file.write(text)