import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen

st.title("Outil d'Analyse de Portefeuille d'Investissement")
st.header("Main Dashboard")

# Définition des symboles crypto
cryptos = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Ripple": "XRP-USD",
    "Bitcoin Cash": "BCH-USD"
}

@st.cache_data
def get_crypto_history(symbol):
    """Récupère l'historique des prix d'une crypto en cache"""
    try:
        crypto_data = yf.Ticker(symbol)
        return crypto_data.history(period="max")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données pour {symbol}: {e}")
        return None

# Récupération des historiques en cache permet de limiter les requetes.
historical_data = {name: get_crypto_history(symbol) for name, symbol in cryptos.items()}

# Téléchargement des données sur une période donnée
@st.cache_data
def download_crypto_data(symbol, start, end):
    """Télécharge les données d'une crypto pour une période donnée."""
    try:
        return yf.download(symbol, start=start, end=end)
    except Exception as e:
        st.error(f"Erreur lors du téléchargement des données pour {symbol}: {e}")
        return None

start_date, end_date = "2025-02-01", "2025-02-10"
crypto_data = {name: download_crypto_data(symbol, start_date, end_date) for name, symbol in cryptos.items()}

# Affichage des données Bitcoin
st.subheader("Bitcoin ($)")
btc_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'
st.image(Image.open(urlopen(btc_img_url)))

if crypto_data["Bitcoin"] is not None:
    st.table(crypto_data["Bitcoin"])
else:
    st.warning("Impossible d'afficher les données Bitcoin.")

