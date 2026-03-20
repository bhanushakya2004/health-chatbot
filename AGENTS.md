# Repository Guidelines

## Project Structure & Module Organization
- `healthcare-api/`: FastAPI backend. Core code in `healthcare-api/app/` with `routes/`, `models/`, `services/`, and `utils/`. Uploads and logs live in `healthcare-api/uploads/` and `healthcare-api/logs/`.
- `medicare-chat/`: React + Vite frontend. Source in `medicare-chat/src/` with `components/`, `pages/`, `hooks/`, and `lib/`.
- Root files: `docker-compose.yml` for full-stack containers, `QUICKSTART.md` for setup, and `.env.template` for environment variables.

## Build, Test, and Development Commands
- Backend install: `cd healthcare-api` then `pip install -r requirements.txt`.
- Backend dev server: `python -m uvicorn app.main:app --reload` (serves `http://localhost:8000`).
- Seed data (first run): `python seed_database.py`.
- Frontend install: `cd medicare-chat` then `npm install`.
- Frontend dev server: `npm run dev` (serves `http://localhost:5173`).
- Frontend build: `npm run build` (production bundle).
- Frontend lint: `npm run lint` (ESLint for TS/TSX).
- Frontend tests: `npm run test` (Vitest).
- Docker stack: `docker-compose up --build` (MongoDB + backend + frontend).

## Coding Style & Naming Conventions
- Python: 4-space indentation; keep FastAPI routes in `app/routes/` and business logic in `app/services/`.
- TypeScript/React: follow existing TSX patterns in `medicare-chat/src/` and keep UI pieces in `components/`.
- Use descriptive file names (`patientService.ts`, `authRoutes.py`) and match existing casing in each folder.
- Run `npm run lint` before frontend changes; backend has no configured formatter, so keep diffs minimal and consistent.

## Testing Guidelines
- Frontend tests use Vitest (see `medicare-chat/src/test/`). Name tests `*.test.ts` or `*.test.tsx`.
- No backend test runner is configured. If adding tests, place them under `healthcare-api/tests/` and document how to run them.

## Commit & Pull Request Guidelines
- Recent commits use a mix of styles (e.g., `feat: ...` and plain messages). Prefer `type: short summary` when possible.
- Keep commits scoped and explain user-visible impact.
- PRs should include: purpose summary, linked issues (if any), and screenshots for UI changes.

## Security & Configuration Tips
- Do not commit secrets. Use `healthcare-api/.env` and `medicare-chat/.env` (see `.env.template`).
- MongoDB must be running locally or via Docker before starting the backend.
