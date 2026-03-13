# Bible Art App

Bible Art App is a full-stack MVP for exploring links between biblical stories, characters, locations, and artworks.

## Stack

- Python 3.11+
- FastAPI
- SQLite
- React + Vite
- React Router
- Tailwind CSS

## Project Structure

- `backend/` FastAPI application and API routes
- `database/` SQLite schema + seed SQL/data
- `frontend/` React client
- `scripts/` operational scripts (seed/reseed/validation/smoke tests)
- `render.yaml` Render service + persistent disk blueprint

## Local development

### One-command startup

```bash
bash scripts/dev.sh
```

This installs backend/frontend dependencies, starts FastAPI on `8000`, and starts Vite on `5173`.

### Backend only

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### Frontend only

```bash
cd frontend
npm ci
npm run dev
```

---

## Production deployment (Render + Vercel)


## Automated deployment with GitHub Actions (recommended)

This repository includes two production deployment workflows:

- `.github/workflows/deploy-backend-render.yml`
- `.github/workflows/deploy-frontend-vercel.yml`

Both workflows support:
- automatic trigger on `push` to `main` for relevant paths
- manual trigger via **Actions → Run workflow** (`workflow_dispatch`)

### Required GitHub Secrets

Add these repository secrets in **GitHub → Settings → Secrets and variables → Actions**.

#### Render (backend)

- `RENDER_DEPLOY_HOOK_URL`  
  Render deploy hook URL for your backend web service.
- `RENDER_HEALTHCHECK_URL`  
  Full backend health endpoint URL (example: `https://your-api.onrender.com/health`).

#### Vercel (frontend)

- `VERCEL_TOKEN`  
  Vercel personal/team token with deploy access.
- `VERCEL_ORG_ID`  
  Vercel org/team ID.
- `VERCEL_PROJECT_ID`  
  Vercel project ID for the frontend app.
- `VITE_API_BASE_URL`  
  Production backend base URL injected during CI build (example: `https://your-api.onrender.com`).

### How automated deployment works

#### Backend workflow (`Deploy Backend to Render`)

1. Calls `RENDER_DEPLOY_HOOK_URL` with `POST`.
2. Polls `RENDER_HEALTHCHECK_URL` until it returns `{"status":"ok"}`.
3. Fails the workflow if health does not pass within the timeout window.

#### Frontend workflow (`Deploy Frontend to Vercel`)

1. Pulls project metadata using `VERCEL_TOKEN` + `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID`.
2. Builds production artifacts with `vercel build --prod`, injecting `VITE_API_BASE_URL`.
3. Deploys via `vercel deploy --prebuilt --prod`.
4. Performs a smoke check against the deployment URL.

### How to trigger deployment

- **Automatic:** push to `main` with changes in backend/frontend paths.
- **Manual:** open GitHub Actions tab and run either deploy workflow.

> Note: You still need one-time platform setup (Render service + deploy hook + disk, Vercel project linked to `frontend/`). After that, deployments are fully GitHub Actions-driven.

---

## 1) Backend on Render (Web Service)

Use `render.yaml` (Blueprint deploy) or configure manually.

### Render settings

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`
- Persistent disk:
  - Name: `bible-art-data`
  - Mount path: `/var/data`
  - Size: 1 GB

### Backend environment variables

- `DATABASE_PATH=/var/data/bible_art.db`
- `AUTO_SEED_DB=true` (first deploy only)
- `ALLOWED_ORIGINS=https://<your-vercel-domain>`

### First deploy vs later deploys

- First successful deploy: keep `AUTO_SEED_DB=true` so Render initializes and seeds the DB when `/var/data/bible_art.db` is absent.
- After seed is complete and service is healthy: set `AUTO_SEED_DB=false` to avoid accidental reseeding behavior on unexpected disk events.

### Health check

```bash
curl https://<your-render-service>.onrender.com/health
# expected: {"status":"ok"}
```

## 2) Frontend on Vercel

Set the Vercel project **Root Directory** to `frontend`.

### Vercel settings

- Framework preset: Vite
- Build command: `npm run build`
- Output directory: `dist`

### Frontend environment variable

- `VITE_API_BASE_URL=https://<your-render-service>.onrender.com`

The app uses this value in production requests. Local development can continue using Vite `/api` proxy.

## 3) CORS alignment

Set backend `ALLOWED_ORIGINS` to the exact deployed frontend origins, comma-separated if multiple:

```env
ALLOWED_ORIGINS=https://your-app.vercel.app,https://www.yourdomain.com
```

---

## Smoke test checklist (post-deploy)

Use the included script:

```bash
bash scripts/smoke_test.sh https://<frontend-domain> https://<backend-domain>
```

This validates:
- `GET /health` returns `{"status":"ok"}`
- stories list endpoint responds with data
- one story detail endpoint responds
- frontend homepage responds
- CORS preflight allows frontend origin

---

## Rollback notes

### Backend rollback (Render)

- Use Render dashboard -> Deploys -> rollback to last healthy deploy.
- Keep the same persistent disk mounted so SQLite data survives code rollback.

### Frontend rollback (Vercel)

- Use Vercel dashboard -> Deployments -> promote previous successful deployment.

### Data rollback

- SQLite lives on Render disk at `/var/data/bible_art.db`.
- Snapshot/download before risky changes.

---

## API endpoints

### Stories
- `GET /stories`
- `GET /stories/{id}`

### Characters
- `GET /characters`
- `GET /characters/{id}`

### Locations
- `GET /locations`
- `GET /locations/{id}`

### Artworks
- `GET /artworks`
- `GET /artworks/{id}`

### Health
- `GET /health`
