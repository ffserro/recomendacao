import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection('gsheets', type=GSheetsConnection)

df = conn.read(worksheet='Página1')

if 'stage' not in st.session_state:

    st.title('Página Inicial')

    if st.button('Começar'):

        st.session_state['stage'] = 1

        st.rerun()

else:

    if st.session_state['stage'] == 1:

        st.title('Recomendados com empenho')

        st.session_state.escolhas_a = st.multiselect('Escolha até 12 militares que você recomendaria com empenho:', df.nome, max_selections=12)

        st.write(st.session_state.escolhas_a)

        if st.button('Prosseguir'):
            st.session_state.stage = 2
            st.rerun()

    if st.session_state.stage == 2:
        st.title('Recomendados')
        st.session_state.escolhas_b = st.multiselect('Escolha até 12 militares que você recomendaria:', [i for i in df.nome if i not in st.session_state.escolhas_a], max_selections=12)
        st.write(st.session_state.escolhas_b)

        if st.button('Prosseguir'):
            st.session_state.stage = 3
            st.session_state.escolhas_c = [i for i in df.nome if i not in (st.session_state.escolhas_a + st.session_state.escolhas_b)]
            st.rerun()
    
    if st.session_state.stage == 3:
        st.title('Muito obrigado pelo sua participação!')
        df.loc[df.nome.isin(st.session_state.escolhas_a), 'a'] += 1
        df.loc[df.nome.isin(st.session_state.escolhas_b), 'b'] += 1
        df.loc[df.nome.isin(st.session_state.escolhas_c), 'c'] += 1
        df = conn.update(worksheet='Página1', data=df)
