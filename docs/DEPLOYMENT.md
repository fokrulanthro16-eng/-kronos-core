# KRONOS CORE — Deployment Guide

This document covers every supported deployment target from local development to cloud VPS production.

---

## Quick Reference

| Target | Backend URL | Frontend URL | Time to Deploy |
|--------|------------|--------------|----------------|
| Local (bare Python) | http://127.0.0.1:8000 | http://localhost:3000 | 2 min |
| Local Docker Compose | http://localhost:8000 | — (API only) | 5 min |
| Docker + nginx | http://localhost:80 | — | 10 min |
| Render | https://your-app.onrender.com | https://your-fe.onrender.com | 15 min |
| Railway | https://your-app.railway.app | https://your-fe.railway.app | 15 min |
| VPS (Ubuntu) | https://api.yourdomain.com | https://yourdomain.com | 30 min |

---

## 1. Local Development (No Docker)

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip, npm

### Backend

```bash
cd kronos-core

# Create and activate virtual environment (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — at minimum set a real SECRET_KEY

# Start backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Verify
curl http://127.0.0.1:8000/api/v1/health
# → {"status":"healthy","service":"KRONOS CORE",...}
```

### Frontend

```bash
cd kronos-core/frontend

# Configure environment
cp .env.local.example .env.local
# BACKEND_URL defaults to http://127.0.0.1:8000 — no change needed for local dev

# Install dependencies
npm install

# Start dev server
npm run dev
# → http://localhost:3000
```

---

## 2. Local Docker Compose (Recommended for Demo)

Single command brings up the hardened backend container.

### Prerequisites
- Docker 24+
- Docker Compose v2

### Steps

```bash
cd kronos-core

# Generate a real secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Set environment variables
export SECRET_KEY=<output from above>
export ALLOWED_ORIGINS=http://localhost:3000

# Build and start
docker compose up --build -d

# Check logs
docker compose logs -f kronos-core

# Verify
curl http://localhost:8000/api/v1/health

# Stop
docker compose down
```

### Environment variable overrides

Create a `docker-compose.override.yml` for local secrets (this file is gitignored):

```yaml
# docker-compose.override.yml  — DO NOT COMMIT
services:
  kronos-core:
    environment:
      - SECRET_KEY=your-actual-secret-key-here
      - ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

Then run: `docker compose up -d`

---

## 3. Docker + nginx Reverse Proxy (Production Local / VPS)

Uses the included `nginx/nginx.conf` as a reverse proxy with rate limiting.

### Update docker-compose.yml to include nginx

Add this service to `docker-compose.yml`:

```yaml
  nginx:
    image: nginx:1.27-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - kronos-core
    restart: unless-stopped
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
```

Then:
```bash
docker compose up --build -d
curl http://localhost/api/v1/health
```

---

## 4. Render Deployment

Render offers a free tier suitable for demo and MVP hosting.

### Backend (Render Web Service)

1. Push your repository to GitHub (see [GitHub Setup](#github-setup) below)
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repository
4. Configure:
   - **Name:** `kronos-core-api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (demo) or Starter ($7/month for production)
5. Add Environment Variables in the Render dashboard:
   ```
   APP_ENV=production
   SECRET_KEY=<generate with python -c "import secrets; print(secrets.token_hex(32))">
   ALLOWED_ORIGINS=https://your-frontend.onrender.com
   LOG_LEVEL=INFO
   RATE_LIMIT_PER_MINUTE=60
   ```
6. Deploy → note the URL: `https://kronos-core-api.onrender.com`

### Frontend (Render Static Site)

1. Render → New → Static Site
2. Connect the same repository
3. Configure:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `frontend/out`
   - **Environment Variables:**
     ```
     BACKEND_URL=https://kronos-core-api.onrender.com
     ```
4. Deploy → URL: `https://kronos-core-frontend.onrender.com`

> **Note:** For Next.js with API rewrites to work on Render static, consider deploying as a Node service instead of a static site:
> - **Build Command:** `npm install && npm run build`
> - **Start Command:** `npm start`

---

## 5. Railway Deployment

Railway has a generous free tier and first-class Docker support.

### Backend

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
cd kronos-core
railway init

# Set environment variables
railway variables set APP_ENV=production
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
railway variables set ALLOWED_ORIGINS=https://your-frontend.up.railway.app
railway variables set LOG_LEVEL=INFO

# Deploy
railway up

# Get your URL
railway open
```

Railway will auto-detect the `Dockerfile` and build accordingly.

### Frontend on Railway

```bash
cd kronos-core/frontend

# Init a new service in the same project
railway init

# Set env
railway variables set BACKEND_URL=https://your-backend.up.railway.app

# Deploy
railway up
```

---

## 6. VPS Deployment (Ubuntu 22.04 / 24.04)

Full production setup with nginx SSL, systemd, and Docker.

### Prerequisites on VPS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Install nginx (for SSL termination)
sudo apt install -y nginx certbot python3-certbot-nginx
```

### Deploy Application

```bash
# Clone repository
git clone https://github.com/yourusername/kronos-core.git
cd kronos-core

# Configure environment
cp .env.example .env
nano .env
# Set: SECRET_KEY, ALLOWED_ORIGINS=https://yourdomain.com, APP_ENV=production

# Build and start
docker compose up --build -d

# Verify local
curl http://localhost:8000/api/v1/health
```

### Configure nginx + SSL

```bash
# Create nginx site config
sudo nano /etc/nginx/sites-available/kronos-core
```

```nginx
server {
    server_name api.yourdomain.com;

    location / {
        proxy_pass         http://localhost:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header   Connection "";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kronos-core /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Issue SSL certificate (requires DNS pointing to VPS)
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal is configured by certbot automatically
```

### Deploy Frontend (Next.js on VPS)

```bash
cd kronos-core/frontend
cp .env.local.example .env.local
# Set: BACKEND_URL=https://api.yourdomain.com

npm install
npm run build

# Run with PM2 (process manager)
npm install -g pm2
pm2 start npm --name "kronos-frontend" -- start
pm2 save
pm2 startup
```

Configure nginx for frontend:

```nginx
server {
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass       http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## GitHub Setup

```bash
cd kronos-core

# Initialize git (if not already done)
git init
git add .
git commit -m "feat: KRONOS CORE v1.0 — initial release"

# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/kronos-core.git
git branch -M main
git push -u origin main
```

> **Before pushing:** Run `git status` and confirm `.env`, `.venv/`, `node_modules/`, and `.next/` are NOT listed as tracked files. They should all be gitignored.

---

## Environment Variable Reference

### Backend (`/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_NAME` | No | `KRONOS CORE` | Service name in health response |
| `APP_VERSION` | No | `1.0.0` | Version string |
| `APP_ENV` | No | `production` | Runtime mode |
| `SECRET_KEY` | **Yes** | — | Min 32 chars, random hex |
| `ALLOWED_ORIGINS` | No | `http://localhost:3000` | CORS allowlist, comma-separated |
| `RATE_LIMIT_PER_MINUTE` | No | `60` | Global rate limit per IP |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
| `PORT` | No | `8000` | Bind port |

### Frontend (`/frontend/.env.local`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BACKEND_URL` | No | `http://127.0.0.1:8000` | Backend base URL for API rewrites |

---

## Health Check

After any deployment, confirm the service is healthy:

```bash
# Backend
curl https://api.yourdomain.com/api/v1/health

# Expected response
{
  "status": "healthy",
  "service": "KRONOS CORE",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2026-..."
}
```
