import streamlit as st
import yfinance as yf
from PIL import Image
from urllib.request import urlopen

st.title("Outil d'Analyse de portfeuille d'investissement")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.write("Test de duo")

st.header("Main Dashboard")

# definir les variables
Bitcoin = 'BTC-USD'
Ethereum = 'ETH-USD'
Ripple = 'XRP-USD'
BitcoinCash = 'BCH-USD'

#Acces au data par yahoo finance
BTC_Data = yf.Ticker(Bitcoin)
ETH_Data = yf.Ticker(Ethereum)
XRP_Data = yf.Ticker(Ripple)
BCH_Data = yf.Ticker(BitcoinCash)

#Recupere l'historique
BTHhis = BTC_Data.history(period="max")
ETHhis = ETH_Data.history(period="max")
XRPhis = XRP_Data.history(period="max")
BCHhis = BCH_Data.history(period="max")

# Fetch crypto data for the dataframe
BTC = yf.download(Bitcoin, start="2025-02-01", end="2025-02-10")
ETH = yf.download(Ethereum, start="2025-02-01", end="2025-02-10")
XRP = yf.download(Ripple, start="2025-02-01", end="2025-02-10")
BCH = yf.download(BitcoinCash, start="2025-02-01", end="2025-02-10")

#Bitcoin
st.write("Bitcoin ($)")
imageBTC = Image.open(urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'))
#Display image
st.image(imageBTC)
#Display dataframe
st.table(BTC)