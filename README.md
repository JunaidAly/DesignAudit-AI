# DesignAudit AI 🎨✨

**Your AI-Powered Design Team Member**

An intelligent web platform that analyzes design screenshots and provides actionable, human-like feedback from specialized AI agents—all within 60 seconds.

![Status](https://img.shields.io/badge/status-active--development-brightgreen)
![Version](https://img.shields.io/badge/version-0.1.0-blue)

---

## 🚀 Quick Start (5 Minutes)

```bash
# With Docker (easiest)
docker-compose up -d

# Or manually
cd backend && python main.py      # Terminal 1
cd frontend && npm run dev        # Terminal 2
```

Open http://localhost:3000

---

## 📚 Documentation (Start Here!)

| Document | Purpose |
|----------|---------|
| **[QUICK_START.md](QUICK_START.md)** | ⭐ Quick reference, commands, troubleshooting |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | What's completed & implementation options |
| **[BLUEPRINT.md](BLUEPRINT.md)** | Complete product specification |
| **[docs/SETUP.md](docs/SETUP.md)** | Detailed setup & deployment |
| **[docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** | Week-by-week development guide |
| **[docs/API.md](docs/API.md)** | API endpoint reference |

---

## 🏗️ Architecture

```
Design Screenshot Upload
        ↓
┌─────────────────────────────┐
│  Inspector Agent            │
│  Computer Vision Analysis   │
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│  Analyst Agent              │
│  Rules-Based Violations     │
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│  Advisor Agent              │
│  LLM-Synthesized Feedback   │
└─────────────────────────────┘
        ↓
Results + Heatmap + Chat Interface
```

**Tech Stack:** Next.js 14 • FastAPI • PostgreSQL • Redis • OpenAI/Claude

---

## ✅ What's Ready

- [x] Complete product blueprint
- [x] Multi-agent architecture design
- [x] Inspector agent (vision analysis)
- [x] Analyst agent (50+ design heuristics)
- [x] Advisor agent (LLM feedback)
- [x] Orchestrator service
- [x] FastAPI backend scaffold
- [x] Database schema design
- [x] Docker configuration
- [x] Full documentation & guides

**Not Yet:** Frontend components, API endpoints, GPT-4 integration

---

## 🎯 Next Steps

**Choose one to get started:**

1. 📖 **[Read PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** (5 min)
   - What's been built
   - Implementation options
   - Recommended next steps

2. 🚀 **[Follow QUICK_START.md](QUICK_START.md)** (10 min)
   - Common commands
   - Quick reference
   - Troubleshooting

3. 🛠️ **[Check IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** (30 min)
   - Week-by-week roadmap
   - Code examples
   - Cost breakdown

4. 🏢 **[Full SETUP.md](docs/SETUP.md)** (60 min)
   - Complete local setup
   - Docker deployment
   - Production deployment

---

## 📁 Project Structure

```
DesignAudit-AI/
├── agents/                    # AI Agent System ✅
│   ├── orchestrator.py       # Workflow orchestration
│   ├── inspector/            # Vision analysis
│   ├── analyst/              # Rules engine
│   └── advisor/              # LLM feedback
│
├── backend/                  # FastAPI ✅
│   ├── main.py              # App entry point
│   ├── config.py            # Configuration
│   └── requirements.txt
│
├── frontend/                # Next.js 🚧
├── docs/                    # Documentation ✅
├── docker-compose.yml       # Containers ✅
└── .env.example            # Env template ✅
```

---

## 🤝 Contributing

This is an active development project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

**Having issues?** Check [QUICK_START.md#troubleshooting](QUICK_START.md)

**Need setup help?** See [docs/SETUP.md](docs/SETUP.md)

**Want to understand the vision?** Read [BLUEPRINT.md](BLUEPRINT.md)

---

## 📄 License

MIT License - see LICENSE file

---

**Ready?** Start with [QUICK_START.md](QUICK_START.md) → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) → [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)
