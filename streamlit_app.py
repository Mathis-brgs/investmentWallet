import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen

st.title("Outil d'Analyse de Portefeuille d'Investissement")
st.header("Main Dashboard")

# Définition des crypto
cryptos = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Ripple": "XRP-USD",
    "Bitcoin Cash": "BCH-USD",
    "Solana": "SOL-USD"
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

start_date, end_date = "2025-02-01", "2025-02-19"
crypto_data = {name: download_crypto_data(symbol, start_date, end_date) for name, symbol in cryptos.items()}

# Affichage des données Bitcoin
st.subheader("Bitcoin ($)")
btc_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'
st.image(Image.open(urlopen(btc_img_url)))

if crypto_data["Bitcoin"] is not None:
    st.table(crypto_data["Bitcoin"])
    st.line_chart(crypto_data["Bitcoin"]["Close"])
else:
    st.warning("Impossible d'afficher les données Bitcoin.")

# Affichage des données Ethereum
st.subheader("Ethereum ($)")
eth_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png'
st.image(Image.open(urlopen(eth_img_url)))

if crypto_data["Ethereum"] is not None:
    st.table(crypto_data["Ethereum"])
    st.line_chart(crypto_data["Ethereum"]["Close"])
else:
    st.warning("Impossible d'afficher les données Ethereum.")

# Affichage des données Solana
st.subheader("Solana ($)")
sol_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png'
st.image(Image.open(urlopen(sol_img_url)))

if crypto_data["Solana"] is not None:
    st.table(crypto_data["Solana"])
    st.line_chart(crypto_data["Solana"]["Close"])
else:
    st.warning("Impossible d'afficher les données Solana.")
