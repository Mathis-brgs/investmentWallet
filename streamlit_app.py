import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen
import pandas as pd
import requests
from datetime import datetime, timedelta
from views.dashboard import show_dashboard
from views.login import show_login_page


# Initialisation de l'état de session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Configuration de la page
st.set_page_config(
    page_title="Investment Wallet",
    page_icon="💰",
    layout="wide"
)

# --- Shared on all pages --- #
st.sidebar.image("assets/logo-removebg2.png")
st.sidebar.text("AlphaTrack")
st.sidebar.text("Made by Mathis BORGES, Bristhis DEGBEKO, Jerome WEIBEL")

# Vérification de la connexion et affichage des pages
if not st.session_state.get('logged_in', False):
    show_login_page()
else:
    # Menu de navigation pour utilisateur connecté
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Market", "Wallet", "Export", "Tableau donnée"]
    )
    
    if menu == "Dashboard":
        show_dashboard()
    elif menu == "Market":
        from views.market import show_market
        show_market()
    elif menu == "Wallet":
        from views.wallet import show_wallet
        show_wallet()
    elif menu == "Export":
        from views.export import show_export
        show_export()
    elif menu == "Formulaire data":
        from views.dataEntry import show_data
        show_data()