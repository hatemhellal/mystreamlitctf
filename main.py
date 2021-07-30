# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:18:24 2021

@author: hatem
"""

import aff
import cont
import streamlit as st
from SessionState import get

session_state = get(password='')

if session_state.password != 'hatem':
    pwd_placeholder = st.sidebar.empty()
    pwd = pwd_placeholder.text_input("Password:", value="", type="password")
    session_state.password = pwd
    if session_state.password == 'hatem':
        pwd_placeholder.empty()
        PAGES = {"قضايا": aff,"عقود": cont }
        st.sidebar.title('Navigation')
        selection = st.sidebar.radio("Go to", list(PAGES.keys()))
        page = PAGES[selection]
        page.app()
    else:
        st.error("the password you entered is incorrect")
else:
        PAGES = {"قضايا": aff,"عقود": cont }
        st.sidebar.title('Navigation')
        selection = st.sidebar.radio("Go to", list(PAGES.keys()))
        page = PAGES[selection]
        page.app()



