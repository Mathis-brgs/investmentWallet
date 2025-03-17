import streamlit as st

def show_login_page():
    st.title("Connexion")
    
    # Créer le formulaire de connexion
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit_button = st.form_submit_button("Se connecter")
        
        if submit_button:
            # Pour l'exemple, identifiants en dur
            if username == "admin" and password == "password":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Connexion réussie!")
                st.rerun()
            else:
                st.error("Identifiants incorrects")