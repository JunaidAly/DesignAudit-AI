# DesignAudit AI - Implementation Guide

## Phase 1: MVP Setup (Single Agent Inspector)

This phase gets a working prototype running quickly. We'll focus on the upload → Inspector pipeline.

### Week 1: Project Setup & Frontend

#### Days 1-2: Initialize Project

**1. Create Next.js Frontend**
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --shadcn-ui
```

**2. Install Key Dependencies**
```bash
npm install konva canvas zustand axios framer-motion
npm install -D @types/konva
```

**3. Project Structure**
```
frontend/app/
├── page.tsx                    # Home/dashboard
├── upload/page.tsx            # Upload interface
├── audit/[id]/page.tsx        # Results page
├── api/
│   └── webhooks.ts           # Webhook for async updates
└── components/
    ├── UploadForm.tsx         # File upload
    ├── AuditReport.tsx        # Results display
    └── LoadingSpinner.tsx
```

#### Days 3-5: Upload Interface

**Create Upload Component** (`components/UploadForm.tsx`):
```tsx
'use client';

import { useState } from 'react';
import { Upload } from 'lucide-react';

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/audits/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (response.ok) {
        window.location.href = `/audit/${data.audit_id}`;
      } else {
        setError(data.error || 'Upload failed');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold mb-2">DesignAudit AI</h1>
        <p className="text-gray-600 mb-8">Your AI-Powered Design Team Member</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition">
            <Upload className="mx-auto mb-4 text-gray-400" size={48} />
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="hidden"
              id="file-input"
              required
            />
            <label htmlFor="file-input" className="cursor-pointer">
              <p className="font-medium">{file?.name || 'Click to upload'}</p>
              <p className="text-sm text-gray-500">PNG, JPG, or WebP</p>
            </label>
          </div>

          {error && <p className="text-red-600 text-sm">{error}</p>}

          <button
            type="submit"
            disabled={!file || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition"
          >
            {loading ? 'Analyzing...' : 'Analyze Design'}
          </button>
        </form>
      </div>
    </div>
  );
}
```

### Week 2: Backend & Database

#### Days 1-2: FastAPI Setup

**1. Initialize Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Create Database Schema**
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- audits table
CREATE TABLE audits (
  id VARCHAR(255) PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  image_url TEXT NOT NULL,
  image_path TEXT,
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- audit_results table
CREATE TABLE audit_results (
  id SERIAL PRIMARY KEY,
  audit_id VARCHAR(255) REFERENCES audits(id),
  inspector_json JSONB,
  analyst_json JSONB,
  advisor_json JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Days 3-5: API Routes

**Create Upload Endpoint** (`routes/audits.py`):
```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
import aiofiles

router = APIRouter(prefix="/api/audits", tags=["audits"])

@router.post("/upload")
async def upload_design(file: UploadFile = File(...)):
    """Upload a design image for analysis"""
    
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Generate audit ID
    audit_id = f"audit_{uuid.uuid4().hex[:12]}"
    
    # Save file
    file_path = f"/tmp/{audit_id}_{file.filename}"
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Upload to S3
    s3_url = await upload_to_s3(file_path, audit_id)
    
    # Create audit record
    await create_audit_record(audit_id, s3_url)
    
    # Queue audit job
    from agents.tasks.audit_pipeline import run_audit_pipeline
    run_audit_pipeline.delay(audit_id, s3_url)
    
    return {
        "audit_id": audit_id,
        "status": "pending",
        "message": "Design analysis started"
    }

@router.get("/{audit_id}")
async def get_audit(audit_id: str):
    """Get audit results"""
    # Fetch from database
    audit = await get_audit_from_db(audit_id)
    
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    return audit
```

### Week 3: Inspector Agent & Integration

#### Days 1-3: Implement Inspector Agent

**Setup GPT-4 Vision API** (`agents/inspector/vision_analyzer.py`):
```python
from openai import AsyncOpenAI
import json

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_with_gpt4_vision(image_url: str):
    """Call GPT-4 Vision for design analysis"""
    
    response = await client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": VISION_SYSTEM_PROMPT  # From vision_analyzer.py
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    },
                    {
                        "type": "text",
                        "text": "Analyze this design screenshot in detail..."
                    }
                ]
            }
        ],
        max_tokens=4096
    )
    
    # Parse JSON response
    content = response.choices[0].message.content
    design_map = json.loads(content)
    
    return design_map
