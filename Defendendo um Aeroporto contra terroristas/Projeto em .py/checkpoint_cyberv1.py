# -*- coding: utf-8 -*-
"""CheckPoint_CyberV1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/felps2003/checkPoint_Cyber/blob/main/CheckPoint_CyberV1.ipynb
"""

!pip install -q pyngrok
!pip install -q streamlit
!pip install -q streamlit_ace

import json
from pyngrok import ngrok

!streamlit run app.py &>/dev/null&

# Commented out IPython magic to ensure Python compatibility.
 %%writefile app.py
 import streamlit as st
 import re
 import requests
 def main():
     html_temp = """ <div style ="background-color:red;padding:13px">
                       <h1 style = "color:white;text-align:center;">Verificador Imigração</h1>
                       <h6 style = "color:black;text-align:center;">Por favor digite as 3 letras do pais e o numero do passaporte"</h6>
                     </div>
                 """

     st.markdown(html_temp, unsafe_allow_html = True)

     numPassaporte = st.text_input('Passaporte')


     if st.button("Verificar"):
       res = requests.get('https://felps2003.github.io/irq.json')
       res = requests.get('https://henricobela.github.io/fra.json')
       match = re.search('(?i)(\D{3})', numPassaporte.lower())
       api = str(match[0])
       paises = ['irq','fra']
       if api in paises:
         x = str(api)
         dict_api = res.json()[x]
         for item in dict_api:
           for value in item.values():
             if str(numPassaporte) == str(x)+str(value):

               st.error('Não pode entrar no país')
           st.success('Pode entrar no país')

      else:
        st.warning("Esse pais não consta na base de dados")

 if __name__=='__main__':
     main()

!streamlit run app.py & npx localtunnel --port 8501