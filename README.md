# Salmon Farm Dashboard – Studentpraksis-app

Dette prosjektet er utviklet som et **opplæringsdashboard** for akvakulturstudenter i Norge, og simulerer virkelige arbeidsprosesser i lakseoppdrett. Studentene kan samle inn data under gårdsbesøk og sende det inn i sanntid via et nettbasert grensesnitt. Systemet gir umiddelbare analyser og visualiseringer som støtter interaktiv læring og bedre forståelse av fiskehelse, produksjon og miljøfaktorer.

---

## 📦 Funksjoner

* Registrer fiskedata som vekt, lengde, lusenivå og observasjoner
* Last opp bilder av fisk (valgfritt)
* Filtrer og vis data etter klasse/gruppe eller besøksdato
* Sanntidsdiagrammer og sammendrag (lusetrender, gjennomsnittsvekt, m.m.)
* Bygget med **Streamlit**, **Python**, og åpne biblioteker

---

## 🚀 Kom i gang (lokal oppsett)

### 1. Klon dette repositoriet

```bash
git clone https://github.com/Shreeramghimire/salmon-farm-dashboard.git
cd salmon-farm-dashboard
```

### 2. Opprett virtuelt miljø (anbefalt)

```bash
python -m venv venv
venv\Scripts\activate  # for Windows
```

### 3. Installer avhengigheter

```bash
pip install -r requirements.txt
```

### 4. Kjør applikasjonen

```bash
streamlit run app.py
```

Appen åpnes automatisk i nettleseren din på `http://localhost:8501/`

---

## 📁 Prosjektstruktur

```
.
├── app.py                # Streamlit-app (skjema + dashbord)
├── requirements.txt      # Python-avhengigheter
├── README.md             # Denne filen
├── data/
│   └── submissions.csv   # Innsendt studentdata
├── images/               # (Valgfritt) Opplastede fiskebilder
└── .gitignore            # Ignorerte filer/mapper
```

---

## 📊 Fremtidige funksjoner

* Integrasjon med værdata (API)
* Bildeanalyse (f.eks. lusedeteksjon med AI)
* Innlogging med gruppe/QR-kode for elever
* Kartvisning av merdanlegg og sensordata

---

## ✍️ Forfatter

**Shreeram Ghimire**
Master i Akvakultur | Utvikler | Salmon Knowledge Center
🔗 GitHub: [Shreeramghimire](https://github.com/Shreeramghimire)

---

## 📝 Lisens

MIT-lisens – Fritt å bruke og modifisere med kreditering.
