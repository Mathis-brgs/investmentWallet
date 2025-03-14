import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen
import pandas as pd
import requests
from datetime import datetime, timedelta

dashboard_page = st.Page(
    page="views/dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True,
)

market_page = st.Page(
    page="views/market.py",
    title="Market",
    icon="🏠",
)

wallet_page = st.Page(
    page="views/wallet.py",
    title="Wallet",
    icon="🏠",
)

export_page = st.Page(
    page="views/export.py",
    title="Export",
    icon="🏠",
)

# --- Navigation setup --- #

pg = st.navigation(pages=[dashboard_page, market_page, wallet_page, export_page])
pg.run()

# --- Shared on all pages --- #
st.logo("assets/logo-removebg2.png")
st.sidebar.text("Made by Mathis BORGES, Bristhis DEGBEKO, Jerome WEIBEL")