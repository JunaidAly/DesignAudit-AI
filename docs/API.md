# DesignAudit AI - API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints require JWT bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Audit Endpoints

### 1. Upload Design for Analysis

**Endpoint:** `POST /audits/upload`

**Description:** Upload a design screenshot to initiate an audit

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file` (File, required): PNG, JPG, or WebP image (max 10MB)

**Response (200 OK):**
```json
{
  "audit_id": "audit_a1b2c3d4",
  "status": "pending",
  "created_at": "2024-01-29T10:00:00Z",
  "message": "Design analysis started"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid file type. Supported: PNG, JPG, WebP"
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/audits/upload \
  -H "Authorization: Bearer token_here" \
  -F "file=@design.png"
```

---

### 2. Get Audit Results

**Endpoint:** `GET /audits/{audit_id}`

**Description:** Retrieve completed audit results

**Path Parameters:**
- `audit_id` (string, required): The audit ID from upload response

**Response (200 OK) - Pending:**
```json
{
  "id": "audit_a1b2c3d4",
  "status": "pending",
  "created_at": "2024-01-29T10:00:00Z"
}
```

**Response (200 OK) - Completed:**
```json
{
  "id": "audit_a1b2c3d4",
  "status": "completed",
  "created_at": "2024-01-29T10:00:00Z",
  "updated_at": "2024-01-29T10:02:30Z",
  
  "inspector": {
    "layout": {
      "grid_system": "12-column",
      "page_dimensions": {"width": 1440, "height": 900},
      "viewport_type": "desktop"
    },
    "components": [
      {
        "id": "button-cta",
        "type": "button",
        "position": {"x": 400, "y": 300},
        "dimensions": {"width": 200, "height": 50},
        "content": "Get Started",
        "style": {
          "background_color": "#007AFF",
          "text_color": "#FFFFFF",
          "font_size": 16,
          "border_radius": 6
        }
      }
    ],
    "color_palette": {
      "primary": ["#007AFF"],
      "secondary": ["#5AC8FA"],
      "neutral": ["#FFFFFF", "#F2F2F7", "#333333"],
      "accent": ["#FF6B6B"]
    },
    "typography": {
      "fonts_used": ["SF Pro Display"],
      "heading_sizes": [32, 24, 20],
      "body_size": 16,
      "line_heights": [1.2, 1.5, 1.6]
    }
  },

  "analyst": {
    "total_violations": 5,
    "by_severity": {
      "critical": [],
      "high": [
        {
          "id": "a11y_contrast_button",
          "category": "accessibility",
          "severity": "high",
          "title": "Insufficient Color Contrast",
          "description": "Text contrast ratio is 3.8:1, but WCAG AA requires 4.5:1",
          "affected_elements": ["button-cta"],
          "guideline_reference": "WCAG 2.1 AA 1.4.3",
          "suggestion": "Increase contrast by darkening text"
        }
      ],
      "medium": [...],
      "low": [...]
    },
    "by_category": {
      "accessibility": [...],
      "spacing": [...],
      "typography": [...]
    }
  },

  "advisor": {
    "summary": "Overall strong design with good visual hierarchy. Main improvements needed in accessibility and spacing consistency.",
    "detailed_feedback": "Your design demonstrates professional execution with a cohesive color scheme...",
    "improvements": [
      {
        "area": "Accessibility",
        "issue": "Text contrast below WCAG AA standard",
        "impact": "Affects 8% of population with visual impairments",
        "recommendation": "Increase contrast from #666 to #333",
        "priority": "high",
        "example": "Gray button labels are hard to read"
      }
    ],
    "quick_wins": [
      "Fix button contrast (2 minutes)",
      "Increase button size to 44x44px (5 minutes)",
      "Standardize spacing to 8px grid (30 minutes)"
    ],
    "resources": [
      {
        "title": "WCAG 2.1 Contrast Requirements",
        "url": "https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html",
        "type": "standard",
        "reason": "Understand exact contrast standards"
      }
    ],
    "next_steps": [
      "1. Fix accessibility issues (1 hour)",
      "2. Standardize spacing (2 hours)",
      "3. Run final accessibility check (30 minutes)"
    ]
  }
}
```

**Response (404 Not Found):**
```json
{
  "error": "Audit not found"
}
```

**curl Example:**
```bash
curl http://localhost:8000/api/audits/audit_a1b2c3d4 \
  -H "Authorization: Bearer token_here"
```

---

### 3. List User Audits

**Endpoint:** `GET /audits`

**Description:** Get all audits for the current user

**Query Parameters:**
- `limit` (integer, optional): Results per page (default: 20)
- `offset` (integer, optional): Pagination offset (default: 0)
- `status` (string, optional): Filter by status (pending|completed|failed)

**Response (200 OK):**
```json
{
  "total": 42,
  "limit": 20,
  "offset": 0,
  "audits": [
    {
      "id": "audit_a1b2c3d4",
      "status": "completed",
      "created_at": "2024-01-29T10:00:00Z",
      "violation_count": 5,
      "critical_count": 0,
      "high_count": 2
    }
  ]
}
```

**curl Example:**
```bash
curl "http://localhost:8000/api/audits?limit=10&status=completed" \
  -H "Authorization: Bearer token_here"
```

---

## Chat Endpoints

### 4. Ask Follow-up Question

**Endpoint:** `POST /audits/{audit_id}/chat`

**Description:** Ask the AI advisor a question about the audit

**Path Parameters:**
- `audit_id` (string, required): The audit ID

**Request Body:**
```json
{
  "question": "How do I implement the contrast fix you suggested?"
}
```

**Response (200 OK):**
```json
{
  "answer": "To fix the contrast issue, you can either darken the text color or lighten the background. The easiest approach is to change your button text color from #666666 (gray) to #333333 (dark gray). This will increase the contrast ratio from 3.8:1 to 7.2:1, well above the WCAG AA requirement of 4.5:1.\n\nIn your CSS: color: #333333; or adjust your component's text color prop.",
  "sources": [
    "WCAG 2.1 AA 1.4.3",
    "Audit Inspector Analysis"
  ]
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/audits/audit_a1b2c3d4/chat \
  -H "Authorization: Bearer token_here" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I fix accessibility issues?"}'
```

---

## Authentication Endpoints

### 5. Register

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "user_id": "user_123",
  "email": "user@example.com",
  "token": "eyJhbGc..."
}
```

---

### 6. Login

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user_id": "user_123",
  "email": "user@example.com",
  "token": "eyJhbGc...",
  "expires_in": 86400
}
```

---

## WebSocket Events (Real-time Updates)

**Endpoint:** `WS /ws/audit/{audit_id}`

**Description:** WebSocket connection for real-time audit progress

**Events:**

```javascript
// Connect
const ws = new WebSocket('ws://localhost:8000/ws/audit/audit_a1b2c3d4');

// Listen for status updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  // {
  //   "type": "status_update",
  //   "status": "inspecting",
  //   "progress": 33
  // }
  
  // {
  //   "type": "status_update",
  //   "status": "analyzing",
  //   "progress": 66
  // }
  
  // {
  //   "type": "completed",
  //   "result": { ...audit_result }
  // }
};
```

---

## Error Handling

### Error Response Format

All error responses follow this format:

```json
{
  "error": "Error message",
  "status_code": 400,
  "timestamp": "2024-01-29T10:00:00Z"
}
```

### Common Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Audit retrieved |
| 201 | Created | New audit created |
| 400 | Bad Request | Invalid file type |
| 401 | Unauthorized | Missing/invalid token |
| 404 | Not Found | Audit doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal error |

---

## Rate Limiting

- **Free tier:** 10 audits/hour per user
- **Pro tier:** 100 audits/hour per user
- **Enterprise:** Unlimited

Rate limit information is returned in headers:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 5
X-RateLimit-Reset: 1704067200
```

