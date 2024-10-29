import streamlit as st

from datetime import datetime, timedelta

st.title('Teste')

st.write('Caixa de teste:')

text = st.text_input('Digite algo para ser gravado:')

with open('./test.txt', 'a+') as file:
    file.write(text)