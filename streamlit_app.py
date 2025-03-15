import streamlit as st
import pandas as pd
import requests
import base64
import json
from datetime import datetime
import random as rnd

# 🛠 GITHUB EINSTELLUNGEN (ANPASSEN)
GITHUB_USER = "JohannesProgrammes"
REPO_NAME = "wg-Jonas-Johannes"
CATEGORIES = {
    "Spülmaschine ausgeräumt": "data/spülmaschine.csv",
    "Restmüll rausgebracht": "data/restmüll.csv",
    "Biomüll rausgebracht": "data/biomüll.csv",
    "Papiermüll rausgebracht": "data/papierlmüll.csv",
    "Verpackungsmüll rausgebracht": "data/Verpackungsmüll.csv",
    "Altglas": "data/altglas.csv",
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
st.set_page_config(page_title="📊 WG", page_icon="📊")
st.title("📊 WG Eifelstraße 21")
st.write("Wähle deinen Namen und eine Aktivität aus:")

# 📊 Auswahl der Eingaben
name = st.selectbox("Wähle deinen Namen", ["Jonas", "Johannes", "Heinzelmännchen"])
kategorie = st.selectbox("Wähle ein Thema", list(CATEGORIES.keys()))

# Daten aus GitHub laden
df, sha = load_data(CATEGORIES[kategorie])
df, sha = load_data("data/spülmaschine.csv")

# ✅ Antwort speichern nur bei Button-Klick
if st.button("Aktion eintragen"):
    now = datetime.now().strftime("%d.%m.%Y, %H:%M Uhr")
    new_data = pd.DataFrame([[now, name]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df, sha, CATEGORIES[kategorie])

# 📊 Ergebnisse sofort anzeigen
st.write(f"### Antworten für das Thema Spülmaschine ausgeräumt")
st.write(f"Die anderen sieht man hier nicht")
st.dataframe(df)


var_zahl = rnd.randint(0,100)
alter = st.slider("Hier ein Slider zum rumspielen", 0, 100, var_zahl)
