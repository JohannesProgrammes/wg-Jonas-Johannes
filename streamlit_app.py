import streamlit as st
import pandas as pd
import requests
import base64
import json
from datetime import datetime

# 🛠 GITHUB EINSTELLUNGEN (ANPASSEN)
GITHUB_USER = "JohannesProgrammes"
REPO_NAME = "sieger-2025"
CATEGORIES = {
    "Kategorie A": "data/kategorie_a.csv",
    "Kategorie B": "data/kategorie_b.csv",
    "Kategorie C": "data/kategorie_c.csv",
    "Kategorie D": "data/kategorie_d.csv",
    "Kategorie E": "data/kategorie_e.csv",
}
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # ⚠ Sicher speichern!

# 📅 Funktion: CSV aus GitHub laden
def load_data(csv_path):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{csv_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        return pd.read_csv(pd.io.common.StringIO(decoded_content)), response.json()["sha"]
    else:
        return pd.DataFrame(columns=["Datum", "Name"]), None

# 📄 Funktion: CSV in GitHub speichern
def save_data(df, sha, csv_path):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{csv_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    csv_content = df.to_csv(index=False).encode("utf-8")
    encoded_content = base64.b64encode(csv_content).decode("utf-8")
    
    data = {
        "message": f"Update {csv_path}",
        "content": encoded_content,
        "sha": sha  # Datei aktualisieren
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in [200, 201]:
        st.success("Antwort gespeichert! ✅")
    else:
        st.error(f"Fehler beim Speichern: {response.json()}")

# 🌟 Streamlit UI
st.set_page_config(page_title="📊 Umfrage 2025", page_icon="📊")
st.title("📊 Umfrage 2025")
st.write("Wähle deinen Namen und eine Kategorie aus:")

# 📊 Auswahl der Eingaben
name = st.selectbox("Wähle deinen Namen", ["Johannes", "Niklas", "Alex", "Maria", "Sophie"])
kategorie = st.selectbox("Wähle eine Kategorie", list(CATEGORIES.keys()))

# Daten aus GitHub laden
df, sha = load_data(CATEGORIES[kategorie])

# ✅ Antwort speichern
if st.button("Antwort absenden"):
    now = datetime.now().strftime("%d.%m.%Y, %H:%M Uhr")
    new_data = pd.DataFrame([[now, name]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df, sha, CATEGORIES[kategorie])

# 📊 Ergebnisse anzeigen
if st.checkbox("Ergebnisse anzeigen"):
    st.dataframe(df)
