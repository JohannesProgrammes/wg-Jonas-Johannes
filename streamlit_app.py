import streamlit as st
import pandas as pd
import requests
import base64
import json
from datetime import datetime
import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components



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
    "Backofen geputzt": "data/backofen.csv",
    "Küche gewischt": "data/küche.csv",
    "Fenster geputzt": "data/fenster.csv",
}
diagramme = ["Spülmaschine ausgeräumt", "Altglas", "Backofen geputzt", "Küche gewischt"]
DIAGRAMS = {x:CATEGORIES[x] for x in diagramme}
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # ⚠ Sicher speichern!
JOHANNES_TOKEN = st.secrets["JOHANNES_TOKEN"]
JONAS_TOKEN = st.secrets["JONAS_TOKEN"]


st.set_page_config(page_title="📊 WG", page_icon="📊")


# 🛠 Erlaubte Nutzer mit Passwörtern
USERS = {"Johannes": f"{JOHANNES_TOKEN}", "Jonas": f"{JONAS_TOKEN}"}

# Initialisierung von Session State
if "user" not in st.session_state:
    st.session_state["user"] = None
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""
if "auto_login_attempted" not in st.session_state:
    st.session_state["auto_login_attempted"] = False


def check_login():
    username = st.session_state["username"]
    password = st.session_state["password"]
    if USERS.get(username) == password:
        st.session_state["user"] = username
        st.success(f"✅ Eingeloggt als {username}")
        st.rerun()
    else:
        st.error("❌ Falsches Passwort!")


