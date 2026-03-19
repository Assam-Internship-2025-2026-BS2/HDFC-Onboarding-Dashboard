# Digital Onboarding Dashboard 

A full-stack, dynamic enterprise web application designed to track, visualize, and analyze digital onboarding metrics across different products, channels, regions, and segments. It features a sleek React frontend connected to a high-performance Python FastAPI backend, utilizing ClickHouse for rapid time-series analytical queries.

---

## Key Features

The platform is engineered for scale, resiliency, and deep data exploration:

- **Unified Dynamic Filtering:** A globally integrated `<Filters />` navigation bar controls the `Dashboard`, `Analysis`, `Products`, and `Customer Insights` tabs, guaranteeing a unified state and flawless cross-page analytical slices.
- **Intelligent Data Generation:** Features live data consumption completely driven by backend queries. Custom insights are mathematically generated via deterministic hashing, outputting tailored alert strings and rigorous multi-tier `Moderate`/`Critical` UI matrices based on your active product slices.
- **Backend Resiliency & Auto-Recovery:** Powered by a global HTTP Axios interceptor, the frontend automatically handles `ERR_CONNECTION_REFUSED` crashes by attempting internal retry cycles with exponential backoff, ensuring uninterrupted user experience even during API turbulence.
- **Deep Dark Mode Architecture:** Fully integrated CSS-driven theme toggling. Hand-crafted styling ensures footers, headers, cards, and textual data perfectly transition between crisp light themes and deep graphite dark modes without rendering anomalies.
- **Real-World Date Computation:** Advanced backend mapping natively handles complex relative timeframe filters (such as `Today` or `Last 7 Days`), parsing mathematically sound zero-values or accurate bounds against the ClickHouse mock dataset.
- **Responsive Chart Visualizations:** The Recharts integration throughout `<DashboardGraphics />`, `<Analysis />`, and embedded KPI sparklines enforces graceful Flexbox resizing across all devices.

---

## Project Architecture & Workflow

The project follows a modern decoupled architecture where the Frontend acts as a presentation layer, while the Backend handles all mathematical modeling, delta calculations, and SQL extractions. 

### Data Flow Workflow
1. **User Interaction:** The user chooses a filter from the dropdowns (e.g., `Today`, `Credit Card`, `Mobile App`).
2. **API Request:** React triggers an asynchronous `fetch` request, generating a tailored JSON payload (e.g., `?time_range=Today&comparison=V/S+Yesterday`).
3. **Backend Routing:** FastAPI intercepts the request securely via `backend/app/routers/executive_router.py`.
4. **Logic & Calculation:** The Service layer determines the exact `datetime` ranges, calculates the mathematical differences between the current and previous period, aggregates SLA breaches, and determines health statuses.
5. **Database Execution:** The service dynamically injects the parameters into raw ClickHouse SQL code located in `backend/app/queries/dashboard_queries.py`.
6. **Schema Validation:** The ClickHouse arrays are fed into rigorous Pydantic validators (`backend/app/schemas/executive_schema.py`) to ensure perfect type-safety before transmission.
7. **Frontend Mapping:** The structured JSON arrives successfully back in React, distributing the data across components like `<KPIStrip />`, `<Matrix />`, and the `<DashboardGraphics />` Recharts engine.

---

## Directory Structure

### Frontend (`/frontend`)
Powered by **React** and **Vite** running on Port `5173`.
- **`src/pages/`**: The core application views (`Dashboard.jsx`, `Analysis.jsx`, `Products.jsx`, `CustomerInsights.jsx`). Manages the global state and API fetching.
- **`src/ui/`**: Reusable visual components including the Recharts implementations, KPI SLA strips, Drop-off matrices, and global filter navigation.
- **`src/services/api.js`**: The central Axios networking hub equipped with auto-retry resilience.

### Backend (`/backend`)
Powered by Python **FastAPI** running on Port `8000`.
- **`app/routers/`**: Exposed API endpoints mirroring physical URLs.
- **`app/services/` (The Core Logic Engine)**: Computes trend directions, translates text filters into `timedelta` ranges, evaluates SLA thresholds, and combines SQL outputs.
- **`app/queries/`**: The raw ClickHouse execution strings.
- **`scripts/`**: Python mock factory generators capable of pushing hundreds of thousands of algorithmic rows into the local ClickHouse infrastructure.

---

## Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- ClickHouse (Local Server or Cloud)

### 1. Database Setup
Ensure ClickHouse is running locally. The `.env` variables located at `backend/app/core/config.py` default to `localhost:8123`.

### 2. Backend Dependencies
Navigate to the `backend` folder and create a virtual environment:
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the core Python packages:
```bash
pip install -r requirements.txt
```

Generate the Database Schema, load the mock algorithm rows, and build the materialized views. *(Note: this script regenerates the dataset backward from the exact moment of execution)*:
```bash
python scripts/generate_large_data.py
python scripts/load_data.py
python setup_mv.py
```

Run the API Node Development Server:
```bash
python -m uvicorn main:app --reload --port 8000
```

### 3. Frontend Dependencies
Open a second terminal, navigate to the `frontend` folder, and install the NPM packages:
```bash
cd frontend
npm install
```

Start the Vite React Development Server:
```bash
npm run dev
```

Navigate to `http://localhost:5173/` to view the fully deployed Dashboard mapped securely to your ClickHouse backend!
