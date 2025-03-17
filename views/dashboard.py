import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen
import pandas as pd
import requests
from datetime import datetime, timedelta
from views.login import show_login_page
import plotly.graph_objects as go
import numpy as np
import ta

# Initialiser l'état de connexion s'il n'existe pas
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def show_dashboard():
    if not st.session_state.get('logged_in', False):
        show_login_page()
        return

    # Layout principal
    st.title("Dashboard")
    
    # Première section : Vue d'ensemble du portefeuille
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Valeur totale du portefeuille",
            value="$25,000",
            delta="+ $1,200 (4.8%)"
        )
    with col2:
        st.metric(
            label="Profit/Perte 24h",
            value="+ $180",
            delta="2.3%"
        )
    with col3:
        st.metric(
            label="Nombre d'actifs",
            value="8",
            delta="2 nouveaux"
        )

    # Deuxième section : Graphique principal
    st.subheader("Évolution du portefeuille")
    
    # Création d'un graphique exemple avec Plotly (a installer)
    @st.cache_data
    def get_portfolio_history():
        # Simulation de données historiques
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Value': [20000 + i * 100 + np.random.randn() * 500 for i in range(len(dates))]
        })
        return data

    portfolio_data = get_portfolio_history()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=portfolio_data['Date'],
        y=portfolio_data['Value'],
        fill='tozeroy',
        name='Portfolio Value'
    ))
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Troisième section : Répartition des actifs (déplacé dans wallet)

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

    #Recuperer les tendances du marchés
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
            
            # Trier par la plus forte hausse en pourcentage sur 24h
            df = df.sort_values(by="price_change_percentage_24h", ascending=False)
            
            # Sélectionner les 5 cryptos les plus performantes
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

    # Nouvelle section : Indicateurs Techniques
    st.subheader("Indicateurs Techniques")
    
    # Sélection de l'actif pour l'analyse technique
    asset_for_analysis = st.selectbox(
        "Sélectionner un actif pour l'analyse technique",
        ["Bitcoin", "Ethereum", "Solana", "Tesla"]
    )

    # Récupération des données pour l'analyse technique
    @st.cache_data
    def get_asset_data(asset):
        if asset in ["Bitcoin", "Ethereum", "Solana"]:
            symbol = {"Bitcoin": "BTC-USD", "Ethereum": "ETH-USD", "Solana": "SOL-USD"}[asset]
        else:
            symbol = "TSLA"
        
        try:
            # Télécharger les données
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            # Récupérer les données brutes
            df = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                interval='1d'
            )
            
            if df.empty:
                st.error(f"Aucune donnée disponible pour {asset}")
                return None

            # Créer un nouveau DataFrame avec uniquement les prix de clôture
            data = pd.DataFrame()
            data['Close'] = df['Close']
            
            # Calcul des indicateurs techniques
            # Moyennes mobiles
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            
            # RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp1 - exp2
            
            # Bandes de Bollinger
            data['BB_middle'] = data['Close'].rolling(window=20).mean()
            data['BB_high'] = data['BB_middle'] + 2 * data['Close'].rolling(window=20).std()
            data['BB_low'] = data['BB_middle'] - 2 * data['Close'].rolling(window=20).std()
            
            return data
            
        except Exception as e:
            st.error(f"Erreur lors du calcul des indicateurs pour {asset}: {str(e)}")
            return None

    # Récupération des données
    technical_data = get_asset_data(asset_for_analysis)

    # Création des onglets pour différents types d'analyses
    tab1, tab2, tab3 = st.tabs(["Moyennes Mobiles & Bollinger", "RSI", "MACD"])

    # Vérification des données avant d'afficher les graphiques
    if technical_data is not None:
        with tab1:
            fig = go.Figure()
            
            # Prix de clôture
            fig.add_trace(go.Scatter(
                x=technical_data.index,
                y=technical_data['Close'],
                name='Prix',
                line=dict(color='blue')
            ))
            
            # SMA 20
            fig.add_trace(go.Scatter(
                x=technical_data.index,
                y=technical_data['SMA_20'],
                name='SMA 20',
                line=dict(color='orange', dash='dash')
            ))
            
            # SMA 50
            fig.add_trace(go.Scatter(
                x=technical_data.index,
                y=technical_data['SMA_50'],
                name='SMA 50',
                line=dict(color='green', dash='dash')
            ))
            
            # Bandes de Bollinger
            fig.add_trace(go.Scatter(
                x=technical_data.index,
                y=technical_data['BB_high'],
                name='BB Supérieure',
                line=dict(color='gray', dash='dot')
            ))
            
            fig.add_trace(go.Scatter(
                x=technical_data.index,
                y=technical_data['BB_low'],
                name='BB Inférieure',
                line=dict(color='gray', dash='dot'),
                fill='tonexty'
            ))

            fig.update_layout(
                title=f"Analyse Technique - {asset_for_analysis}",
                height=500,
                xaxis_title="Date",
                yaxis_title="Prix"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            if not technical_data['RSI'].isnull().all():
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=technical_data.index,
                    y=technical_data['RSI'],
                    name='RSI'
                ))
                
                fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Surachat")
                fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Survente")
                
                fig.update_layout(
                    title="RSI",
                    height=300,
                    yaxis=dict(range=[0, 100])
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Données RSI non disponibles")

        with tab3:
            if not technical_data['MACD'].isnull().all():
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=technical_data.index,
                    y=technical_data['MACD'],
                    name='MACD'
                ))
                
                fig.update_layout(
                    title="MACD",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Données MACD non disponibles")
    else:
        st.warning("Données non disponibles pour cet actif")
