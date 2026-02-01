# 🚀 Docker Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- At least 4GB RAM available for containers
- API keys: GOOGLE_API_KEY or DEEPSEEK_API_KEY

### Step 1: Clone & Configure

```bash
cd health-chatbot
```

### Step 2: Create Environment File

Create `.env` file in the root directory:

```env
# AI Model API Keys (provide at least one)
GOOGLE_API_KEY=your_gemini_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Security (IMPORTANT: Change in production!)
SECRET_KEY=your-super-secret-jwt-key-min-32-chars

# Optional: Token expiry (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Step 3: Start All Services

```bash
# Start all containers (MongoDB, Backend, Frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Step 4: Access Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

### Step 5: Stop Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

---

## 📋 Container Details

### Backend Container
- **Image**: Python 3.10 slim + Tesseract OCR
- **Port**: 8000
- **Volumes**:
  - `backend-logs`: Application logs
  - `backend-uploads`: Temporary file uploads
  - `chromadb-data`: Vector database
- **Health Check**: Every 30s on `/health` endpoint

### Frontend Container
- **Image**: Nginx + React build
- **Port**: 80
- **Features**:
  - Gzip compression
  - Static asset caching
  - SPA routing support
- **Health Check**: Every 30s

### MongoDB Container
- **Image**: MongoDB 7.0
- **Port**: 27017
- **Volume**: `mongo-data` (persistent database)
- **Health Check**: Every 10s with mongosh ping

---

## 🛠 Advanced Commands

### Build Without Cache
```bash
docker-compose build --no-cache
```

### View Container Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongo
```

### Execute Commands in Containers
```bash
# Backend shell
docker-compose exec backend bash

# MongoDB shell
docker-compose exec mongo mongosh healthcare_db

# Check backend environment
docker-compose exec backend env | grep GOOGLE_API_KEY
```

### Restart Individual Services
```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart mongo
```

### Scale Backend (Multiple Workers)
```bash
docker-compose up -d --scale backend=3
```

---

## 🔧 Troubleshooting

### Issue: Backend fails to start
**Symptom**: Backend container keeps restarting

**Solutions**:
1. Check API keys are set:
   ```bash
   docker-compose exec backend env | grep API_KEY
   ```

2. Check MongoDB connection:
   ```bash
   docker-compose exec backend python -c "from pymongo import MongoClient; print(MongoClient('mongodb://mongo:27017').server_info())"
   ```

3. View backend logs:
   ```bash
   docker-compose logs backend
   ```

### Issue: Frontend shows "Network Error"
**Symptom**: Frontend can't connect to backend

**Solutions**:
1. Check backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verify CORS settings in `healthcare-api/app/main.py`

3. Check browser console for actual error

### Issue: MongoDB connection refused
**Symptom**: Backend logs show MongoDB connection errors

**Solutions**:
1. Wait for MongoDB to be healthy:
   ```bash
   docker-compose ps mongo
   ```

2. Check MongoDB logs:
   ```bash
   docker-compose logs mongo
   ```

3. Restart services:
   ```bash
   docker-compose restart
   ```

### Issue: Tesseract OCR not working
**Symptom**: Document OCR processing fails

**Solutions**:
1. Check Tesseract is installed in container:
   ```bash
   docker-compose exec backend tesseract --version
   ```

2. Rebuild backend with cache cleared:
   ```bash
   docker-compose build --no-cache backend
   ```

### Issue: Out of disk space
**Symptom**: Containers fail to start

**Solutions**:
1. Clean up unused Docker resources:
   ```bash
   docker system prune -a --volumes
   ```

2. Check disk usage:
   ```bash
   docker system df
   ```

---

## 📊 Monitoring & Health Checks

### Check Service Health
```bash
# All services
docker-compose ps

# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost/health

# MongoDB health
docker-compose exec mongo mongosh --eval "db.adminCommand('ping')"
```

### View Resource Usage
```bash
# Real-time stats
docker stats

# Specific container
docker stats healthcare-backend
```

---

## 🔐 Production Deployment

### 1. Security Checklist
- ✅ Change `SECRET_KEY` to strong random value
- ✅ Use secure API keys
- ✅ Set `ACCESS_TOKEN_EXPIRE_MINUTES` appropriately
- ✅ Enable HTTPS (use reverse proxy like Nginx/Traefik)
- ✅ Restrict MongoDB port (remove from docker-compose ports)
- ✅ Set up firewall rules
- ✅ Regular backups of MongoDB volume

### 2. Update docker-compose.yml for Production
```yaml
services:
  backend:
    restart: always
    environment:
      - SECRET_KEY=${SECRET_KEY}  # Load from .env
    # Remove port exposure, use reverse proxy
  
  mongo:
    restart: always
    # Remove ports section (internal only)
```

### 3. Use Environment-Specific Configs
```bash
# Development
docker-compose -f docker-compose.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### 4. Enable Logging
Add to docker-compose.yml:
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 📦 Data Persistence

### Backup MongoDB
```bash
# Backup
docker-compose exec mongo mongodump --out=/data/backup

# Copy to host
docker cp healthcare-mongo:/data/backup ./mongodb-backup

# Restore
docker-compose exec mongo mongorestore /data/backup
```

### Backup Volumes
```bash
# Backup all volumes
docker run --rm -v healthcare_mongo-data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/mongo-backup.tar.gz /data
```

---

## 🌐 Alternative: Using .bat Files (Windows)

If you prefer not to use Docker, use the existing .bat files:

### Start Backend
```bash
start-backend.bat
```

### Start Frontend
```bash
start-frontend.bat
```

**Requirements for .bat files:**
- Python 3.9+ with venv
- Node.js 18+
- MongoDB running on localhost:27017
- Tesseract OCR installed

---

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes* | - | Gemini API key |
| `DEEPSEEK_API_KEY` | Yes* | - | DeepSeek API key |
| `SECRET_KEY` | Yes | - | JWT signing key (32+ chars) |
| `MONGODB_URL` | No | mongodb://mongo:27017 | MongoDB connection string |
| `DATABASE_NAME` | No | healthcare_db | Database name |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 60 | Token expiry time |

*At least one AI API key required

---

## 🎯 Next Steps

1. ✅ Start services with `docker-compose up -d`
2. ✅ Open http://localhost and signup
3. ✅ Upload medical documents
4. ✅ Start chatting with AI health consultant
5. ✅ Generate health summary from profile

---

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Check health: `docker-compose ps`
3. Review this guide's troubleshooting section
4. Check API documentation: http://localhost:8000/docs

---

**Last Updated**: 2026-02-01
