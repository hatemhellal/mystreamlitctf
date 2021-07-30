import streamlit as st
from pandas.api.types import is_numeric_dtype
import pandas as pd
from datetime import date
import base64
import smtplib


#import mailer

#from win10toast_click import ToastNotifier 
   



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
        server = smtplib.SMTP('smtp-mail.outlook.com',587)
        server.ehlo()
        server.starttls()
        server.login("faten_hellal@hotmail.fr", "neneoichietina00")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("faten_hellal@hotmail.fr", "hatemhellal5@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")




def filterdate(df):
    mask =( df["الحالات"] == "منتهي")
    return df.loc[mask]
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


#############################
def app():
    local_css("./style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    st.title("قضايا ctf")
    st.header("حاتم هلال")
    avocat=st.sidebar.text_input("المستشار القانوني")
    partie=st.sidebar.text_input("الاطراف")
    nomT=st.sidebar.text_input("المحكمة المختصة")
    description=st.sidebar.text_input("الاجراءات المتخذة")
    dateD=st.sidebar.date_input("تاريخ النزاع")
    dateF=st.sidebar.date_input("تاريخ التذكير")
    etat = st.sidebar.selectbox(    'الحالات',('جاري','منتهي'))     
 
    if st.sidebar.button("اضافة سطر"):
        get_data().append({"الاطراف":partie,"المحكمة المختصة":nomT,"المستشار القانوني":avocat,"تاريخ النزاع":dateD,"تاريخ التذكير":dateF, "الاجراءات المتخذة": description,'الحالات':etat})


    
    


    df=pd.DataFrame(get_data()) 

    if st.checkbox("تغيير"):
        columns = st.selectbox("اختيار ", df.columns)
        old_values = st.multiselect("valeurs initiales",list(df[columns].unique()),list(df[columns].unique()))
        ligne=st.selectbox("اختيار",df.index)
        with st.form(key='my_form'):
            col1,col2 = st.beta_columns(2)
     
            if is_numeric_dtype(df[columns]) :
                st_input = st.number_input
            elif columns in ["تاريخ النزاع","تاريخ التذكير"]:
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
                            if columns=="المستشار القانوني":
                                get_data()[ligne].update({"المستشار القانوني":new_val})
                            elif columns=="تاريخ النزاع":
                                get_data()[ligne].update({"تاريخ النزاع":new_val})
                            elif columns=="الاطراف":
                                get_data()[ligne].update({"الاطراف":new_val})
                            elif columns=="المحكمة المختصة":
                                get_data()[ligne].update({"المحكمة المختصة":new_val})
                            elif columns=="تاريخ التذكير":
                                get_data()[ligne].update({"تاريخ التذكير":new_val})
                            elif columns=="الاجراءات المتخذة":
                                get_data()[ligne].update({"الاجراءات المتخذة":new_val})
                            else:
                                get_data()[ligne].update({"الحالات":new_val})
    if st.checkbox("تنقية"):
        with st.form(key='my_form'):
            if st.form_submit_button("تنقية"):
                df_filter= filterdate(df)
                st.table(df_filter)
                st.markdown(get_table_download_link_csv(df_filter), unsafe_allow_html=True)
                    
                    
                        
    if st.sidebar.button("بعث"):
        for i in range(len(df["تاريخ التذكير"])):
            if df["تاريخ التذكير"][i]==date.today():
                send('important',df["الاجراءات المتخذة"][i])
                
        
    st.dataframe(df)
    st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)  


           
           
          
           
           


