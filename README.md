# Digital Onboarding Dashboard 

A full-stack, dynamic web application designed to track, visualize, and analyze digital onboarding metrics across different products, channels, regions, and segments. It features a sleek React frontend connected to a high-performance Python FastAPI backend, utilizing ClickHouse for rapid time-series analytical queries.

---

## Project Architecture & Workflow

The project follows a modern decoupled architecture where the Frontend acts as a presentation layer, while the Backend handles all mathematical modeling, delta calculations, and SQL extractions. 

### 1. Data Flow Workflow
1. **User Interaction:** The user chooses a filter from the dropdowns (e.g., `Today`, `Credit Card`, `Mobile App`) inside `frontend/src/ui/Filters.jsx`.
2. **API Request:** React triggers an asynchronous `fetch` request using `useEffect` inside `Dashboard.jsx`, generating a payload (e.g., `?time_range=Today&comparison=V/S+Yesterday`).
3. **Backend Routing:** FastAPI receives the request at `backend/app/routers/executive_router.py`.
4. **Logic & Calculation:** The Router passes the variables into `backend/app/services/executive_service.py`. This file determines the exact `datetime` ranges, calculates the mathematical differences between the current and previous period, aggregates SLA breaches, and determines health statuses.
5. **Database Execution:** The service dynamically injects the parameters into raw ClickHouse SQL code located in `backend/app/queries/dashboard_queries.py`.
6. **Schema Validation:** The ClickHouse SQL arrays are fed into Pydantic validators (`backend/app/schemas/executive_schema.py`) to ensure perfect typing and JSON formatting before being shipped out.
7. **Frontend Mapping:** The structured JSON arrives successfully back at `Dashboard.jsx`, distributing the data across components like `<KPIStrip />`, `<Matrix />`, and the `<DashboardGraphics />` Recharts engine.

---

## Directory Structure & Core Logic

### Frontend (`/frontend`)
Powered by **React** and **Vite**.
- **`src/pages/Dashboard.jsx`**: The main Hub. Manages the global state (`filters`, `data`, `matrix`) and handles fetching from the API.
- **`src/pages/Analysis.jsx`**: The secondary page. Note: **This page currently utilizes hardcoded mock data** (`productData` dictionary) and does not map to the database.
- **`src/ui/`**: Reusable visual components.
  - `DashboardGraphics.jsx` - Renders the Recharts Area Chart (Trend Data) and Pie Chart (Channel Origin) dynamically mapped to the SQL aggregation.
  - `KPIStrip.jsx` & `KPITile.jsx` - Processes the 4 colored SLA & Pipeline grid blocks.
  - `Matrix.jsx` - Evaluates strict percentage thresholds, colorizing the Drop-off matrix into Green, Yellow, Pink, and Red pills.
  - `Filters.jsx` - The pill-styled dropdown navigation system.

### Backend (`/backend`)
Powered by Python **FastAPI**.
- **`app/routers/`**: Exposed API endpoints mirroring physical URLs (`executive_router.py`).
- **`app/services/` (The Core Logic Engine)**: 
  - `executive_service.py`: Computes trend directions (UP/DOWN), converts text inputs like "Last 7 Days" into actual Python `timedelta` ranges, evaluates SLA thresholds, and combines multiple SQL outputs into a singular JSON master format.
  - `stage_dropoff_service.py`: Handles pure mathematical drop-off mapping. 
- **`app/queries/dashboard_queries.py`**: The raw ClickHouse execution strings containing rigorous `SUM()`, `AVG()`, and `GROUP BY` logic isolated for execution.
- **`app/schemas/executive_schema.py`**: Pydantic Type-safety files. If a python variable isn't whitelisted here (e.g., `trend_data: List[Dict]`), FastAPI will instantly drop it from the final React delivery package.
- **`scripts/`**: Python generators holding the mock factory script to push 200,000 algorithmic rows into local ClickHouse infrastructure.

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

Generate the Database Schema and load the mock algorithm rows:
```bash
python scripts/generate_large_data.py
python scripts/load_data.py
```

Run the API Node Development Server:
```bash
python -m uvicorn main:app --reload
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

Navigate to `http://localhost:5173/` to view the fully deployed Dashboard mapped securely to the ClickHouse backend!
