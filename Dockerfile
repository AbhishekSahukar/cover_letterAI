# ─────────────────────────────────────────────
# Stage 1 — Build the React frontend
# ─────────────────────────────────────────────
FROM node:20-alpine AS frontend

WORKDIR /app

COPY coverletter-ai/package*.json ./
RUN npm ci --silent

COPY coverletter-ai/ ./
RUN npm run build

# ─────────────────────────────────────────────
# Stage 2 — Python backend + serve static files
# ─────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy the compiled React app into the backend's static folder
COPY --from=frontend /app/dist ./backend/static

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]