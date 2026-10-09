# ⚖️ LegalEase: AI-Powered Legal Document Generator

LegalEase is a full-stack, AI-driven legal drafting engine that generates enforceable, customizable legal contracts (NDAs, Employment Contracts, Lease Agreements) using **Google Gemini**, served via **FastAPI**, with multi-format export and financial analytics.

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (HTML/JS/CSS)                 │
│  ┌─────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │ Document     │  │ Dynamic    │  │ Preview / Edit / │  │
│  │ Type Picker  │  │ Input Form │  │ Terms / Analytics│  │
│  └──────┬──────┘  └─────┬──────┘  └────────┬─────────┘  │
│         │               │                   │            │
│         └───────┬───────┘                   │            │
│                 ▼                           │            │
│          API Calls (fetch)                  │            │
└─────────────────┬───────────────────────────┘            │
                  │ HTTP (JSON / Streams)                   │
┌─────────────────▼───────────────────────────────────────┐│
│                FastAPI Backend (Python)                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Endpoints:                                        │   │
│  │  POST /api/v1/generate   → Gemini AI Generation   │   │
│  │  POST /api/v1/preview    → Live Preview Payload    │   │
│  │  POST /api/v1/analytics  → NumPy/Matplotlib Charts │   │
│  │  POST /api/v1/export/pdf → ReportLab PDF Stream    │   │
│  │  POST /api/v1/export/docx→ python-docx Stream      │   │
│  │  POST /api/v1/export/txt → Raw Text Stream         │   │
│  │  GET  /api/v1/health     → Health Check            │   │
│  └──────┬────────────┬───────────────┬──────────────┘   │
│         │            │               │                   │
│  ┌──────▼──────┐ ┌───▼──────────┐ ┌──▼───────────────┐  │
│  │ Gemini      │ │ Export       │ │ Analytics        │  │
│  │ Service     │ │ Service      │ │ Service          │  │
│  │ (google-    │ │ (reportlab,  │ │ (numpy,          │  │
│  │  genai)     │ │  python-docx)│ │  matplotlib)     │  │
│  └─────────────┘ └──────────────┘ └──────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

| Layer             | Technology                                     |
| ----------------- | ---------------------------------------------- |
| **AI Core**       | Google Gemini API (`google-genai`)              |
| **Backend**       | Python 3.10+, FastAPI, Uvicorn, Pydantic        |
| **Doc Export**    | `reportlab` (PDF), `python-docx` (DOCX)         |
| **Analytics**     | `numpy` (calculations), `matplotlib` (charts)   |
| **Frontend**      | HTML5, Tailwind CSS, Vanilla JavaScript          |
| **Containerization** | Docker                                       |

## 📁 Project Structure

```
legalease/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app, routing, CORS
│   │   ├── config.py                # Environment & Gemini API settings
│   │   ├── schemas.py               # Pydantic models for validation
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── gemini_service.py    # Gemini prompt orchestration
│   │       ├── export_service.py    # PDF, DOCX, TXT generators
│   │       └── analytics_service.py # NumPy/Matplotlib financial analytics
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html                   # Responsive split-screen UI
│   ├── app.js                       # API integration, form logic, tabs
│   └── style.css                    # Custom styles
├── .env.example                     # Template for environment variables
├── .gitignore
└── README.md
```

## 🚀 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-team/legalease.git
cd legalease
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your Gemini API key:
# GEMINI_API_KEY="your-key-from-aistudio.google.com"
```

### 3. Install Dependencies

```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Open the App

- **Frontend UI:** http://localhost:8000/
- **API Docs (Swagger):** http://localhost:8000/docs

## 📡 API Endpoints

| Method | Endpoint              | Description                        | Request Body                  |
| ------ | --------------------- | ---------------------------------- | ----------------------------- |
| `GET`  | `/api/v1/health`       | Health check                       | —                             |
| `POST` | `/api/v1/generate`     | Generate legal document via Gemini | `{ document_type, data }`     |
| `POST` | `/api/v1/preview`      | Get live editable preview          | `{ markdown_content }`        |
| `POST` | `/api/v1/analytics`    | Get NumPy metrics + chart          | `{ document_type, data }`     |
| `POST` | `/api/v1/export/pdf`   | Download PDF                       | `{ markdown_content }`        |
| `POST` | `/api/v1/export/docx`  | Download DOCX                      | `{ markdown_content }`        |
| `POST` | `/api/v1/export/txt`   | Download TXT                       | `{ markdown_content }`        |

### Sample Request: Generate NDA

```json
{
    "document_type": "NDA",
    "data": {
        "disclosing_party": "Acme Corp",
        "receiving_party": "Beta LLC",
        "effective_date": "2026-01-15",
        "jurisdiction": "State of Delaware",
        "confidentiality_period": "3 Years"
    }
}
```

## 🐳 Docker Deployment

```bash
cd backend
docker build -t legalease-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY="your-key" legalease-backend
```

## ☁️ Deploy to Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/legalease-backend

# Deploy
gcloud run deploy legalease-backend \
    --image gcr.io/YOUR_PROJECT_ID/legalease-backend \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GEMINI_API_KEY=your-key
```

## 👥 Team

| Name              | Role        |
| ----------------- | ----------- |
| **Aafrin**        | Team Lead   |
| **ISHWARYA M**    | Developer   |
| **Shifana Jasmine** | Developer |

## 📜 License

This project was built as part of the **Google Cloud Generative AI** module on [SkillWallet](https://myskillwallet.ai).
