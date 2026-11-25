#!/usr/bin/env bash
# Lance TrouveTaMusique (http://localhost:8020)
cd "$(dirname "$0")"
exec ./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8020
