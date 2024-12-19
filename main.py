import streamlit as st
from streamlit_gsheets import GSheetsConnection

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

    st.session_state.df = st.session_state.conn.read(worksheet='Página1')

    st.write('Tome um tempo para recomendar militares que tenham se destacado em suas atribuições')

    columns = st.columns([2,1,2,1,2], horizontal_alignment="center")

    if columns[1].button('Solicitar uma compra'):
        st.session_state['stage'] = 1
        st.rerun()
    
    if columns[3].button('Abrir o coração'):
        st.session_state['stage'] = 1
        st.rerun()
else:

    if st.session_state['stage'] == 1:

        st.title('Recomendados com empenho')

        st.session_state.escolhas_a = st.multiselect('Escolha até 12 militares que você recomendaria com empenho:', st.session_state.df.nome, max_selections=12)

        if st.button('Prosseguir'):
            st.session_state.stage = 2
            st.rerun()

    if st.session_state.stage == 2:
        st.title('Recomendados')
        st.session_state.escolhas_b = st.multiselect('Escolha até 12 militares que você recomendaria:', [i for i in st.session_state.df.nome if i not in st.session_state.escolhas_a], max_selections=12)

        if st.button('Prosseguir'):
            st.session_state.stage = 3
            st.session_state.escolhas_c = [i for i in st.session_state.df.nome if i not in (st.session_state.escolhas_a + st.session_state.escolhas_b)]
            st.rerun()

    if st.session_state.stage == 3:
        st.title('Confira os seus votos')
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.html('<h4>Recomendados com empenho:</h2>')
            for i in st.session_state.escolhas_a:
                st.write(i)
        with col_b:
            st.html('<h4>Recomendados:</h2>')
            for i in st.session_state.escolhas_b:
                st.write(i)
        with col_c:
            st.html('<h4>Não recomendados:</h2>')
            for i in st.session_state.escolhas_c:
                st.write(i)
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button('Quero começar de novo...'):
                st.session_state.escolhas_a = []
                st.session_state.escolhas_b = []
                st.session_state.escolhas_c = []
                st.session_state.stage = 1
                st.rerun()

        with col2:
            if st.button('Pode confirmar!'):
                st.session_state.stage = 4
                st.rerun()
    
    if st.session_state.stage == 4:
        st.title('Muito obrigado pelo sua participação!')
        st.session_state.df = st.session_state.conn.read(worksheet='Página1')
        st.session_state.df.loc[st.session_state.df.nome.isin(st.session_state.escolhas_a), 'a'] += 1
        st.session_state.df.loc[st.session_state.df.nome.isin(st.session_state.escolhas_b), 'b'] += 1
        st.session_state.df.loc[st.session_state.df.nome.isin(st.session_state.escolhas_c), 'c'] += 1
        st.session_state.conn.update(worksheet='Página1', data=st.session_state.df)
