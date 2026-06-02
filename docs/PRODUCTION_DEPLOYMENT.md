# KRONOS CORE — Production Deployment Guide

## Prerequisites

- Docker 24+ and Docker Compose v2
- A domain name (e.g. `api.kronos-core.com`)
- A Supabase project (free tier works)
- Optional: Stripe account for billing

---

## Option 1: Render (Recommended for fast launch)

1. Push repository to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect GitHub repo
4. Configure:
   - **Runtime:** Docker
   - **Dockerfile path:** `Dockerfile`
   - **Port:** 8000
5. Add environment variables in Render dashboard (copy from `.env.production.example`)
6. Set **Health Check Path:** `/api/v1/health`
7. Deploy

Frontend (Next.js):
1. New → Static Site or Web Service
2. **Build command:** `cd frontend && npm install && npm run build`
3. **Publish directory:** `frontend/.next` (or use Vercel instead)
4. Add `NEXT_PUBLIC_API_BASE_URL=https://your-api.onrender.com`

---

## Option 2: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link
railway login
railway link

# Deploy backend
railway up --service backend

# Set env vars
railway variables set APP_ENV=production
railway variables set CORS_ALLOWED_ORIGINS=https://your-frontend.up.railway.app
# ... add all vars from .env.production.example
```

Frontend: Create a separate Railway service for the Next.js app.

---

## Option 3: VPS (DigitalOcean / Hetzner / Linode)

```bash
# On your VPS — install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Clone repo
git clone https://github.com/your-username/kronos-core.git
cd kronos-core

# Create production env file
cp .env.production.example .env
nano .env   # fill in all values

# Build and start
docker compose up -d --build

# Check health
curl http://localhost:8000/api/v1/health
```

---

## Option 4: Docker Compose (Full stack with Nginx)

```bash
# Generate a strong secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Set environment
export SECRET_KEY=<output-from-above>
export CORS_ALLOWED_ORIGINS=https://your-domain.com
export SUPABASE_URL=https://xxxx.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=sb_secret_...
# ... set all production vars

# Build and start backend
docker compose up -d --build

# Verify
docker ps
docker logs kronos-core
curl http://localhost:8000/api/v1/health
```

### Passing all env vars to docker-compose

Create a `.env` file at project root (git-ignored) with all production values from `.env.production.example`. Docker Compose reads it automatically.

---

## Option 5: Nginx Reverse Proxy

The `nginx/nginx.conf` is pre-configured to proxy to `kronos-core:8000`.

Add Nginx to `docker-compose.yml`:

```yaml
  nginx:
    image: nginx:1.27-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro   # SSL certificates
    depends_on:
      - kronos-core
    restart: unless-stopped
```

For HTTPS, add an SSL server block to `nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name api.your-domain.com;

    ssl_certificate     /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # ... same location blocks as port 80 config
}

server {
    listen 80;
    server_name api.your-domain.com;
    return 301 https://$host$request_uri;
}
```

---

## Option 6: Domain + HTTPS with Let's Encrypt (Certbot)

```bash
# Install Certbot on VPS
sudo apt install certbot python3-certbot-nginx

# Stop nginx if running on port 80
sudo systemctl stop nginx

# Obtain certificate
sudo certbot certonly --standalone -d api.your-domain.com

# Certs saved to:
#   /etc/letsencrypt/live/api.your-domain.com/fullchain.pem
#   /etc/letsencrypt/live/api.your-domain.com/privkey.pem

# Mount into nginx container via docker-compose volume
# Auto-renew: certbot renews automatically via systemd timer
```

---

## Environment Variables Checklist

| Variable | Required | Notes |
|---|---|---|
| `APP_ENV` | Yes | Set to `production` |
| `SECRET_KEY` | Yes | Min 32 random chars — generate fresh |
| `CORS_ALLOWED_ORIGINS` | Yes | Your exact frontend domain |
| `SUPABASE_URL` | SaaS | Required for history/auth features |
| `SUPABASE_ANON_KEY` | SaaS | Public key — safe in backend |
| `SUPABASE_SERVICE_ROLE_KEY` | SaaS | Server-only — never expose to frontend |
| `JWT_SECRET` | SaaS | From Supabase JWT settings |
| `STRIPE_SECRET_KEY` | Billing | Server-only — never expose to frontend |
| `STRIPE_WEBHOOK_SECRET` | Billing | From Stripe webhook settings |
| `STRIPE_PRICE_STARTER` | Billing | Price ID from Stripe dashboard |
| `STRIPE_PRICE_PRO` | Billing | Price ID from Stripe dashboard |
| `STRIPE_PRICE_ENTERPRISE` | Billing | Price ID from Stripe dashboard |

Frontend variables (in `frontend/.env.local` or hosting dashboard):

| Variable | Notes |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Your backend URL, e.g. `https://api.your-domain.com` |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key — safe for browser |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key — safe for browser |

---

## Docker Security Profile (already configured)

The existing `Dockerfile` and `docker-compose.yml` implement:

| Control | Configuration |
|---|---|
| Non-root user | UID/GID 10001 (`kronos`) |
| Capability drop | `cap_drop: ALL` |
| Privilege escalation | `no-new-privileges: true` |
| Read-only filesystem | `read_only: true` |
| Writable tmp | `tmpfs: /tmp:size=64m` |
| Resource limits | 1 CPU, 512 MB RAM |
| Health check | `/api/v1/health` every 30s |
| Structured logging | JSON via structlog → stdout |

No changes needed to the existing Dockerfile or docker-compose.yml for production.

---

## Frontend Deployment (Vercel — easiest)

```bash
# Install Vercel CLI
npm install -g vercel

cd frontend

# Deploy
vercel --prod

# Set env vars in Vercel dashboard:
#   NEXT_PUBLIC_API_BASE_URL=https://api.your-domain.com
#   NEXT_PUBLIC_SUPABASE_URL=...
#   NEXT_PUBLIC_SUPABASE_ANON_KEY=...
#   NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=...
```
