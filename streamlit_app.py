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

pg = st.navigation(pages=[dashboard_page, market_page, wallet_page, export_page])
pg.run()

st.title("Outil d'Analyse de Portefeuille d'Investissement")