```

#### Days 4-5: Create Audit Pipeline Task

**Setup Celery Task** (`agents/tasks/audit_pipeline.py`):
```python
from celery import shared_task
from agents.orchestrator import AuditOrchestrator

@shared_task
def run_audit_pipeline(audit_id: str, image_url: str):
    """Celery task for async audit processing"""
    
    orchestrator = AuditOrchestrator()
    
    try:
        # Run full pipeline
        result = orchestrator.run_audit(
            image_path=None,
            image_url=image_url
        )
        
        # Save to database
        save_audit_results(audit_id, result)
        
        # Update status
        update_audit_status(audit_id, "completed")
        
    except Exception as e:
        update_audit_status(audit_id, "failed")
        log_error(audit_id, str(e))
```

### Week 4: Frontend Results Display

**Create Results Page** (`app/audit/[id]/page.tsx`):
```tsx
'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

export default function AuditPage() {
  const params = useParams();
  const auditId = params.id as string;
  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAudit = async () => {
      const response = await fetch(`/api/audits/${auditId}`);
      const data = await response.json();
      setAudit(data);
      setLoading(false);
    };

    fetchAudit();
    // Poll for updates every 2 seconds
    const interval = setInterval(fetchAudit, 2000);
    return () => clearInterval(interval);
  }, [auditId]);

  if (loading) return <div>Loading...</div>;
  if (!audit) return <div>Audit not found</div>;

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Design Audit Results</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Inspector Output */}
        <div className="lg:col-span-2">
          <h2 className="text-2xl font-bold mb-4">Design Analysis</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-auto">
            {JSON.stringify(audit.inspector, null, 2)}
          </pre>
        </div>
        
        {/* Violations Summary */}
        <div>
          <h3 className="text-xl font-bold mb-4">Issues Found</h3>
          <div className="space-y-4">
            {audit.analyst?.violations?.map((v, i) => (
              <div key={i} className="border-l-4 border-yellow-500 pl-4">
                <p className="font-bold">{v.title}</p>
                <p className="text-sm text-gray-600">{v.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
```

## Development Workflow

### Testing Inspector Agent Locally

```python
# test_inspector.py
import asyncio
from agents.inspector.vision_analyzer import VisionAnalyzer

async def test():
    analyzer = VisionAnalyzer(api_key="sk-...")
    
    # Test with real image
    result = await analyzer.analyze(
        "https://example.com/design.png"
    )
    
    print(json.dumps(result, indent=2))

asyncio.run(test())
```

### Debugging Tips

```python
# Add logging to understand the pipeline
import logging
logging.basicConfig(level=logging.DEBUG)

# Print intermediate outputs
print("Inspector output:", json.dumps(inspector_output, indent=2))
print("Analyst output:", json.dumps(analyst_output, indent=2))
print("Advisor output:", json.dumps(advisor_output, indent=2))
```

## Cost Optimization Notes

### API Costs (Estimated)
- **GPT-4 Vision**: $0.01 per image (input tokens) + $0.03 (output)
- **GPT-4 for Advisor**: $0.03 per query (input) + $0.06 (output)
- **Redis Cache**: ~$5-10/month (Upstash)
- **Database**: ~$15-25/month (Supabase)
- **S3 Storage**: ~$0.023 per GB

### Optimization Strategies
1. Cache vision outputs to avoid re-analyzing same design
2. Use Claude 3 Haiku for Advisor (cheaper than GPT-4)
3. Implement rate limiting per user
4. Compress images before uploading

## Next Phase Preparation

Once MVP is complete:
- [ ] Implement Analyst agent
- [ ] Add Advisor agent
- [ ] Build heatmap overlay visualization
- [ ] Create chat interface
- [ ] Add user authentication
- [ ] Deploy to production

