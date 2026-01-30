# DesignAudit AI - Quick Reference

## 📋 Project Overview

**What it is:** An AI-powered design quality platform that analyzes UI screenshots and provides constructive feedback through three specialized agents:
1. **Inspector** - Computer vision analysis
2. **Analyst** - Rules-based violation detection
3. **Advisor** - Human-like feedback generation

**Time to MVP:** 2-3 weeks  
**Tech Stack:** Next.js + FastAPI + PostgreSQL + OpenAI/Claude

---

## 🚀 Start Here (Choose One)

### Quick Local Setup (5 minutes)
```bash
# With Docker Compose (simplest)
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Manual Setup
```bash
# 1. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
python main.py

# 2. Frontend (separate terminal)
cd frontend
npx create-next-app@latest .
npm run dev

# 3. Database
psql -U postgres -c "CREATE DATABASE designaudit_dev;"
```

---

## 📁 Key Files & Directories

| File | Purpose |
|------|---------|
| **[BLUEPRINT.md](BLUEPRINT.md)** | Complete product spec & vision |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | What's done & next steps |
| **[docs/SETUP.md](docs/SETUP.md)** | Setup & troubleshooting |
| **[docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** | Week-by-week dev guide |
| **[docs/API.md](docs/API.md)** | API endpoint reference |
| **[agents/orchestrator.py](agents/orchestrator.py)** | Multi-agent workflow |
| **[agents/inspector/vision_analyzer.py](agents/inspector/vision_analyzer.py)** | Vision analysis |
| **[agents/analyst/rules_engine.py](agents/analyst/rules_engine.py)** | Design rules (50+) |
| **[agents/advisor/feedback_generator.py](agents/advisor/feedback_generator.py)** | LLM feedback synthesis |
| **[backend/main.py](backend/main.py)** | FastAPI app |
| **[backend/config.py](backend/config.py)** | Configuration |

---

## 🔑 Environment Variables

Create `.env` (copy from `.env.example`):

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/designaudit_dev

# Redis
REDIS_URL=redis://localhost:6379

# AI APIs
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=designaudit-uploads

# Other
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

---

## 🧠 Architecture Overview

```
User Upload Image
        ↓
┌─────────────────────────┐
│   FastAPI Backend       │
│   - Upload Handler      │
│   - Task Queue (Celery) │
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│   Inspector Agent       │
│   (GPT-4 Vision)        │
│   → JSON Design Map     │
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│   Analyst Agent         │
│   (Rules Engine)        │
│   → Violations List     │
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│   Advisor Agent         │
│   (LLM Synthesis)       │
│   → Human-Readable      │
│     Feedback            │
└─────────────────────────┘
        ↓
Display Results + Chat Interface
```

---

## 🛠 Common Commands

### Backend
```bash
cd backend

# Start development server
python main.py

# Run tests
pytest

# Format code
black .

# Type checking
mypy .

# View API docs
# Open http://localhost:8000/docs
```

### Frontend
```bash
cd frontend

# Development
npm run dev

# Production build
npm run build
npm start

# Lint
npm run lint
```

### Database
```bash
# Connect to PostgreSQL
psql -U designaudit -d designaudit_dev -h localhost

# Run migrations (when available)
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "description"
```

### Docker
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Clean up volumes (WARNING: deletes data)
docker-compose down -v

# View logs
docker-compose logs -f backend
docker-compose logs -f postgres
```

---

## 🎯 Development Phases

### Phase 1: MVP (Weeks 1-3)
- [ ] Frontend: Upload interface
- [ ] Backend: Upload & audit endpoints
- [ ] Database: Core schema
- [ ] Inspector: GPT-4 Vision integration
- **Result:** Single-agent working end-to-end

### Phase 2: Multi-Agent (Weeks 4-6)
- [ ] Analyst: Rules engine
- [ ] Advisor: LLM feedback
- [ ] Orchestrator: Full workflow
- [ ] Results display: Violations list
- **Result:** Complete 3-agent system

### Phase 3: Polish (Weeks 7-8)
- [ ] Heatmap visualization
- [ ] Chat interface
- [ ] Authentication
- [ ] Performance optimization
- [ ] Production deployment

---

## 📊 API Quick Reference

### Upload Design
```bash
curl -X POST http://localhost:8000/api/audits/upload \
  -F "file=@design.png" \
  -H "Authorization: Bearer token"
```

### Get Results
```bash
curl http://localhost:8000/api/audits/audit_id \
  -H "Authorization: Bearer token"
```

### Ask Question
```bash
curl -X POST http://localhost:8000/api/audits/audit_id/chat \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I fix this?"}'
```

Full API reference: [docs/API.md](docs/API.md)

---

## 💰 Cost Estimates

| Component | Cost | Notes |
|-----------|------|-------|
| **Database** | $25/mo | Supabase or Neon |
| **Backend** | $20/mo | Cloud Run or Lambda |
| **Frontend** | $20/mo | Vercel |
| **Vision API** | $10-30/mo | GPT-4 Vision (~$0.03/image) |
| **LLM API** | $10-30/mo | GPT-4 or Claude |
| **Redis Cache** | $5/mo | Upstash |
| **Storage** | $5/mo | S3 for images |
| **Total** | **~$95-140/mo** | All-in production setup |

---

## 🔗 Useful Resources

### Documentation
- [Complete Blueprint](BLUEPRINT.md)
- [Setup Guide](docs/SETUP.md)
- [Implementation Roadmap](docs/IMPLEMENTATION.md)
- [API Reference](docs/API.md)

### AI APIs
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic Claude Docs](https://docs.anthropic.com)
- [LangChain Docs](https://python.langchain.com)

### Design Standards
- [Material Design](https://material.io)
- [Apple HCI Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref)

### Tools
- [FastAPI Swagger UI](http://localhost:8000/docs)
- [PostgreSQL Client](https://www.pgadmin.org)
- [Redis Inspector](https://redis-commander.herokuapp.com)

---

## ❓ Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Check .env DATABASE_URL
cat .env | grep DATABASE_URL
```

### Redis Connection Error
```bash
# Start Redis
redis-server

# Or with Docker
docker run -d -p 6379:6379 redis:7
```

### API Key Error
```bash
# Get API keys from:
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com

# Add to .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 📞 Next Steps

**What would you like to do?**

1. ✅ **[Set up locally](docs/SETUP.md)** - Get everything running
2. 🎨 **Build frontend** - Create upload & results UI
3. 🔌 **Set up backend** - API & database
4. 🤖 **Integrate GPT-4** - Get Inspector agent working
5. 📚 **Read implementation guide** - Week-by-week plan

Pick one and let me know! 🚀
