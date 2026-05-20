# AuditFlow Pro

AuditFlow Pro is a comprehensive, centralized platform for auditors and financial professionals. It allows you to integrate with various accounting platforms (Zoho Books, Tally Prime) and government portals (GST Portal, Income Tax) to pull financial data into one unified dashboard, enabling powerful data reconciliation and analytics.

## Project Structure

This is a monorepo containing both the frontend and backend applications.

- `/backend` - FastAPI Python backend serving the REST API.
- `/frontend` - React + Vite frontend built with Tailwind CSS.

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- MongoDB (Running locally on default port `27017` or a MongoDB Atlas URI)

---

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables:
```bash
cp .env.example .env
```
Make sure your MongoDB is running locally, or update the `MONGODB_URL` inside `.env` to point to your cloud database. By default, the application runs in Mock Data mode (`USE_MOCK_DATA=true`) so you can test connections and syncing without needing real external API keys.

Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*The backend API will be available at http://localhost:8000*
*API Documentation (Swagger UI) is available at http://localhost:8000/docs*

---

### 2. Frontend Setup

Open a new terminal window and navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
*The frontend application will be available at http://localhost:5173*

## 💡 Key Features

- **Authentication:** Secure JWT-based authentication system.
- **Platform Integrations:** Framework to connect external accounts (Zoho, Tally, GST) via their respective APIs.
- **Data Synchronization:** Unified data pipeline to fetch and normalize external financial records into a standard format.
- **Reconciliation Engine:** Compare different data sources (e.g., Accounting Software vs. Government Filings) to highlight discrepancies and missing records.
- **Mock Mode:** Test all features instantly without requiring live production API access from third parties.
