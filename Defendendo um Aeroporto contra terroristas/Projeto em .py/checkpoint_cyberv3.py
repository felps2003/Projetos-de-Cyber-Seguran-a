# -*- coding: utf-8 -*-
"""CheckPoint_CyberV3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/felps2003/checkPoint_Cyber/blob/main/CheckPoint_CyberV3.ipynb
"""

!pip install -q pyngrok

!pip install -q streamlit

!pip install -q streamlit_ace

!pip install fuzzywuzzy[speedup]

!streamlit run app.py &>/dev/null&

from pyngrok import ngrok

from fuzzywuzzy import process

# Commented out IPython magic to ensure Python compatibility.
%%writefile app.py
import streamlit as st
import re
import json
import requests as req
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from pyngrok import ngrok
 
 
 res = requests.get('https://henricobela.github.io/fra.json')
 nomes = req.get('https://cspinheiro.github.io/interpol.json')
   
 def main():
 
   html_temp = """ 
   <div style ="background-color:red;padding:13px"> 
   <h1 style ="color:black;text-align:center;">Imigração para o Iraque</h1> 
   <h6 style ="color:white;text-align:center;">Por favor digite as três letra de identificação do pais</h6>
   <h6 style ="color:white;text-align:center;">e os numeros do passaporte</h6>
   </div> 
   """      
   st.markdown(html_temp, unsafe_allow_html = True) 
   names = st.text_input('Nome do imigrante')
   numPassaporte = st.text_input('Passaporte')
   
   def verificarNome(names):
     InterpolList = req.get('https://cspinheiro.github.io/interpol.json')
     lista_fuzzy = process.extract(names, InterpolList)
     resultado = []
     for sublista in lista_fuzzy: 
         if sublista[1] > 80:
           resultado.append(sublista)
     if len(resultado) == 0:
         return True
     return False
 
   res = req.get('https://felps2003.github.io/irq.json')
   paises = ['irq','fra']
   def verificacaoPassaporte(numPassaporte):
     match = re.search('(?i)(\D{3})', numPassaporte.lower())
     api = (match[0])
     if api in paises:
       x = (api)
       dict_api = res.json()[x]
       for item in dict_api:
           for value in item.values():
             if str(numPassaporte) == str(x)+str(value):
               return False
       return True
 
       
   def verificacao(names,numPassaporte):
     imigrante = verificarNome(names)
     passaporte = verificacaoPassaporte(numPassaporte)
     if passaporte == False or imigrante == False:
       st.error('Prenda o individuo, possivel terrorista')
     elif passaporte == True and imigrante == True:
       st.success('Imigração permitida')
           
   if st.button("Verificar"):
     verificacao(names,numPassaporte)
 
 if __name__=='__main__': 
     main()

!streamlit run app.py & npx localtunnel --port 8501