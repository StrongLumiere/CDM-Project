import streamlit as st
import pandas as pd
from tab3 import display_tab3
from tab2 import display_tab2
from tab1 import display_tab1

# Streamlit 앱 제목
st.title("Streamlit 트리맵 구현 예시")


# 탭 구성
tab1, tab2, tab3 = st.tabs(["Overview", "Procedure", "Hospitalization Prediction"])

with tab1:
    display_tab1()

with tab2:
    st.markdown("### CSV 파일 업로드")
    uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요", type=["csv"], key="file_uploader_tab2")
    # uploaded_file = pd.read_csv('file.csv')
    display_tab2(uploaded_file)

   
# 탭 3: Hospitalization Prediction
with tab3:
    st.markdown("### CSV 파일 업로드")
    uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요", type=["csv"], key="file_uploader_tab3")
    # uploaded_file = pd.read_csv('file.csv')
    display_tab3(uploaded_file)
    
    
