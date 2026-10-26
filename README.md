# 🔐 VaultDrop — Secure File Sharing

<div align="center">

![VaultDrop Banner](https://img.shields.io/badge/VaultDrop-Secure%20File%20Sharing-00e5ff?style=for-the-badge&logo=shield&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![Supabase](https://img.shields.io/badge/Supabase-Backend-3ECF8E?style=flat-square&logo=supabase)](https://supabase.com)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=flat-square&logo=railway)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Share files securely using AES-256 encryption with one-time access codes.**  
No account required. No traces left behind.

[🌐 Live Demo](https://vaultdrop-production-c71a.up.railway.app) · [📖 Documentation](#documentation) · [🚀 Getting Started](#getting-started)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔒 **AES-256-GCM Encryption** | Files are encrypted client-side before being sent anywhere |
| 🧠 **Zero-Knowledge Architecture** | The server never sees your file or its name — only encrypted bytes |
| 🎫 **One-Time Access Codes** | Each upload generates a unique code required to decrypt and download |
| ⏱️ **Auto-Expiry** | Files self-destruct after 1 hour, 24 hours, 3 days, or 7 days |
| 🔥 **Burn-After-Reading** | Set a max download limit — file is permanently destroyed when reached |
| 📱 **Responsive Design** | Works seamlessly on desktop and mobile |
| ⚡ **No Account Needed** | Upload and share instantly without signing up |

---

## 🛠️ Tech Stack

### Frontend
- **HTML5 / CSS3 / Vanilla JavaScript**
- **Web Crypto API** — For client-side AES-256-GCM encryption
- **Supabase JS SDK** — Storage and database communication

### Backend
- **Python 3.10+** with **Flask** — Serves the web application
- **Gunicorn** — Production WSGI server

### Cloud Services
- **Supabase Storage** — Stores encrypted file blobs (zero-knowledge)
- **Supabase Database** — Stores file metadata (expiry, quota, UUID)
- **Railway** — Hosting and deployment platform

---

## 🏗️ Project Structure

```
VaultDrop/
│
├── app.py                    # Flask application entry point
├── Procfile                  # Railway/Gunicorn deployment config
├── requirements.txt          # Python dependencies
├── .railwayignore            # Files excluded from Railway deployment
│
├── templates/
│   └── secure-fileshare.html # Main application page (Jinja2 template)
│
├── static/
│   └── styles.css            # Application stylesheet
│
└── uploads/                  # Temporary upload directory (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com) project with:
  - A storage bucket named `encrypted_vault`
  - A table named `vault_registry`

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/vaultdrop.git
   cd vaultdrop
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   python app.py
   ```

5. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

---

## 🗄️ Supabase Setup

### 1. Create the `vault_registry` table
Run this SQL in your Supabase **SQL Editor**:

```sql
CREATE TABLE IF NOT EXISTS public.vault_registry (
  id            TEXT PRIMARY KEY,
  ttl_timestamp BIGINT NOT NULL,
  quota         INTEGER NOT NULL DEFAULT 1,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.vault_registry ENABLE ROW LEVEL SECURITY;

-- Allow public access (no auth required)
CREATE POLICY "allow_insert" ON public.vault_registry FOR INSERT WITH CHECK (true);
CREATE POLICY "allow_select" ON public.vault_registry FOR SELECT USING (true);
CREATE POLICY "allow_update" ON public.vault_registry FOR UPDATE USING (true);
CREATE POLICY "allow_delete" ON public.vault_registry FOR DELETE USING (true);
```

### 2. Create the `encrypted_vault` storage bucket
In Supabase → **Storage** → **New Bucket**:
- Name: `encrypted_vault`
- Public: `false` (Private)

Then add Storage Policies:
```sql
CREATE POLICY "allow_upload"   ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'encrypted_vault');
CREATE POLICY "allow_download" ON storage.objects FOR SELECT USING (bucket_id = 'encrypted_vault');
CREATE POLICY "allow_delete"   ON storage.objects FOR DELETE USING (bucket_id = 'encrypted_vault');
```

---

## 🔄 How It Works

```
User selects file
      │
      ▼
AES-256-GCM key + IV generated (browser)
      │
      ▼
File encrypted client-side (Web Crypto API)
      │
      ├──→ Encrypted file ──→ Supabase Storage
      └──→ Encrypted metadata ──→ Supabase Storage
                │
                ▼
         UUID + Expiry + Quota ──→ Supabase Database
                │
                ▼
    Access Code = UUID # AES-Key # IV
    (shared with recipient)
```

**Download flow:**
- Recipient enters the access code
- UUID is used to fetch encrypted file from Supabase
- AES key and IV from the code decrypt the file in the browser
- Quota is decremented — file destroyed when quota reaches 0

---

## ☁️ Deployment on Railway

1. Push your code to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Railway auto-detects the `Procfile` and deploys with Gunicorn

The `Procfile` contains:
```
web: gunicorn app:app
```

---

## 📦 Dependencies

```
flask
gunicorn
werkzeug
```

---

## 🔒 Security Notes

- **Encryption happens entirely in the browser** — the server is a simple file router
- **The server never stores decryption keys** — they exist only in the access code
- **Files are stored as opaque encrypted blobs** — filenames are also encrypted
- **Access codes are single-use** by default and time-limited

---

## 👨‍💻 Author

- **Mamoud AKmali**

> Graduation Project — Computer Science Department

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
