import streamlit as st
import time
import numpy as np
import re
import sys

# Load filters folders
sys.path.append('./filters/PII') 
from PII_filter import PII_filter, regex_dict

examples_dict = {}
examples_dict['None'] = ''
examples_dict['Example with PII (1)'] = 'Mi número de teléfono es el 690312141'
examples_dict['Example with PII (2)'] = 'Mi mail es sdsdf@gmail.com'


st.set_page_config(
     page_title="Review validation",
     page_icon="🔮",
)

st.title('Spam review or not?')

option = st.sidebar.selectbox(
     'Examples',
     examples_dict.keys())

doc = st.text_area(
     "Paste your review below",
     value=examples_dict.get(option, ''),
     height=150,
     )

if st.button(label="✨ Validate!"):
     
     result_dict = PII_filter(doc, regex_dict)
     
     st.write(result_dict['Suspicious'])
     st.write(result_dict['Motive'])


