'''
author : saurav.pattnaik
'''

import streamlit as st
import base64
import os
import sys
import joblib
from get_recommendations import depth_limited_search

# Set page title and icon
st.set_page_config(page_title="Gastronomy Guide", page_icon=":memo:", layout="wide")

# Add a title text with white color and center align
st.write(
    f'<h1 style="color: white; text-align: center;">Gastronomy Guide</h1>',
    unsafe_allow_html=True
)


module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


set_png_as_page_bg('data/background.jpg')

recommendation_model = joblib.load(open('model/BLR_restaurant_model.pkl','rb'))
movie_keys = list(recommendation_model.keys())
choice = st.selectbox(label="",options=movie_keys)

col1,col2 = st.columns([9,1])
recommend_button = col1.button(label='Get Recommendations')
clear_button = col2.button(label='Clear')

if recommend_button:
    recommendations = depth_limited_search(recommendation_model,choice)
    st.write(recommendations)