---

## Code Examples

### Python (requests)
```python
import requests

# Upload
with open('design.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/audits/upload',
        files={'file': f},
        headers={'Authorization': f'Bearer {token}'}
    )
    audit_id = response.json()['audit_id']

# Get results
response = requests.get(
    f'http://localhost:8000/api/audits/{audit_id}',
    headers={'Authorization': f'Bearer {token}'}
)
results = response.json()
```

### JavaScript (fetch)
```javascript
// Upload
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('/api/audits/upload', {
  method: 'POST',
  body: formData,
  headers: {'Authorization': `Bearer ${token}`}
});

const {audit_id} = await uploadResponse.json();

// Poll for results
let audit = null;
while (audit?.status !== 'completed') {
  const response = await fetch(`/api/audits/${audit_id}`, {
    headers: {'Authorization': `Bearer ${token}`}
  });
  audit = await response.json();
  await new Promise(r => setTimeout(r, 1000));
}
```

### cURL (command line)
```bash
# Upload
curl -X POST http://localhost:8000/api/audits/upload \
  -H "Authorization: Bearer token" \
  -F "file=@design.png"

# Get results (polling)
for i in {1..30}; do
  curl http://localhost:8000/api/audits/audit_123 \
    -H "Authorization: Bearer token"
  sleep 2
done
```

---

## Interactive API Explorer

FastAPI automatically generates interactive API documentation at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Use these to test all endpoints in your browser.

