# Carbon Footprint PoC — Local Scaffold

This repo boots a local stack:
- **frontend**: Next.js + TypeScript (form wizard stub + file uploader)
- **api**: FastAPI + SQLAlchemy (Postgres) with starter endpoints
- **worker**: Celery worker for async tasks (OCR/NLP stubs)
- **postgres**, **redis**, **minio** (S3‑compatible object store)


## Prereqs
- Docker + Docker Compose v2
- Make (optional)


## Quickstart
```bash
cp .env.example .env
make up # or: docker compose up --build
make logs # follow logs for all services
```
App URLs:
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs
- MinIO Console: http://localhost:9001 (user/pass from .env)


## Useful Commands
```bash
make up # build & start
make down # stop & remove
make logs # tail logs
make api # shell into API container
make db # psql into Postgres
```


## Next Steps
- Implement CSV mapper UI and form steps for energy/fuel.
- Build `/sources/upload` presign endpoint + S3 (MinIO) uploader in frontend.
- Flesh out Celery OCR/NLP task to parse invoices and create `activities`.
```