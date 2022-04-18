import streamlit as st
import sys
import json
import uuid
import subprocess

# Load filters folders
sys.path.append('./filters/PII') 
from PII_filter import PII_filter, regex_dict

sys.path.append('./filters/Language') 
from Lang_filter import Lang_filter, create_language_detection_model

#Load language model (if was not already loaded)
language_detection_model = create_language_detection_model()

examples_dict = {}
examples_dict['None'] = ''
examples_dict['Valid review'] = 'La comida estaba muy buena'
examples_dict['Example with PI (1)'] = 'Mi numero de telefono es el 690312141'
examples_dict['Example with PI (2)'] = 'Mi mail es sdsdf@gmail.com'

st.set_page_config(
     page_title="Review validation",
     page_icon="🔮",
)

st.title('🔮 Valid review or not?')

option = st.sidebar.selectbox(
     'Examples',
     examples_dict.keys())

doc = st.text_area(
     "Paste your review below",
     value=examples_dict.get(option, ''),
     height=150,
     )

if st.button(label="✨ Validate!"):
     
     # Create a mock input
     input_dict = {}
     input_dict['product_id'] = str(uuid.uuid4())
     input_dict['user_id'] = str(uuid.uuid4())
     input_dict['review'] = doc
     input_dict['value'] = 5
     
     result_dict = Lang_filter(language_detection_model, input_dict['review'])
     if not result_dict['suspicious']:
          result_dict = PII_filter(input_dict['review'], regex_dict)
     
     if result_dict['suspicious']:
          st.error(f'💢 THE REVIEW IS SUSPICIOUS! \n  We think this review includes {result_dict["filter_failed"]} ( Candidates: {result_dict["motive"]})')
          
     else:
          st.success('✔️ THE REVIEW IS VALID! \n  Nothing to see here.')
          
     col1, col2 = st.columns(2)

     with col1:
          st.subheader('SageMaker endpoint input (mock)', anchor=None)
          
          json_object_input = json.dumps(input_dict, indent = 4) 
          
          doc_input = st.text_area('',
          value=json_object_input,
          height=300,
          )
          

     with col2:
          st.subheader('SageMaker endpoint response', anchor=None)
     
          json_object_output = json.dumps(result_dict, indent = 4) 
          
          doc2 = st.text_area('',
          value=json_object_output,
          height=300,
          )
     
st.write ('Still under development')


