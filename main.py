import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime as dt

from io import BytesIO
import base64

if 'stage' not in st.session_state:

    st.cache_data.clear()

    file_ = open("logo.png", "rb")
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
    
    if columns[3].button('Abrir o coração'):
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
                {'Data': [dt.now().strftime(format='%d/%m/%Y %H:%M')],	
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
                {'Data': [dt.now().strftime(format='%d/%m/%Y %H:%M')],	
                'Nome':[nome if nome != '' else 'Anônimo'],	
                'Sugestão':[sugestao]}
            )])
            st.session_state.conn.update(worksheet='Sugestões', data=st.session_state.df)
            st.rerun()

    if st.session_state.stage == 3:

        st.html('<h1>Muito obrigado pela sua contribuição!</h1>')

        st.write('Estamos trabalhando para fazer um grupamento melhor, e você é parte da solução.')


    #     with col_a:
    #         st.html('<h4>Recomendados com empenho:</h2>')
    #         for i in st.session_state.escolhas_a:
    #             st.write(i)
    #     with col_b:
    #         st.html('<h4>Recomendados:</h2>')
    #         for i in st.session_state.escolhas_b:
    #             st.write(i)
    #     with col_c:
    #         st.html('<h4>Não recomendados:</h2>')
    #         for i in st.session_state.escolhas_c:
    #             st.write(i)
        
    #     col1, col2 = st.columns(2)

    #     with col1:
    #         if st.button('Quero começar de novo...'):
    #             st.session_state.escolhas_a = []
    #             st.session_state.escolhas_b = []
    #             st.session_state.escolhas_c = []
    #             st.session_state.stage = 1
    #             st.rerun()

    #     with col2:
    #         if st.button('Pode confirmar!'):
    #             st.session_state.stage = 4
    #             st.rerun()
    
    if st.session_state.stage == 4:
        st.title('Muito obrigado pelo sua participação!')
        st.session_state.df = st.session_state.conn.read(worksheet='Página1')
        st.session_state.df.loc[st.session_state.df.nome.isin(st.session_state.escolhas_a), 'a'] += 1
        st.session_state.df.loc[st.session_state.df.nome.isin(st.session_state.escolhas_b), 'b'] += 1
        st.session_state.df.loc[st.session_state.df.nome.isin(st.session_state.escolhas_c), 'c'] += 1
        st.session_state.conn.update(worksheet='Página1', data=st.session_state.df)
