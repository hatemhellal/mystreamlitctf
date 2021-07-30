# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:18:23 2021

@author: hatem
"""

import streamlit as st
from pandas.api.types import is_numeric_dtype
import pandas as pd
import base64


@st.cache(allow_output_mutation=True)
def get_data():
    
    return []





def get_table_download_link_csv(df):
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="affaires.csv" target="_blank">Download csv file</a>'
    return href

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)



#############################
def app():
    
    local_css("./style1.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    st.title("عقود ctf")
    st.header("حاتم هلال")
    prix=st.sidebar.text_input("سعر")
    penaltie=st.sidebar.text_input("الخطية")
    garantie=st.sidebar.text_input("الضمانات")
    description=st.sidebar.text_input("المواصفات")
    dateD=st.sidebar.date_input("اجال")
    excution=st.sidebar.text_input("تنفيذ")
    etat = st.sidebar.selectbox(    'الحالات',('جاري','منتهي')) 
 
    if st.sidebar.button("اضافة سطر"):
        get_data().append({"سعر":prix,"الخطية":penaltie,"الضمانات":garantie,"اجال":dateD,"المواصفات":description,"تنفيذ":excution, "الحالات" :etat})



    df=pd.DataFrame(get_data()) 

    if st.checkbox("تغيير"):
        columns = st.selectbox("اختيار ", df.columns)
        old_values = st.multiselect("valeurs initiales",list(df[columns].unique()),list(df[columns].unique()))
        ligne=st.selectbox("اختيار",df.index)
        with st.form(key='my_form'):
            col1,col2 = st.beta_columns(2)
     
            if is_numeric_dtype(df[columns]) :
                st_input = st.number_input
            elif columns == "اجال" :
                st_input= st.date_input
            else :
                st_input = st.text_input
         
            with col1:
                old_val = st_input("القديم")
            with col2:
                new_val = st_input("الجديد")
            if st.form_submit_button("تعديل"):
                for i in df[columns]:
                    
                    if i ==old_val:
                        
                        for j in range(len(get_data()[ligne])):
                            if columns=="يعر":
                                get_data()[ligne].update({"سعر":new_val})
                            elif columns=="اجال":
                                get_data()[ligne].update({"اجال":new_val})
                            elif columns=="الخطية":
                                get_data()[ligne].update({"الخطية":new_val})
                            elif columns=="االضمانات":
                                get_data()[ligne].update({"الضمانات":new_val})
                            elif columns=="المواصفات":
                                get_data()[ligne].update({"المواصفات":new_val})
                            elif columns=="تنفيذ":
                                get_data()[ligne].update({"تنفيذ":new_val})
                            else:
                                get_data()[ligne].update({"الحالات":new_val})
                                
                                
                                
                                
    st.dataframe(df)
    st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)  
