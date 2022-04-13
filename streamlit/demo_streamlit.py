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
     
     if result_dict['Suspicious']:
          st.error(f'💢 THE REVIEW IS SUSPICIOUS! \n  We think this review includes one of this options: {result_dict["Motive"]}')
          
     else:
          st.success('✔️ THE REVIEW IS VALID! \n  Nothing to see here.')
     
     st.subheader('SageMaker endpoint response', anchor=None)
     
     doc = st.text_area('',
     value=result_dict,
     height=50,
     )
     
st.write ('Still under development')


