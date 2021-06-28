import streamlit as st
from pandas.api.types import is_numeric_dtype
import pandas as pd
from datetime import date
import base64
import smtplib


#import mailer

#from win10toast_click import ToastNotifier 
   

st.title("affaires ctf")
st.header("Hatem Hellal")

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
#def send(title,message):
   # notifier = ToastNotifier()

def send(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("hatemhellal5@gmail.com", "Hatouma1998*")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("hatemhellal5@gmail.com","hatemhellal5@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")




def filterdate(df,start,end):
    mask = (df["date de depart"] >= start) & (df["date d'expiration"] <= end)
    return df.loc[mask]
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("./style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
#############################
avocat=st.sidebar.text_input("avocat")
nom=st.sidebar.text_input("nom de contrat")
description=st.sidebar.text_input("description")
dateD=st.sidebar.date_input("date de depart")
dateF=st.sidebar.date_input("date d'expiration")
etat = st.sidebar.selectbox(
    'etats',('actif','suspendu','terminé'))
 
if st.sidebar.button("ajouter ligne"):
    get_data().append({"nom de contrat":nom,"avocat":avocat,"date de depart":dateD,"date d'expiration":dateF, "description": description,"état":etat})


    
    
c=0

df=pd.DataFrame(get_data()) 

if st.checkbox("remplace"):
    columns = st.selectbox("choix de  colonne", df.columns)
    old_values = st.multiselect("valeurs initiales",list(df[columns].unique()),list(df[columns].unique()))
    ligne=st.selectbox("choix de ligne",df.index)
    with st.form(key='my_form'):
        col1,col2 = st.beta_columns(2)
     
        if is_numeric_dtype(df[columns]) :
            st_input = st.number_input
        elif columns in ["date de depart","date d'expiration"]:
            st_input= st.date_input
        else :
            st_input = st.text_input
         
        with col1:
            old_val = st_input("ancien valeur")
        with col2:
            new_val = st_input("nouveau valeur")
            if st.form_submit_button("Remplacer"):
                for i in df[columns]:
                    
                    if i ==old_val:
                        
                        for j in range(len(get_data()[ligne])):
                            if columns=="nom de contrat":
                                get_data()[ligne].update({"nom de contrat":new_val})
                            elif columns=="date de depart":
                                get_data()[ligne].update({"date de depart":new_val})
                            elif columns=="date d'expiration":
                                get_data()[ligne].update({"date d'expiration":new_val})
                            elif columns=="description":
                                get_data()[ligne].update({"description":new_val})
                            else:
                                get_data()[ligne].update({"état":new_val})
if st.checkbox("filtrer"):
    with st.form(key='my_form'):
        start_date,end_date = st.beta_columns(2)
        start_date=st.text_input("entrer le premier date")
        start_date=pd.to_datetime(start_date,format='%Y-%m-%d')
        end_date=st.text_input("entrer le deuxieme date")
        end_date=pd.to_datetime(end_date,format='%Y-%m-%d')
        if st.form_submit_button("filtrer"):
           df_filter= filterdate(df,start_date,end_date)
           st.table(df_filter)
           st.markdown(get_table_download_link_csv(df_filter), unsafe_allow_html=True)
                    
                    
                        
if st.sidebar.button("notify"):
    for i in range(len(df["date d'expiration"])):
        if df["date d'expiration"][i]==date.today():
            send('important',df["description"][i])
                
        
st.dataframe(df)
st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)  


           
           
          
           
           



