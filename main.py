import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime as dt, timedelta as td

from io import BytesIO
import base64

if 'stage' not in st.session_state:

    st.cache_data.clear()

    file_ = open("logo.jpg", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(f"<img style='display: block; margin-left: auto; margin-right: auto; width:40%;' src='data:image/png;base64,{data_url}' alt='EAMCE' width='500'>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>CENTRAL DE DEMANDAS</h1>", unsafe_allow_html=True)
    st.session_state.conn = st.connection('gsheets', type=GSheetsConnection)

    st.write('Este é um espaço para que você possa solicitar aquisições ou ajustes, visando a melhoria do material e do funcionamento da Organização.')

    columns = st.columns([1,1,1,1,1])

    if columns[1].button('Solicitar aquisição'):
        st.session_state['stage'] = 1
        st.rerun()
    
    if columns[3].button('Registrar sugestão'):
        st.session_state['stage'] = 2
        st.rerun()
else:

    if st.session_state['stage'] == 1:

        st.session_state.df = st.session_state.conn.read(worksheet='Aquisições')

        st.html('<h1>Solicitar uma compra</h1>')

        solicitante = st.text_input('Identificação do solicitante:')
        setor = st.selectbox('Setor do solicitante:', ['', 'NPAMRC', 'NPAORE', 'NPAGUA', 'GPNSSE-01', 'GPNSSE-02', 'GPNSSE-10', 'GPNSSE-30', 'GPNSSE-40', 'GPNSSE-50', 'GPNSSE-60'])
        descricao = st.text_area('Descrição da necessidade de aquisição')
        tipo = st.selectbox('Tipo de aquisição', ['', 'Material', 'Serviço', 'Material permanente'])
        valor = st.number_input('Qual é o valor estimado desta aquisição?', format="%0.2f")

        if st.button('Enviar', disabled=(any([field=='' for field in [solicitante, setor, descricao, tipo]]) or valor==0)):
            st.session_state.stage = 3
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame(
                {'Data': [(dt.now() - td(hours=3)).strftime(format='%d/%m/%Y %H:%M')],	
                'Solicitante':[solicitante],	
                'Setor':[setor],	
                'Descrição detalhada':[descricao],	
                'Tipo':[tipo],	
                'Valor estimado':[valor]}
            )])
            st.session_state.conn.update(worksheet='Aquisições', data=st.session_state.df)
            st.rerun()

    if st.session_state.stage == 2:

        st.session_state.df = st.session_state.conn.read(worksheet='Sugestões')

        st.html('<h1>Fazer uma sugestão</h1>')

        nome = st.text_input('Digite seu nome caso queira se identificar:')
        sugestao = st.text_area('Digite a sua sugestão:')

        if st.button('Enviar', disabled=(sugestao=='')):
            st.session_state.stage = 3
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame(
                {'Data': [(dt.now() - td(hours=3)).strftime(format='%d/%m/%Y %H:%M')],	
                'Nome':[nome if nome != '' else 'Anônimo'],	
                'Sugestão':[sugestao]}
            )])
            st.session_state.conn.update(worksheet='Sugestões', data=st.session_state.df)
            st.rerun()

    if st.session_state.stage == 3:

        st.html('<h1>Muito obrigado pela sua contribuição!</h1>')

        st.write('Estamos trabalhando para fazer o Comando do Grupamento de Patrulha Naval e os meios subordinados melhores, e você é parte da solução.')
