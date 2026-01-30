# Getting Started with DesignAudit AI

Complete guide to setting up and running the DesignAudit AI platform.

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows 10+
- **Processor**: 2+ cores (4+ recommended)
- **Memory**: 4GB minimum, 8GB+ recommended
- **Storage**: 2GB free space

### Required Software
- **Node.js**: 18.0 or higher ([Download](https://nodejs.org/))
- **Python**: 3.9 or higher ([Download](https://www.python.org/))
- **PostgreSQL**: 13 or higher ([Download](https://www.postgresql.org/))
- **Redis**: 6 or higher ([Download](https://redis.io/))

**OR** if you prefer Docker:
- **Docker**: 20.10+ ([Download](https://www.docker.com/))
- **Docker Compose**: 2.0+ (included with Docker Desktop)

### API Keys Required
- **OpenAI API Key** - For GPT-4 Vision analysis ([Get Key](https://platform.openai.com/))
- **(Optional) Anthropic API Key** - Alternative LLM provider ([Get Key](https://console.anthropic.com/))

---

## 🐳 Option 1: Docker Setup (Recommended for New Users)

### Step 1: Clone Repository
```bash
git clone <repository-url> DesignAudit-AI
cd DesignAudit-AI
```

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required:
# - OPENAI_API_KEY=sk-...
# - DATABASE_URL (can stay as is for Docker)
# - REDIS_URL (can stay as is for Docker)
```

### Step 3: Start Services
```bash
# Start all containers
docker-compose up -d

# Verify services are running
docker-compose ps

# Check logs (optional)
docker-compose logs -f

# Wait for services to be ready (30-60 seconds)
```

### Step 4: Access Application
Open your browser and navigate to: **http://localhost:3000**

### Useful Docker Commands
```bash
# View logs
docker-compose logs -f backend    # Backend logs
docker-compose logs -f frontend   # Frontend logs
docker-compose logs -f postgres   # Database logs

# Stop services
docker-compose down

# Stop and remove data
docker-compose down -v

# Rebuild containers
docker-compose build --no-cache

# Run database migrations
docker-compose exec backend alembic upgrade head
```

---

## 🖥️ Option 2: Manual Setup (Development)

### Step 1: Clone Repository
```bash
git clone <repository-url> DesignAudit-AI
cd DesignAudit-AI
```

### Step 2: Setup Backend

**macOS/Linux:**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp ../.env.example ../.env
# Edit .env - set your OpenAI API key

# Initialize database (first time only)
alembic upgrade head

# Start backend server
python main.py
```

**Windows (PowerShell):**
```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
copy ..\.env.example ..\.env
# Edit .env - set your OpenAI API key

# Initialize database (first time only)
alembic upgrade head

# Start backend server
python main.py
```

The backend will start on **http://localhost:8000**

### Step 3: Setup Frontend (New Terminal)

**macOS/Linux:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Windows (PowerShell):**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on **http://localhost:3000**

### Step 4: Start Background Tasks (New Terminal)

**macOS/Linux:**
```bash
cd backend
source venv/bin/activate

# Start Celery worker for async tasks
celery -A tasks worker -l info
```

**Windows (PowerShell):**
```bash
cd backend
.\venv\Scripts\Activate.ps1

# Start Celery worker for async tasks
celery -A tasks worker -l info
```

### Step 5: Access Application
Open http://localhost:3000 in your browser

---

## ⚙️ Environment Configuration

### Essential Settings (.env)

```env
# AI APIs (Required)
OPENAI_API_KEY=sk-your-key-here

# Database (Local PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/designaudit_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Upload limits
MAX_UPLOAD_SIZE_MB=10

# Timeouts (seconds)
AUDIT_TIMEOUT_SECONDS=300
```

### Optional Settings

```env
# Alternative LLMs
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...

# Cloud Storage (AWS S3)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=designaudit-uploads
AWS_REGION=us-east-1

# Alternative Storage (Vercel Blob)
VERCEL_BLOB_TOKEN=...

# Authentication
JWT_SECRET=your-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

---

## 🧪 Testing the Setup

### Backend Health Check
```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","service":"DesignAudit AI API","version":"0.1.0"}
```

### Frontend Check
Open http://localhost:3000 in your browser - you should see the upload form

### Full Integration Test
1. Go to http://localhost:3000
2. Upload a screenshot (any image file)
3. Wait for analysis to complete (30-60 seconds)
4. View the audit report

---

## 🐛 Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Find what's using port 3000
lsof -i :3000  # macOS/Linux
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess  # Windows

# Use different ports
docker-compose.yml - update ports section
```

**Services not starting:**
```bash
# Check service status
docker-compose ps

# View detailed logs
docker-compose logs

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Backend Issues

**Python dependency errors:**
```bash
# Clear and reinstall
pip install --upgrade pip
pip cache purge
pip install -r requirements.txt
```

**Database connection errors:**
```bash
# Verify PostgreSQL is running
psql -U postgres -c "\l"

# Create database if missing
createdb designaudit_dev

# Update DATABASE_URL in .env
```

**Port 8000 in use:**
```bash
# Change in backend/main.py or set PORT environment variable
PORT=8001 python main.py
```

### Frontend Issues

**Dependencies not installing:**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 in use:**
```bash
# Use different port
npm run dev -- -p 3001
```

**API not connecting:**
- Check `.env` has correct `NEXT_PUBLIC_API_URL`
- Verify backend is running: `curl http://localhost:8000`
- Check CORS settings in backend

---

## 📁 Project Structure Reference

```
DesignAudit-AI/
├── frontend/              # Next.js frontend
│   ├── app/
│   │   ├── components/   # React components
│   │   ├── lib/         # Utilities, API client
│   │   └── store/       # State management
│   ├── package.json
│   └── next.config.js
│
├── backend/              # FastAPI backend
│   ├── main.py          # Entry point
│   ├── models.py        # Database models
│   ├── database.py      # Database setup
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   ├── tasks.py         # Celery tasks
│   ├── config.py        # Configuration
│   └── requirements.txt
│
├── agents/              # AI agents
│   ├── orchestrator.py  # Multi-agent coordinator
│   ├── inspector/       # Vision analysis
│   ├── analyst/         # Rules-based analysis
│   └── advisor/         # LLM feedback
│
├── docs/               # Documentation
├── docker-compose.yml  # Docker setup
└── .env.example       # Configuration template
```

---

## 🎯 Next Steps

1. **Upload a design** - Try the full audit flow
2. **Explore API** - Visit http://localhost:8000/docs for interactive docs
3. **Customize rules** - Modify `agents/analyst/rules_engine.py`
4. **Deploy** - See [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)

---

## 📚 Additional Resources

- [API Documentation](../docs/API.md)
- [Product Blueprint](../BLUEPRINT.md)
- [Quick Reference](../QUICK_START.md)
- [Architecture Guide](../docs/ARCHITECTURE.md)

---

## 💬 Need Help?

- Check [Troubleshooting](#-troubleshooting) above
- Review [QUICK_START.md](../QUICK_START.md)
- Look at issue examples in `/docs`
- Check code comments for implementation details

---

**Happy auditing! 🚀**