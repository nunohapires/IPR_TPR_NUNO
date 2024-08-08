import pandas as pd 
import streamlit as st
import numpy as np

st.set_page_config(
    layout="wide",
    page_title="Modelos IPR x TPR"
)

st.markdown(
    '# Calcule E Plote Seu IPR x TPR .'
)

with st.expander("Informações Adicionais"):
    st.write("""
    *Este web app foi desenvolvido usando apenas python , pelo estudante de engenharia de petróleo Nuno Henrique Albuquerque Pires,
    da Universidade Federal de Alagoas.*
    """)
    st.markdown('- Esse web app foi feito para testar dados de IPR e TPR , gerando um plote gráfico .')
    st.markdown('- Esse web app foi desenvolvido com base nas equações do livro Petroleum Production Engineering Second Edition .')
    st.markdown('- Referência : Guo, Boyun, Xinghui Liu, e Xuehao Tan. Petroleum Production Engineering. 2ª ed., Gulf Professional Publishing, 2017.')
    

st.divider()
modelo = st.selectbox("## Qual modelo para curvas de IPR gostaria de usar ?",
                      ("Linear", "Vogel ", "Patton e Goland", "Fetkovich","Quadrático mássico")
)
col1 , col2 = st.columns(2)

def pegar_valores():
    col1.info('### *De acordo com o seu teste de formação:*', icon="📉")          
    Pe = col1.number_input('Qual a pressão estatica ? (Psi)')
    Pwf = col1.number_input('Qual a Pressão do teste 1 ? (Psi)')
    Qo = col1.number_input('Qual a vazão do teste 1 ? (Stb/day)')
    RAO_test = col1.selectbox("Existe Razão Agua e Oleo ?", ("Não", "Sim"))
    if RAO_test == "Não": 
        Rao = 0
    else:
        col1.write('Informe no seguinte formato : 20% = 0.2')
        Rao = col1.number_input('Qual a RAO ?')
    return Pe,Qo,Pwf,Rao

def calcular_linear(Pe,Qo,Pwf,Rao):
    Qw = Rao * Qo
    Qtotal = Qw + Qo
    Ip = (Qtotal)/(Pe - Pwf)
    variacao = [e for e in range(int(Pe + 1))]
    df = pd.DataFrame(variacao,columns=['IPR'])
    df['Q'] = Ip*(Pe - df )
    return df,Qtotal

def calcular_vogel (Pe,Qo,Pwf,Rao,Psat):
    Qw = Rao * Qo
    Qtotal = Qw + Qo
    Jl = Qtotal/(Pe - Pwf)
    jq = Qtotal/((Pe - Psat) + (Psat/1.8)*(1 - 0.2*(Pwf/Psat) - 0.8*((Pwf)/Psat)**2))
    variacao = [e for e in range(int(Pe + 1))]
    df = pd.DataFrame(variacao,columns=['IPR'])
    df['Q'] = (jq*((Pe - Psat) + (Psat/1.8)*(1 - 0.2*(df['IPR']/Psat) - (0.8*((df['IPR'])/Psat)**2))))
    return df 

def calcular_Patton_Goland (Pe,Qo,Pwf,Rao,Psat):
    Qw = Rao * Qo
    Qtotal = Qw + Qo
    Jl = Qtotal/(Pe - Pwf)
    jq = Qtotal/((Pe - Psat) + (Psat/1.8)*(1 - 0.2*(Pwf/Psat) - 0.8*((Pwf)/Psat)**2))
    variacao = [e for e in range(int(Pe + 1))]
    df = pd.DataFrame(variacao,columns=['IPR'])
    df['Q'] = np.where(df['IPR'].index <= Psat ,(jq*((Pe - Psat) + (Psat/1.8)*(1 - 0.2*(df['IPR']/Psat) - (0.8*((df['IPR'])/Psat)**2)))), Jl*(Pe - df['IPR']))
    return df

def calcular_fetkovich (Pe,Qo,Pwf,Rao,Psat,Pwf2,Qo2):
    Qw = Rao * Qo
    Qtotal = Qw + Qo
    n = (np.log(Qo/Qo2))/(np.log((Pe**2 - Pwf**2)/(Pe**2 - Pwf2**2)))
    C = Qo/(Pe**2 - Pwf2**2)**n
    variacao = [e for e in range(int(Pe + 1))]
    df = pd.DataFrame(variacao,columns=['IPR'])
    df['Q'] =  C*(Pe**2 - df['IPR']**2)**n
    return df 

def calcular_Quadrático_mássico (Pe,Qo,Pwf,Rao,Do,Dl,Dg,Rgo):
    BSW = Qo * Rao
    Qmt = ((Do + Dg*Rgo)*(1-BSW) + Dl*BSW)*Qo
    B = (Pe**2 - Pwf**2)/Qmt
    Dt = ((Do + Dg*Rgo)*(1-BSW) + Dl*BSW)
    variacao = [e for e in range(int(Pe + 1))]
    df = pd.DataFrame(variacao,columns=['IPR'])
    df['Q'] =  (Pe**2 - df['IPR']**2)/(B*Dt)
    return df 

