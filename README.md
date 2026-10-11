# 🛡️ Sentinel-SOAR

> **Security Orchestration, Automation, and Response** daemon for Cowrie Honeypots.

Sentinel-SOAR est un démon Python léger conçu pour surveiller, parser et réagir en temps réel aux attaques SSH/Telnet capturées par un honeypot Cowrie.

## 🏗️ Architecture du Flux (Data Pipeline)

Le flux de données est direct et isolé : 
1. **Interception :** Cowrie encaisse l'attaque (CGNAT) et génère un log JSON. 
2. **Parsing :** Le démon Python surveille ce fichier en temps réel (I/O non bloquant).
3. **Double Action :** Il archive la trace à froid dans une base relationnelle SQLite pour l'historique, et déclenche simultanément une requête HTTP POST vers un Webhook Discord pour l'alerte à la seconde.

## ✨ Fonctionnalités Core

* **Parsing Temps Réel :** Lecture continue du fichier `cowrie.json` via un pointeur de fin de fichier (`os.SEEK_END`).
* **Archivage SQL :** Structuration des métadonnées d'attaque (IP, credentials, timestamp) dans une base de données relationnelle locale (`sqlite3`).
* **Alerte Instantanée :** Notification Push via Webhook HTTP.
* **Sécurité des Secrets :** Utilisation de `python-dotenv` pour isoler les URL et credentials hors du code source.

## ⚙️ Déploiement (Standard de l'industrie)

### 1. Prérequis
* Python 3.10+
* Un environnement virtuel (recommandation : gestionnaire `uv`)

### 2. Installation
```bash
git clone [https://github.com/snisharahamad/sentinel-soar.git](https://github.com/snisharahamad/sentinel-soar.git)
cd sentinel-soar
uv venv
uv pip install python-dotenv requests
```

### 3. Configuration de la Sécurité
Créer un fichier `.env` à la racine pour isoler le secret (fichier volontairement ignoré par Git) :
```env
WEBHOOK_URL="[https://discord.com/api/webhooks/VOTRE_LIEN_SECRET](https://discord.com/api/webhooks/VOTRE_LIEN_SECRET)"
```

### 4. Allumage
```bash
uv run sentinel_soar.py
```
