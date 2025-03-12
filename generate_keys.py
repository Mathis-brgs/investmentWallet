import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Jerome Weibel", "Mathis Borges"]
usernames = ["jweibel", "mborges"]
passwords = ["abc123", "def456"]

hashed_passwords = [stauth.Hasher([]).hash(pw) for pw in passwords]  # Hash chaque mot de passe individuellement

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)