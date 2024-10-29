import streamlit as st

from googleapiclient.discovery import build

from datetime import datetime, timedelta

drive_service = build('drive', 'v3', developerKey=st.secrets['GOOGLE_API_KEY'])


st.title('Teste')

st.write('Caixa de teste:')

text = st.text_input('Digite algo para ser gravado:')

results = drive_service.files().list(q="'" + '1C9NdZjedjCOXGRkMjuy9eTFSahZOYTWh' + "' in parents and mimeType != 'application/vnd.google-apps.folder'").execute()

items = results.get('files', [])

for item in items:

    st.write(item['name'])
