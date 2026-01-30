# DesignAudit AI - Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Git

### Step 1: Clone & Setup Directories

```bash
cd DesignAudit-AI

# Install dependencies
npm install              # Frontend
python -m pip install -r backend/requirements.txt  # Backend
```

### Step 2: Environment Configuration

```bash
# Copy and configure environment variables
cp .env.example .env

# Edit .env with your:
# - Database credentials
# - API keys (OpenAI, Anthropic)
# - AWS S3 or Vercel Blob credentials
```

### Step 3: Database Setup

```bash
# Create database
psql -U postgres -c "CREATE DATABASE designaudit_dev;"

# Run migrations (when available)
# alembic upgrade head
```

### Step 4: Start Services

**Terminal 1 - Backend:**
```bash
# Run from repo root
python -m backend.main
# FastAPI running on http://localhost:8000
```

**Terminal 2 - Redis (if not containerized):**
```bash
redis-server
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
# Next.js running on http://localhost:3000
```

## Full Development Setup

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: designaudit
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: designaudit_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://designaudit:dev_password@postgres:5432/designaudit_dev
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app

volumes:
  postgres_data:
```

## Testing the API

### Upload Design Image

```bash
curl -X POST http://localhost:8000/api/audits/upload \
  -F "file=@design.png" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
{
  "audit_id": "audit_123abc",
  "status": "pending",
  "created_at": "2024-01-29T10:00:00Z"
}
```

### Check Audit Status

```bash
curl http://localhost:8000/api/audits/audit_123abc \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
{
  "id": "audit_123abc",
  "status": "completed",
  "inspector": {...},
  "analyst": {...},
  "advisor": {...},
  "created_at": "2024-01-29T10:00:00Z"
}
```

## Project Structure Overview

```
DesignAudit-AI/
├── frontend/           # Next.js 14 application
│   ├── app/           # App router
│   ├── components/    # React components
│   └── package.json
│
├── backend/           # FastAPI application
│   ├── main.py        # Entry point
│   ├── config.py      # Configuration
│   ├── routes/        # API endpoints
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   └── requirements.txt
│
├── agents/            # AI Agent system
│   ├── orchestrator.py     # Main workflow
│   ├── inspector/          # Vision analysis
│   ├── analyst/            # Rules engine
│   └── advisor/            # LLM feedback
│
├── docker-compose.yml # Container orchestration
└── .env.example      # Environment template
```

## Next Steps

### Phase 1: MVP (1-2 weeks)
- [ ] Set up Next.js frontend with upload UI
- [ ] Create FastAPI backend scaffold
- [ ] Implement Inspector agent with GPT-4 Vision
- [ ] Create database schema
- [ ] Build basic results display

### Phase 2: Multi-Agent System (2-3 weeks)
- [ ] Implement Analyst agent rules engine
- [ ] Build Advisor agent with LLM integration
- [ ] Create orchestrator workflow
- [ ] Integrate async task queue
- [ ] Build audit report display

### Phase 3: Polish & Scale (2-3 weeks)
- [ ] Implement heatmap visualization
- [ ] Build chat interface for follow-up questions
- [ ] Add user authentication
- [ ] Optimize performance
- [ ] Deploy to production

## Common Issues & Solutions

### Database Connection Error
```
Error: could not connect to server
Solution: Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify credentials: psql -U user -d designaudit_dev
```

### Redis Connection Error
```
Error: Error 111 connecting to localhost:6379
Solution: 
- Start Redis: redis-server
- Or use Docker: docker run -d -p 6379:6379 redis:7
```

### OpenAI API Error
```
Error: Invalid API key
Solution:
- Get key from https://platform.openai.com/api-keys
- Add to .env: OPENAI_API_KEY=sk-...
```

### Port Already in Use
```
Error: Address already in use
Solution: Change port in .env or kill process:
- Linux/Mac: lsof -i :3000 && kill -9 <PID>
- Windows: netstat -ano | findstr :3000
```

## Useful Commands

```bash
# Backend
python -m pytest                    # Run tests
python -m black backend/           # Format code
python -m mypy backend/            # Type checking

# Frontend
npm run dev                        # Development
npm run build                      # Production build
npm run lint                       # Lint code

# Database
psql -U designaudit -d designaudit_dev  # Connect to DB
alembic revision --autogenerate -m "description"  # Create migration

# Docker
docker-compose down -v            # Clean up volumes
docker-compose logs --tail=100 backend  # View logs
```

## Deployment

### Vercel (Frontend)
```bash
vercel link
vercel deploy
```

### Cloud Run (Backend)
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/designaudit-backend
gcloud run deploy designaudit-backend \
  --image gcr.io/PROJECT_ID/designaudit-backend \
  --platform managed \
  --region us-central1
```

## Support & Resources

- **Issues:** GitHub Issues in the repository
- **Documentation:** See ARCHITECTURE.md, API.md
- **API Docs:** http://localhost:8000/docs (FastAPI Swagger)
- **Design Resources:** See feedback_generator.py for curated links
