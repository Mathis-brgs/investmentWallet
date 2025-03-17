import streamlit as st
import pandas as pd
import requests
import yfinance as yf

def show_market():
    st.title("Marché des Cryptos & Actions")
    st.header("Aperçu du marché en temps réel")

    # Récupération des crypto
    @st.cache_data
    def get_market_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": False
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            return pd.DataFrame(data)[["name", "symbol", "image", "current_price", "price_change_percentage_24h"]]
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données du marché : {e}")
            return pd.DataFrame()

    # Récupération des actions
    @st.cache_data
    def get_stock_data(_symbols):
        stock_data = {}
        try:
            for symbol in _symbols:
                ticker = yf.Ticker(symbol)
                stock_data[symbol] = ticker.history(period="1d").iloc[-1]["Close"]
            return stock_data
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données boursières : {e}")
            return {}

    # Liste des indices boursiers et actions (on peut en rajouter si on veut)
    stocks = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "Dow Jones": "^DJI", "Apple": "AAPL", "Tesla": "TSLA"}
    stock_data = get_stock_data(stocks.values())

    market_data = get_market_data()

    # Barre de recherche pour filtrer les actifs
    search_query = st.text_input("Rechercher une crypto ou une action (nom ou symbole) :").lower()
    if search_query:
        market_data = market_data[market_data["name"].str.lower().str.contains(search_query) | market_data["symbol"].str.lower().str.contains(search_query)]
        stock_data = {k: v for k, v in stock_data.items() if search_query in k.lower()}

    # Gestion pagination avec des boutons
    st.subheader("Cryptos")

    if not market_data.empty:
        num_cryptos = len(market_data)

        # Initialiser l'index de départ
        if "start_index" not in st.session_state:
            st.session_state.start_index = 0

        # Boutons de navigation
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            if st.button("←") and st.session_state.start_index > 0:
                st.session_state.start_index -= 10
        with col3:
            if st.button("→") and st.session_state.start_index + 10 < num_cryptos:
                st.session_state.start_index += 10

        # Affichage des cryptos
        cryptos_to_display = market_data.iloc[st.session_state.start_index:st.session_state.start_index + 10]

        for index, row in cryptos_to_display.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2])
            with col1:
                st.image(row["image"], width=30)
            with col2:
                st.write(f"**{row['name']} ({row['symbol'].upper()})**")
            with col3:
                st.write(f"${row['current_price']:,}")
            with col4:
                change = row["price_change_percentage_24h"]
                color = "🟢" if change > 0 else "🔴"
                st.write(f"{color} {change:.2f}%")
            st.markdown("---")
    else:
        st.write("Aucune crypto correspondant à votre recherche.")


    # Affichage actions et indices
    st.subheader("Indices & Actions")
    if stock_data:
        stock_df = pd.DataFrame(list(stock_data.items()), columns=["Indice/Action", "Prix actuel ($)"])
        st.dataframe(stock_df.set_index("Indice/Action"))
    else:
        st.write("Aucune action ou indice correspondant à votre recherche.")

    # Graphique des variations des cryptos
    st.subheader("Performance des Cryptos sur 24h")
    if not market_data.empty:
        st.bar_chart(market_data.set_index("name")["price_change_percentage_24h"])
    else:
        st.write("Données indisponibles.")
