import calendar
from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import database as db
import pandas as pd

def show_data():
    st.title("Investment Tracker :money_with_wings:")

 
    years = [datetime.today().year, datetime.today().year + 1]
    months = list(calendar.month_name[1:])

 
    selected = option_menu(
        menu_title=None,
        options=["Data Entry", "Data Visualization"],
        icons=["pencil-fill", "bar-chart-fill"],
        orientation="horizontal",
    )


    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    def create_investment_form(investment_type):
        if investment_type == "Actions":
            st.subheader("Actions")
            date = st.date_input("Date", label_visibility="visible")
            action_name = st.text_input("Action Name", label_visibility="visible")
            unity_price = st.number_input("Unity Price", min_value=0, format="%i", step=10, label_visibility="visible")
            quantity = st.number_input("Quantity", min_value=0, format="%i", step=10, label_visibility="visible")
            comment = st.text_area("Comment", placeholder="Enter a comment here ...", label_visibility="visible")
            return {
                "date": date,
                "action_name": action_name,
                "unity_price": unity_price,
                "quantity": quantity,
                "comment": comment
            }
        elif investment_type == "Crypto":
            st.subheader("Crypto")
            date = st.date_input("Date", label_visibility="visible")
            crypto_name = st.text_input("Crypto Name", label_visibility="visible")
            unity_price = st.number_input("Unity Price", min_value=0, format="%i", step=10, label_visibility="visible")
            quantity = st.number_input("Quantity", min_value=0, format="%i", step=10, label_visibility="visible")
            comment = st.text_area("Comment", placeholder="Enter a comment here ...", label_visibility="visible")
            return {
                "date": date,
                "crypto_name": crypto_name,
                "unity_price": unity_price,
                "quantity": quantity,
                "comment": comment
            }
        elif investment_type == "Immobilier":
            st.subheader("Immobilier")
            date = st.date_input("Date", label_visibility="visible")
            type_immobilier = st.text_input("Type Immobilier", label_visibility="visible")
            metrage = st.number_input("Metrage", min_value=0, format="%i", step=10, label_visibility="visible")
            localisation = st.text_input("Localisation", label_visibility="visible")
            price = st.number_input("Price", min_value=0, format="%i", step=10, label_visibility="visible")
            comment = st.text_area("Comment", placeholder="Enter a comment here ...", label_visibility="visible")
            return {
                "date": date,
                "type_immobilier": type_immobilier,
                "metrage": metrage,
                "localisation": localisation,
                "price": price,
                "comment": comment
            }
        return {}

    def get_investment_data(investment_type, data):
        if investment_type == "Actions":
            return {
                "date": data["date"],
                "action_name": data["action_name"],
                "unity_price": data["unity_price"],
                "quantity": data["quantity"],
                "price": data["unity_price"] * data["quantity"],
                "comment": data["comment"]
            }
        elif investment_type == "Crypto":
            return {
                "date": data["date"],
                "crypto_name": data["crypto_name"],
                "unity_price": data["unity_price"],
                "quantity": data["quantity"],
                "price": data["unity_price"] * data["quantity"],
                "comment": data["comment"]
            }
        elif investment_type == "Immobilier":
            return {
                "date": data["date"],
                "type_immobilier": data["type_immobilier"],
                "metrage": data["metrage"],
                "localisation": data["localisation"],
                "price": data["price"],
                "comment": data["comment"]
            }
        return {}

    # Traitement de l'entrée des données
    if selected == "Data Entry":
        st.header("Data Entry")

        investment_type = option_menu(
            menu_title=None,
            options=["Actions", "Crypto", "Immobilier"],
            icons=["activity", "currency-bitcoin", "house-door"],
            orientation="horizontal",
        )

        with st.form("entry_form", clear_on_submit=True):
            data = create_investment_form(investment_type)
            submitted = st.form_submit_button("Save Data")
            if submitted:
                period = str(st.session_state.get("year", datetime.today().year)) + "_" + str(st.session_state.get("month", datetime.today().month))
                investment_data = get_investment_data(investment_type, data)
                db.insert_investment(period, investment_type, investment_data)
                st.success("Data saved!")

    elif selected == "Data Visualization":
        st.header("Data Visualization")

        # Sélecteur pour filtrer les données
        filter_options = ["Actions", "Crypto", "Immobilier"]
        selected_filter = st.selectbox("Filter by Investment Type", filter_options)

        # Récupérer les données de la base de données
        investments = db.fetch_portfolio_data()

        # Filtrer les données en fonction du sélecteur
        filtered_investments = [inv for inv in investments if inv['investment_type'] == selected_filter]

        # Afficher les données en fonction du type d'investissement
        if selected_filter == "Actions":
            if filtered_investments:
                for inv in filtered_investments:
                    st.write(f"**Date:** {inv['data']['date']}")
                    st.write(f"**Action Name:** {inv['data']['action_name']}")
                    st.write(f"**Unity Price:** {inv['data']['price']}")
                    st.write(f"**Quantity:** {inv['data']['quantity']}")
                    st.write(f"**Total Invested:** {inv['data']['price']}")
                    st.write(f"**Comment:** {inv['data']['comment']}")
                    st.write("---")
            else:
                st.warning("No data available for Actions.")

        elif selected_filter == "Crypto":
            if filtered_investments:
                for inv in filtered_investments:
                    st.write(f"**Date:** {inv['data']['date']}")
                    st.write(f"**Crypto Name:** {inv['data']['crypto_name']}")
                    st.write(f"**Unity Price:** {inv['data']['price']}")
                    st.write(f"**Quantity:** {inv['data']['quantity']}")
                    st.write(f"**Total Invested:** {inv['data']['price']}")
                    st.write(f"**Comment:** {inv['data']['comment']}")
                    st.write("---")
            else:
                st.warning("No data available for Crypto.")

        elif selected_filter == "Immobilier":
            if filtered_investments:
                for inv in filtered_investments:
                    st.write(f"**Date:** {inv['data']['date']}")
                    st.write(f"**Type Immobilier:** {inv['data']['type_immobilier']}")
                    st.write(f"**Metrage:** {inv['data']['metrage']}")
                    st.write(f"**Localisation:** {inv['data']['localisation']}")
                    st.write(f"**Price:** {inv['data']['price']}")
                    st.write(f"**Comment:** {inv['data']['comment']}")
                    st.write("---")
            else:
                st.warning("No data available for Immobilier.")


if __name__ == "__main__":
    show_data()
