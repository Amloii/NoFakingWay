import streamlit as st
import sys
import json
import uuid
import os
import pandas as pd

# Load filters folders
filters_dir = os.path.join(os.path.dirname( __file__ ), '..', 'src' )
sys.path.append(filters_dir) 

from Ensemble.Ensemble_filter import EnsembleModel

#Load language model (if was not already loaded)
filter_object = EnsembleModel()

examples_dict = {}
examples_dict['None'] = ''
examples_dict['Valid review'] = 'La comida estaba muy buena'
examples_dict['Non Sense Text'] = 'iweoefivhe edfgiowe ieini efwef'
examples_dict['Personal Info'] = 'Mi numero de telefono es el 690312141 y mi email es sadfa@gmail.com'
examples_dict['URL'] = 'Si quieres comer de verdad, ven a https://www.vips.es/'
examples_dict['Offensive'] = 'El camarero es un gilipollas y ojalá se muera'


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
     

     prediction = filter_object.predict(input_dict)
     
     
     if prediction['suspicious']:
          st.error(f'💢 THE REVIEW IS SUSPICIOUS! \n  We think this review includes {prediction["filter_failed"]} ( Motive: {prediction["motive"]})')
          
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
     
          json_object_output = json.dumps(prediction, indent = 4) 
          
          doc2 = st.text_area('',
          value=json_object_output,
          height=300,
          )
     
st.write ('Still under development')

st.subheader('Documentation', anchor=None)

data = {
     'URL': 'https://nextchance.atlassian.net/wiki/spaces/CHAR/pages/1979547649/Data+CHAR-2295+Analyze+solutions+for+URL+detection',
     'Personal Info': 'https://nextchance.atlassian.net/wiki/spaces/CHAR/pages/1975648261/Data+CHAR-2184+Analyze+solutions+for+Personal+Information+Filter',
     'Filler': 'https://nextchance.atlassian.net/wiki/spaces/CHAR/pages/1976467458/Data+CHAR-2213+Analyze+solutions+for+Filler+Reviews+Filter',
     'Offensive': 'https://nextchance.atlassian.net/wiki/spaces/CHAR/pages/1976893441/Data+CHAR-2212+Analyze+solutions+for+Ofensive+Reviews+Filter'}
df = pd.DataFrame.from_dict(data, orient='index')
df.columns = ['Confluence Info']

st.dataframe(df) 