# Nur anzeigen, wenn nicht eingeloggt
if not st.session_state["user"]:
    # JavaScript, um das Username-Feld automatisch zu fokussieren
    components.html(
        """
        <div style="display:none;" tabindex="-1">
        <script>
        window.onload = function() {
        const inputs = window.parent.document.querySelectorAll('input[aria-label="Benutzername"]');
        if (inputs.length > 0) inputs[0].focus();
        }
        </script>
        </div>
        """,
        height=0,
    )
    st.title("🔐 Login")

    with st.form("login_form"):
        username = st.text_input("Benutzername", key="username")
        password = st.text_input("Passwort", type="password", key="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        st.session_state["auto_login_attempted"] = True
        check_login()

    st.stop()


# # 🌐 Session-Status für den eingeloggten Nutzer
# if "user" not in st.session_state:
#     st.session_state["user"] = None

# def check_login():
#     username = st.session_state["username"]
#     password = st.session_state["password"]
    
#     if USERS.get(username) == password:
#         st.session_state["user"] = username
#         st.success(f"✅ Eingeloggt als {username}")
#     else:
#         st.error("❌ Falsches Passwort!")

# # 🔐 Login-Formular anzeigen, wenn nicht eingeloggt
# if not st.session_state["user"]:
#     st.title("🔐 Login erforderlich")

#     # Benutzername und Passwort als Eingabefelder
#     username = st.text_input("Benutzername", key="username")
#     password = st.text_input("Passwort", type="password", key="password", on_change=check_login)

#     # Login-Button
#     if st.button("Login"):
#         check_login()

#     st.stop()  # 🚫 Stoppt die Ausführung der App, solange kein Login erfolgt ist



# 🌟 Hier beginnt deine App (wird nur nach Login angezeigt!)

# Eingeloggten Benutzer abrufen
user = st.session_state["user"]
users = [user] + [person for person in ["Jonas", "Johannes", "Heinzelmännchen"] if not person == user]

if st.button("Abmelden"):
    st.session_state["user"] = None
    st.rerun()


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
        return pd.DataFrame(columns=["Datum", "Account", "Name"]), None

# 📄 Funktion: CSV in GitHub speichern
def save_data(df, sha, csv_path):
    df, sha = load_data(CATEGORIES[kategorie])
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
#st.set_page_config(page_title="📊 WG", page_icon="📊")
st.title("📊 WG Eifelstraße")
st.write(f"Hallo {user}!")
st.write("Wähle deinen Namen und eine Aktivität aus:")


# 📊 Auswahl der Eingaben
name = st.selectbox("Wähle deinen Namen", users)
kategorie = st.selectbox("Wähle eine Aktivität", list(CATEGORIES.keys()))

# Daten aus GitHub laden
df, sha = load_data(CATEGORIES[kategorie])
df, sha = load_data("data/spülmaschine.csv")

# ✅ Antwort speichern nur bei Button-Klick
if st.button("Aktion eintragen"):
    now = datetime.now().strftime("%d.%m.%Y, %H:%M Uhr")
    new_data = pd.DataFrame([[now, user, name]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df, sha, CATEGORIES[kategorie])




# Daten initialisieren
personen = ["Johannes", "Jonas"]
werte = [0, 0]  # Beispielzahlen für die zwei Personen

# Daten aus GitHub laden
df, sha = load_data(CATEGORIES[kategorie])
df, sha = load_data("data/spülmaschine.csv")
#st.dataframe(df)
matrix = df.to_numpy()
for zeile in matrix:
    if zeile[2] == "Johannes":
        werte[0] += 1
    if zeile[2] == "Jonas":
        werte[1] += 1


print(werte)
if user == "Johannes":
    if werte[0] > werte[1]:
        st.write(f"### Jonas muss noch {abs(werte[0]-werte[1])} mal die Spülmaschine ausräumen")
    elif werte[0] < werte[1]:
        st.write(f"### Du musst noch {abs(werte[0]-werte[1])} mal die Spülmaschine ausräumen")
    else:
        st.write(f"### Jeder muss die Spülmaschine ausräumen, denn es ist Gleichstand")
elif user == "Jonas":
    if werte[0] > werte[1]:
        st.write(f"### Du musst noch {abs(werte[0]-werte[1])} mal die Spülmaschine ausräumen")
    elif werte[0] < werte[1]:
        st.write(f"### Johannes muss noch {abs(werte[0]-werte[1])} mal die Spülmaschine ausräumen")
    else:
        st.write(f"### Jeder muss die Spülmaschine ausräumen, denn es ist Gleichstand")
else:
    if werte[0] > werte[1]:
        st.write(f"### Jonas muss noch {abs(werte[0]-werte[1])} mal die Spülmaschine ausräumen")
    elif werte[0] < werte[1]:
        st.write(f"### Johannes muss noch {abs(werte[0]-werte[1])} mal die Spülmaschine ausräumen")
    else:
        st.write(f"### Jeder muss die Spülmaschine ausräumen, denn es ist Gleichstand")





# 📊 Ergebnisse sofort anzeigen
st.write(f"### Antworten für das Thema Spülmaschine ausgeräumt")
#st.write(f"Die anderen sieht man hier nicht")
st.dataframe(df)
matrix = df.to_numpy()
print(matrix)


# var_zahl = rnd.randint(0,100)
# alter = st.slider("Hier ein Slider zum rumspielen", 0, 100, 69)


#st.stop()


# Erstelle einen Pandas DataFrame für das Balkendiagramm
df = pd.DataFrame({
    'Personen': personen,
    'Werte': werte
})

# Horizontale Auswahl für Kategorien
# kategorie = st.radio(
#     "Wähle eine Kategorie",
#     ["Spülmaschine ausgeräumt", "Restmüll rausgebracht", "Biomüll rausgebracht", "Papiermüll rausgebracht", "Altglas"],
#     horizontal=True
# )

# Balkendiagramm erstellen
st.subheader(f"Balkendiagramm: {kategorie}")
st.bar_chart(df.set_index('Personen'))



st.stop()


# Weitere Interaktionen, je nach Auswahl
if kategorie == "Spülmaschine ausgeräumt":
    st.write("Hier kannst du die Daten zur Spülmaschine sehen...")
elif kategorie == "Restmüll rausgebracht":
    st.write("Hier kannst du die Daten zum Restmüll sehen...")
elif kategorie == "Biomüll rausgebracht":
    st.write("Hier kannst du die Daten zum Biomüll sehen...")
elif kategorie == "Papiermüll rausgebracht":
    st.write("Hier kannst du die Daten zum Papiermüll sehen...")
else:
    st.write("Hier kannst du die Daten zum Altglas sehen...")


# Erstelle einen Pandas DataFrame für das Balkendiagramm
df = pd.DataFrame({'Personen': personen, 'Werte': werte})

# 🎨 Seaborn-Theme für schöneres Design
sns.set_theme(style="whitegrid")

# 📌 Dropdown für Kategorien (anstelle von radio)
kategorie = st.selectbox(
    "Wähle eine Kategorie",
    ["Spülmaschine ausgeräumt", "Restmüll rausgebracht", "Biomüll rausgebracht", "Papiermüll rausgebracht", "Altglas"]
)

# 🏆 Schöneres Balkendiagramm mit Matplotlib
st.subheader(f"Balkendiagramm: {kategorie}")

fig, ax = plt.subplots(figsize=(6, 4))
colors = ["#4CAF50", "#FF9800"]  # Grün & Orange für die Balken

bars = ax.bar(df["Personen"], df["Werte"], color=colors, edgecolor="black", linewidth=1.2)

# 🎨 Runde Ecken für Balken (funktioniert nur mit Patch-Objekten in Matplotlib)
for bar in bars:
    bar.set_linewidth(0)  # Entfernt harte Kanten
    bar.set_alpha(0.9)  # Leichte Transparenz
    bar.set_capstyle('round')  # Runde Balken-Ecken

# Achsen entfernen für cleanen Look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticklabels(df["Personen"], fontsize=12)
ax.set_yticks([])  # Entfernt Zahlen auf Y-Achse für cleanes Design

st.pyplot(fig)

# 🔍 Extra Infos zur gewählten Kategorie
st.write(f"Details zur Kategorie **{kategorie}** kommen hier...")




kategorie = st.selectbox("Wähle eine Aktivität", diagramme)

# Beispiel-Daten
data = pd.DataFrame({
    "Person": ["Johannes", "Jonas"],
    "Aktionen": [10, 7]
}).set_index("Person")

# Balkendiagramm in Streamlit
st.bar_chart(data)




fig, ax = plt.subplots()
personen = ["Johannes", "Jonas"]
werte = [10, 7]

bars = ax.bar(personen, werte, color=["royalblue", "tomato"], edgecolor="black")

# Runde Balken-Ecken simulieren
for bar in bars:
    bar.set_linewidth(2)
    bar.set_alpha(0.9)
    bar.set_linestyle("solid")
    bar.set_capstyle("round")  # Macht die Kanten weicher

ax.set_title("💡 Aktionen im Überblick")
ax.set_ylabel("Anzahl")
ax.set_ylim(0, max(werte) + 5)

st.pyplot(fig)




def johannes(daten):
    namen, counts = np.unique(daten[:, 2], return_counts=True)
    if "Johannes" in namen:
        return 

    name_counts = dict(zip(namen, counts))
    print(name_counts, namen, counts)
    print(name_counts["Johannes"])
    sorted_counts = dict(sorted(name_counts.items(), key=lambda item: item[1], reverse=True))
    print(sorted_counts)


# Beispiel-Daten
df = pd.DataFrame({
    "Johannes": [3, 2, 4],
    "Jonas": [1, 5, 2]
}, index=["Kategorie A", "Kategorie B", "Kategorie C"])

# Balkendiagramm
st.bar_chart(df)