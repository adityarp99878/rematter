# ReMater

**ReMater** is an AI-powered marketplace for recovered construction materials. It helps construction teams assess surplus materials, find viable reuse opportunities, estimate value and logistics, and measure circularity impact.

## What it does

- Upload and analyze material photos with a computer-vision workflow.
- Create material listings and reuse requirements.
- Match available materials to suitable projects.
- Estimate pricing, logistics, and environmental impact.
- Generate material passports and track verification and transactions.
- Explore a dashboard, marketplace, notifications, and circularity metrics.

## Technology

| Area | Stack |
| --- | --- |
| Web app | Next.js 16, React 19, TypeScript, Tailwind CSS |
| API | FastAPI, Pydantic, SQLAlchemy / SQLModel |
| Data | SQLite by default; PostgreSQL supported |
| AI & vision | Configurable LLM endpoint and optional YOLO model |

## Project structure

```text
remater/
├── backend/                 # FastAPI API, database models, agents, and vision services
│   ├── app/api/             # Materials, matches, pricing, logistics, impact, and more
│   ├── app/agents/          # Assessment, matching, pricing, logistics, and impact agents
│   └── requirements.txt
├── frontend/                # Next.js application
│   ├── app/                 # Dashboard, marketplace, scanner, requirements, and impact views
│   └── package.json
├── .env.example             # Environment-variable template
└── docker-compose.yml        # Service configuration reference
```

## Run locally

### Prerequisites

- Python 3.9 or later
- Node.js 20 or later

### 1. Configure environment variables

From the project root, copy the template and update any values you need:

```powershell
Copy-Item .env.example .env
```

`DEMO_MODE=true` lets the API populate demo data. The app uses SQLite by default, so no database service is required to get started.

### 2. Start the API

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`; interactive API documentation is at `http://localhost:8000/docs`.

### 3. Start the web app

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

## Configuration

See [`.env.example`](.env.example) for all configuration values. Key optional settings include:

- `DATABASE_URL` — SQLite or PostgreSQL connection string.
- `LLAMA_API_KEY`, `LLAMA_MODEL`, and `LLAMA_BASE_URL` — LLM provider configuration.
- `YOLO_MODEL_PATH` — path to a compatible model file when using object detection.
- `MAPS_API_KEY` — maps provider key for logistics features.

Never commit `.env` files, uploaded images, local databases, or model weights. They are excluded by `.gitignore`.

## API overview

The FastAPI service exposes endpoints for health checks, materials, requirements, matching, pricing, logistics, impact, verification, transactions, dashboard metrics, and notifications. Browse the complete, live schema at `/docs` after starting the API.

## Tests

From `backend` with the virtual environment active:

```powershell
pytest
```

## License

Add a license file before publishing if you want to define how others may use this project.
