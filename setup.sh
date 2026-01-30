#!/bin/bash

# DesignAudit AI - Complete Setup Script
# This script sets up the entire development environment

set -e

echo "🚀 DesignAudit AI - Development Setup"
echo "======================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
    echo -e "${YELLOW}⚠️  Please update .env with your API keys${NC}"
    echo ""
fi

# Setup Backend
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Installing dependencies..."
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

cd ..

# Setup Frontend
echo -e "${BLUE}Setting up Frontend...${NC}"
cd frontend

echo "Installing dependencies..."
npm install --silent
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

cd ..

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Update .env with your API keys:"
echo "   - OPENAI_API_KEY"
echo "   - DATABASE_URL (if using PostgreSQL)"
echo "   - AWS credentials (if using S3)"
echo ""
echo "2. Start the services:"
echo "   Option A - With Docker Compose:"
echo "     docker-compose up -d"
echo ""
echo "   Option B - Manually:"
echo "     # Terminal 1 - Backend"
echo "     cd backend && source venv/bin/activate && python main.py"
echo ""
echo "     # Terminal 2 - Frontend"
echo "     cd frontend && npm run dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "- README.md - Project overview"
echo "- QUICK_START.md - Quick reference"
echo "- BLUEPRINT.md - Feature specifications"
echo "- docs/ - Detailed documentation"
