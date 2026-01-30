# DesignAudit AI - Project Structure

```
DesignAudit-AI/
├── BLUEPRINT.md                 # Product blueprint and architecture
├── project.json                 # Project metadata
│
├── frontend/                    # Next.js 14 application
│   ├── app/                     # App router pages
│   │   ├── page.tsx            # Home/dashboard
│   │   ├── upload/             # Upload page
│   │   ├── audit/              # Audit results page
│   │   └── api/                # API routes
│   ├── components/             # Reusable React components
│   │   ├── UploadForm.tsx
│   │   ├── AuditReport.tsx
│   │   ├── HeatmapOverlay.tsx
│   │   └── ChatInterface.tsx
│   ├── public/                 # Static assets
│   ├── styles/                 # Global styles
│   ├── lib/                    # Utility functions
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.ts
│
├── backend/                    # FastAPI/Python backend
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   │
│   ├── routes/                # API endpoints
│   │   ├── auth.py
│   │   ├── audits.py
│   │   └── uploads.py
│   │
│   ├── models/                # Database models
│   │   ├── user.py
│   │   ├── audit.py
│   │   └── audit_result.py
│   │
│   ├── services/              # Business logic
│   │   ├── upload_service.py
│   │   ├── audit_service.py
│   │   └── storage_service.py
│   │
│   ├── middleware/            # Authentication, validation
│   └── Dockerfile
│
├── agents/                    # AI Agent system
│   ├── __init__.py
│   ├── orchestrator.py        # Main orchestration logic
│   │
│   ├── inspector/             # Computer Vision Agent
│   │   ├── __init__.py
│   │   ├── vision_analyzer.py
│   │   └── json_mapper.py
│   │
│   ├── analyst/               # Rules-Based Agent
│   │   ├── __init__.py
│   │   ├── rules_engine.py
│   │   ├── design_heuristics.py
│   │   └── wcag_validator.py
│   │
│   ├── advisor/               # LLM Agent
│   │   ├── __init__.py
│   │   └── feedback_generator.py
│   │
│   ├── prompts/               # System prompts
│   │   ├── inspector_prompt.txt
│   │   ├── analyst_prompt.txt
│   │   └── advisor_prompt.txt
│   │
│   └── tasks/                 # Celery task definitions
│       └── audit_pipeline.py
│
├── database/                  # Database schema & migrations
│   ├── schema.sql
│   └── migrations/
│
├── docker-compose.yml         # Local development
├── .env.example              # Environment variables template
└── docs/                     # Documentation
    ├── ARCHITECTURE.md
    ├── API.md
    └── SETUP.md
```

## Quick Start Phases

### Phase 1: MVP (Single Agent)
- [ ] Set up Next.js frontend with upload interface
- [ ] Set up FastAPI backend with upload endpoint
- [ ] Create PostgreSQL schema
- [ ] Implement Inspector agent (GPT-4 Vision)
- [ ] Display basic feedback

### Phase 2: Full System
- [ ] Implement Analyst agent (rules engine)
- [ ] Implement Advisor agent (LLM synthesis)
- [ ] Build orchestrator
- [ ] Create audit pipeline with task queue

### Phase 3: Polish
- [ ] Build heatmap visualization
- [ ] Implement chat interface
- [ ] Add authentication
- [ ] Optimize performance
