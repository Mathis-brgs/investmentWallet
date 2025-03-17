import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen
import pandas as pd
import requests
from datetime import datetime, timedelta
from views.login import show_login_page

# initialiser l'état de connexion
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def show_dashboard():

    #Bouton de connexion
    with st.sidebar:
        if not st.session_state.get('logged_in', False):
            if st.button("Se connecter"):
                show_login_page()
                return
        else:
            if st.button("Se déconnecter"):
                st.session_state.logged_in = False
                st.rerun()

    # vérifier si l'utilisateur est connecté
    if not st.session_state.get('logged_in', False):
        show_login_page()
        return

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

    # récupération des historiques en cache permet de limiter les requetes.
    historical_data = {name: get_crypto_history(symbol) for name, symbol in cryptos.items()}

    # téléchargement des données sur une période donnée
    @st.cache_data
    def download_crypto_data(symbol, start, end):
        """Télécharge les données d'une crypto pour une période donnée."""
        try:
            return yf.download(symbol, start=start, end=end)
        except Exception as e:
            st.error(f"Erreur lors du téléchargement des données pour {symbol}: {e}")
            return None

    #recuperer les tendances du marchés
    @st.cache_data
    def get_top_trending_cryptos():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            df = pd.DataFrame(data)
            
            # trier par la plus forte hausse en pourcentage sur 24h
            df = df.sort_values(by="price_change_percentage_24h", ascending=False)
            
            # sélectionner les 5 cryptos les plus performantes
            top_5 = df.head(5)[["name", "symbol", "image", "current_price", "price_change_percentage_24h"]]
            
            return top_5
        except Exception as e:
            st.error(f"Erreur lors de la récupération des tendances : {e}")
            return pd.DataFrame()

    #top5    
    st.header("Top 5 tendances du marchés (24H)")
    top_cryptos = get_top_trending_cryptos()

    if not top_cryptos.empty:
        for index, row in top_cryptos.iterrows():
            col1, col2, col3, col4 = st.columns([1,2,2,2])
            with col1:
                st.image(row["image"], width=40)
            with col2:
                st.write(f"**{row['name']} ({row['symbol'].upper()})**")
            with col3:
                st.write(f"💲 {row['current_price']}")
            with col4:
                st.write(f"📈 {row['price_change_percentage_24h']:.2f} %")
    else:
        st.write("Impossible de récupérer les tendances du marché pour le moment.")


    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=14)).strftime("%Y-%m-%d")
    crypto_data = {name: download_crypto_data(symbol, start_date, end_date) for name, symbol in cryptos.items()}

    st.write(f"Période analysée : {start_date} → {end_date}")

    titres_onglets = ['Bitcoin', 'Ethereum', 'Solana']
    onglet1, onglet2, onglet3 = st.tabs(titres_onglets)

    with onglet1:
        # Affichage des données Bitcoin
        st.subheader("Bitcoin ($)")
        btc_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'
        st.image(Image.open(urlopen(btc_img_url)))

        if crypto_data["Bitcoin"] is not None:
            st.table(crypto_data["Bitcoin"])
            st.line_chart(crypto_data["Bitcoin"]["Close"])
        else:
            st.warning("Impossible d'afficher les données Bitcoin.")

    with onglet2:
    # Affichage des données Ethereum
        st.subheader("Ethereum ($)")
        eth_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png'
        st.image(Image.open(urlopen(eth_img_url)))

        if crypto_data["Ethereum"] is not None:
            st.table(crypto_data["Ethereum"])
            st.line_chart(crypto_data["Ethereum"]["Close"])
        else:
            st.warning("Impossible d'afficher les données Ethereum.")

    with onglet3:
    # Affichage des données Solana
        st.subheader("Solana ($)")
        sol_img_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png'
        st.image(Image.open(urlopen(sol_img_url)))

        if crypto_data["Solana"] is not None:
            st.table(crypto_data["Solana"])
            st.line_chart(crypto_data["Solana"]["Close"])
        else:
            st.warning("Impossible d'afficher les données Solana.")