def calcular_tpr(Qo,Rao):
        with col2 :
            st.info('### *De acordo com os dados do seu poço :*', icon="📈")
            st.write('### Considerando apenas o produção')

            L = st.number_input('Qual é o comprimento do tubo (m):')
            D = st.number_input('Qual é o diametro do primeiro tubo (in):')
            N_tubos = st.number_input('Qual é o numero de tubo :')
            Do = st.number_input('Qual é a densidade do óleo (g/m³):')
            Dw =  st.number_input('Qual é a densidade da água (g/m³):')
            Dg = st.number_input('Qual é a densidade do gás (g/m³):')
            Rgo = st.number_input('Qual é RGO :')
            Pwh = st.number_input('Qual é a pressão na cabeça do poço em psi :')

            Yo = Do/Dw
            Yw = Dw/1000
            Yg = Dg/1
            M = 350.17*(Yo + Rao*Yw) + (Rgo*Dg * Yg)
            Dvp = (1.437* (10**-5) * M * Qo )/D
            F2f = 10**(1.444 - 2.5* np.log(Dvp))
            K = (F2f * Qo**2 * M)/(7.4137* 10**10 * D*5)
            
            L_tubo = [e for e in range(int((L * N_tubos) + 1))]
            dl = pd.DataFrame(L_tubo,columns=['Tamanho'])
            dl['TPR']= Pwh + (D + (K/D))*(dl/144)
            return dl 



##############################################################################################################################
if modelo == 'Linear':
    Pe,Qo,Pwf,Rao = pegar_valores()
    dl = calcular_tpr(Qo,Rao)
    if st.button('Confirme os dados :'):
        df,Qtotal = calcular_linear(Pe,Qo,Pwf,Rao)
        df['TPR'] = dl['TPR']
        st.line_chart(df, x='Q')
        st.divider()
        st.markdown('## Aqui temos a planilha calculada !\n* Você pode interagir editar e muito mais !')
        st.data_editor(df)

elif modelo == 'Vogel ':
    Pe,Qo,Pwf,Rao = pegar_valores()
    dl = calcular_tpr(Qo,Rao)
    #pegar valores que faltam 
    Psat = col1.number_input('Qual é a pressão de saturação (Psi)?')
    if st.button('Confirme os dados :'):
        df = calcular_vogel(Pe,Qo,Pwf,Rao,Psat)
        df['TPR'] = dl['TPR']
        st.line_chart(df, x='Q')
        st.divider()
        st.markdown('## Aqui temos a planilha calculada !\n*Você pode interagir editar e muito mais !')
        st.data_editor(df)
        

elif modelo == 'Patton e Goland':
    Pe,Qo,Pwf,Rao = pegar_valores()
    #pegar valores que faltam 
    Psat = col1.number_input('Qual é a pressão de saturação (Psi)?')
    dl = calcular_tpr(Qo,Rao)
    if st.button('Confirme os dados :'):
        df = calcular_Patton_Goland(Pe,Qo,Pwf,Rao,Psat)
        df['TPR'] = dl['TPR']
        st.line_chart(df, x='Q')
        st.divider()
        st.markdown('## Aqui temos a planilha calculada !\n* Você pode interagir editar e muito mais !')
        st.data_editor(df)


elif modelo == 'Fetkovich':
    Pe,Qo,Pwf,Rao = pegar_valores()
    dl = calcular_tpr(Qo,Rao)
    #pegar valores que faltam 
    Psat = col1.number_input('Qual é a pressão de saturação (Psi)?')
    Pwf2 = col1.number_input('Qual é a pressão do teste 2 (Psi)?')
    Qo2 = col1.number_input('Qual é a vazão do teste 2 (Stb/day)?')
    
    if st.button('Confirme os dados :'):
        df = calcular_fetkovich(Pe,Qo,Pwf,Rao,Psat,Pwf2,Qo2)
        df['TPR'] = dl['TPR']
        st.line_chart(df, x='Q')
        st.divider()
        st.markdown('## Aqui temos a planilha calculada !\n* Você pode interagir editar e muito mais !')
        st.data_editor(df)


elif modelo == "Quadrático mássico":
    Pe,Qo,Pwf,Rao = pegar_valores()
    dl = calcular_tpr(Qo,Rao)
    #pegar valores que faltam 
    Psat = col1.number_input('Qual é a pressão de saturação (Psi)?')
    Do = col1.number_input('Qual é densidade do oleo (kg/m³) ?')
    Dl = col1.number_input('Qual é densidade do liguido (kg/m³)?')
    Dg = col1.number_input('Qual é densidade do gás (kg/m³)?')
    Rgo = col1.number_input('Qual é RGO ?')
    
    if st.button('Confirme os dados :'):
        df = calcular_Quadrático_mássico(Pe,Qo,Pwf,Rao,Do,Dl,Dg,Rgo)
        df['TPR'] = dl['TPR']
        st.line_chart(df, x='Q')
        st.divider()
        st.markdown('## Aqui temos a planilha calculada !\n*Você pode interagir editar e muito mais !')
        st.data_editor(df)




