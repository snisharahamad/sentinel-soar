# 🛡️ Sentinel-SOAR

> **Security Orchestration, Automation, and Response** daemon for Cowrie Honeypots.

Sentinel-SOAR is a lightweight Python daemon designed to monitor, parse, and respond in real-time to SSH/Telnet attacks captured by a Cowrie honeypot.

## 🏗️ Data Pipeline Architecture

The data flow is direct and isolated: 
1. **Interception:** Cowrie absorbs the attack (CGNAT restricted) and generates a JSON log. 
2. **Parsing:** The Python daemon monitors this file in real-time (non-blocking I/O).
3. **Dual Action:** It archives the trace in a local SQLite relational database for historical analysis, while simultaneously triggering an HTTP POST request to a Discord Webhook for sub-second alerting.

## ✨ Core Features

* **Real-Time Parsing:** Continuous reading of the `cowrie.json` file using an end-of-file pointer (`os.SEEK_END`).
* **SQL Archiving:** Structuring attack metadata (IP, credentials, timestamp) into a local relational database (`sqlite3`).
* **Instant Alerting:** Push notifications via HTTP Webhook.
* **Secrets Management:** Utilizing `python-dotenv` to securely isolate URLs and credentials from the source code.

## ⚙️ Deployment (Industry Standard)

### 1. Prerequisites
* Python 3.10+
* A virtual environment (recommended: `uv` package manager)

### 2. Installation
```bash
git clone [https://github.com/snisharahamad/sentinel-soar.git](https://github.com/snisharahamad/sentinel-soar.git)
cd sentinel-soar
uv venv
uv pip install python-dotenv requests
```

### 3. Security Configuration
Create a `.env` file at the root to isolate the secret (intentionally ignored by Git):
```env
WEBHOOK_URL="[https://discord.com/api/webhooks/YOUR_SECRET_LINK](https://discord.com/api/webhooks/YOUR_SECRET_LINK)"
```

### 4. Startup
```bash
uv run sentinel_soar.py
```
