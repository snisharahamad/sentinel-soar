import sqlite3
import requests
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Le chemin exact du fichier actif que nous venons de trouver
LOG_FILE_PATH = "/var/lib/docker/volumes/5d7c6ee786f919126911048a271dc7c71328236da21f2812a3c799669aba32e2/_data/log/cowrie/cowrie.json"

def setup_database():
    conn = sqlite3.connect('sentinel.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intrusions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            ip VARCHAR(50),
            login VARCHAR(50),
            password VARCHAR(50)
        )
    """)
    conn.commit()
    conn.close()

def process_intrusion(ip, login, password, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Archivage SQL
    conn = sqlite3.connect('sentinel.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO intrusions (timestamp, ip, login, password) VALUES (?, ?, ?, ?)", (now, ip, login, password))
    conn.commit()
    conn.close()

    # Déclenchement de l'alerte
    if WEBHOOK_URL:
        alerte = "🚨 FRAPPE REPOUSSÉE" if status == "failed" else "☠️ BRÈCHE CRITIQUE (SUCCÈS)"
        payload = {
            "content": f"{alerte}\n**IP:** {ip}\n**Tentative:** `{login}` / `{password}`\n**Heure:** {now}"
        }
        requests.post(WEBHOOK_URL, json=payload)
        print(f"[{now}] Intrusion {status} de {ip} archivée et signalée.")

def monitor_logs():
    print(f"Démarrage de la surveillance du fichier: {LOG_FILE_PATH}")
    # Ouvre le fichier à la fin (tail)
    with open(LOG_FILE_PATH, 'r') as file:
        file.seek(0, os.SEEK_END)
        
        # Boucle de surveillance infinie
        while True:
            line = file.readline()
            if not line:
                time.sleep(1) # Pause pour ne pas surcharger le processeur
                continue
                
            try:
                # Traduction JSON -> Dictionnaire Python
                log_data = json.loads(line)
                
                # Traque des événements de connexion
                if log_data.get("eventid") == "cowrie.login.failed":
                    process_intrusion(log_data.get("src_ip"), log_data.get("username"), log_data.get("password"), "failed")
                elif log_data.get("eventid") == "cowrie.login.success":
                    process_intrusion(log_data.get("src_ip"), log_data.get("username"), log_data.get("password"), "success")
            except json.JSONDecodeError:
                pass # Ignore les lignes mal formatées

if __name__ == "__main__":
    setup_database()
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\nArrêt manuel de Sentinel-SOAR.")