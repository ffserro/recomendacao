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

        st.multiselect('Escolha os militares que você recomendaria com empenho:', df.nome)




# if st.button('Vote no SO SANDRO'):
#     df.loc[df.nome=='SO SANDRO', 'a'] = df.loc[df.nome=='SO SANDRO', 'a'] + 1
#     df = conn.update(worksheet='Página1', data=df)
#     st.dataframe(df)
