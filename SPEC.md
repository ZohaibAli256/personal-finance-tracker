# Personal Finance Tracker — Project Specification

## Project Overview

A full-stack personal finance tracker that lets users add, edit, and delete income/expense transactions, categorize them, view a dashboard with summary cards (total income, total expenses, current balance), visualize spending by category with a pie/donut chart, and filter/search their transaction history. The backend is a FastAPI REST API backed by Neon PostgreSQL via SQLAlchemy, and the frontend is a Next.js 16 app using TypeScript, Tailwind CSS, Recharts for charts, and Server Actions to communicate with the API.
Each part of each phase should be executed one by one and at the end of each phase, a message must be displayed confirming whether it should be commited and pushed to git. After each step of each phase is completed, it should be crossed off.

### Project Frontend Layout
The font for all the headings/titles should be Gill Sans MT and the font for all the other text should be Trebuchet MS
All the money values should be in Pakistani Rupees and the format for the commas should be: 1,00,00,000/- (the "/-" at the end of the value must be included)
All the windows should be rectangular with a very slight curve around the edges (leaving a little bit of space around the information it needs to display)
#### Overwiew Window
When the page is opened, it should only show one window (titled the Overview Window) in the middle of the page where you are shown your Income, Expenses, and Remaining Balance (in that order)
#### Transactions Window
Below the Overwiew window, there should be a dropdown option labeled "Transactions" which should show the options "Add Transaction", "Edit Transaction", "Delete Transaction", and "View Transaction History" when it is clicked. Upon clicking, a window should open below the Overwiew Window (called the Options Window) and the dropdown window should adjust so that the new window fits the middle of the page with a smooth animation
#### Transactions Detail Window
When one of the buttons is pressed from the Options Window dropdown menu, a new window should open on the right side of the page (called the "Transactions Detail" window) with a smooth animation. The page should split so that the Overwiew and Options windows take up as much space as is needed (and no more) on the left, and, the rest of the page is given to the "Transactions Detail" window. If there is space remaining after all windows are beign displayed, leave equal empty space on the left and right side of the page. In the "Transactions Deatil" window, the transactions should be sorted like a stack (the earliest transactions should be displayed at the bottom and the newest transactions should be displayed at the top)
On the top of the Transactions Detail window, there should be a button labelled "Add Transaction". When the "Add Transaction" button is pressed, the date for the new transaction should automatically be the current date, however, the option to change it to a previous date before the transaction is added to the stack MUST be available along with the option to categorise it
On the right side of each transaction, there should be a button (symbolised by a triple dot) which should open a dropdown menu allowing you to categorise each transaction, edit it, or delete it
Each transaction should be split into 3 parts; the description of the transaction (aligned to the left side), the amount of the transaction (aligned to the centre on the right side), and the category of the transaction (displayed right below the description) in a small font with a colour symbolising its type (e.g. one colour for food, another for transport, etc.)
#### Transactions Detail Layout
In the Transactions Detail window, there should be a title for each year (which can be minimised) under which there should be a subtitle for each month (which can also be minimised). At the end of each month, the total monthly expenditure should be displayed 
#### Visual Display Window
Above the transaction histotry window, there should be a Visual Display window which should pop up from behind the Transactions Detail window with a smooth animation. Here, there should be 2 donut charts; the left one displaying expenses in the past 30 days and the right one displaying all expenses. Both should show categorised expenses (e.g. 50% spent on food, 20% spent on travel etc.) with a specific colour for each category of expense (which should be consistent across both charts)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | FastAPI (Python) |
| Package Manager (Python) | uv |
| ORM | SQLAlchemy |
| Database | Neon PostgreSQL (cloud) |
| ASGI Server | Uvicorn |
| Frontend Framework | Next.js 16 with Turbopack |
| Language (Frontend) | TypeScript |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Frontend–Backend Bridge | Next.js Server Actions |
| Testing (Backend) | pytest |
| Testing (Frontend) | Vitest |

## Project Structure

```
personal-finance-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app, CORS, router includes
│   │   ├── database.py      # SQLAlchemy engine, SessionLocal, Base
│   │   ├── models.py        # SQLAlchemy ORM model (Transaction)
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   └── routers/
│   │       └── transactions.py  # All /transactions endpoints + /summary
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py      # Test DB fixture, test client
│   │   └── test_transactions.py
│   ├── .env                 # DATABASE_URL (git-ignored)
│   ├── .env.example
│   ├── pyproject.toml
│   └── main.py              # (existing stub — will be replaced)
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx          # Dashboard page
│   │   ├── transactions/
│   │   │   └── page.tsx      # Transactions list page
│   │   └── transactions/new/
│   │       └── page.tsx      # Add/Edit transaction page
│   ├── components/
│   │   ├── SummaryCards.tsx
│   │   ├── CategoryChart.tsx
│   │   ├── TransactionList.tsx
│   │   ├── TransactionForm.tsx
│   │   ├── TransactionFilters.tsx
│   │   └── Navbar.tsx
│   ├── lib/
│   │   ├── types.ts          # Shared TypeScript types
│   │   └── actions.ts        # Server Actions (fetch/create/update/delete)
│   ├── __tests__/
│   │   ├── SummaryCards.test.tsx
│   │   ├── TransactionList.test.tsx
│   │   └── TransactionForm.test.tsx
│   ├── .env.local            # NEXT_PUBLIC_API_URL (git-ignored)
│   ├── .env.example
│   └── ...existing config files
├── .gitignore
├── SPEC.md                   # ← This file
└── README.md
```

## Database Model — `transactions`

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key, auto-increment |
| description | String(255) | NOT NULL |
| amount | Float | NOT NULL |
| type | String(10) | NOT NULL — `"income"` or `"expense"` |
| category | String(50) | NOT NULL — one of: food, transport, shopping, bills, salary, freelance, entertainment, health, education, other |
| date | Date | NOT NULL |
| created_at | DateTime | Server default = now() |

## API Endpoints

| Method | Path | Description |
|--------|------|------------|
| GET | `/transactions` | List all transactions (supports query params: `type`, `category`, `search`, `sort`) |
| POST | `/transactions` | Create a new transaction |
| GET | `/transactions/{id}` | Get a single transaction by ID |
| PUT | `/transactions/{id}` | Update a transaction |
| DELETE | `/transactions/{id}` | Delete a transaction |
| GET | `/summary` | Return `{ total_income, total_expenses, balance, category_breakdown }` |

---

## Task List

### Phase 1 — Backend

#### 1.1 Database Setup
- [x] Create `backend/app/__init__.py`
- [x] Create `backend/app/database.py` — SQLAlchemy engine, `SessionLocal`, `Base`, using `DATABASE_URL` from env
- [x] Create `backend/.env.example` with placeholder `DATABASE_URL`
- [x] Add `python-dotenv`, `sqlalchemy`, `psycopg2-binary` to project dependencies via `uv add`

#### 1.2 ORM Model
- [x] Create `backend/app/models.py` — `Transaction` model with all columns (id, description, amount, type, category, date, created_at)
- [x] Add enum validation for `type` (income/expense) and `category` (food, transport, shopping, bills, salary, freelance, entertainment, health, education, other)

#### 1.3 Pydantic Schemas
- [x] Create `backend/app/schemas.py` — `TransactionCreate` schema (request body for POST/PUT)
- [x] Add `TransactionResponse` schema (response model with `id` and `created_at`)
- [x] Add `SummaryResponse` schema (total_income, total_expenses, balance, category_breakdown)

#### 1.4 API Endpoints — Transactions CRUD
- [x] Create `backend/app/routers/__init__.py`
- [x] Create `backend/app/routers/transactions.py` with APIRouter
- [x] Implement `GET /transactions` — list all, with optional query params (`type`, `category`, `search`)
- [x] Implement `POST /transactions` — create a new transaction, return 201
- [x] Implement `GET /transactions/{id}` — get by ID, return 404 if not found
- [x] Implement `PUT /transactions/{id}` — update by ID, return 404 if not found
- [x] Implement `DELETE /transactions/{id}` — delete by ID, return 404 if not found

#### 1.5 Summary Endpoint
- [x] Implement `GET /summary` — compute total_income, total_expenses, balance, and category_breakdown from DB

#### 1.6 App Entrypoint & CORS
- [x] Replace `backend/main.py` stub with FastAPI app that imports from `backend/app/main.py`
- [x] Create `backend/app/main.py` — FastAPI instance, CORS middleware (allow localhost:3000), include transaction router
- [x] Add table creation on startup (`Base.metadata.create_all`)
- [x] Verify backend starts with `uv run uvicorn app.main:app --reload` from `backend/`

#### 1.7 Manual API Smoke Test
- [x] Test all 6 endpoints via Swagger UI (`/docs`) or curl to confirm they work against Neon DB

---

### Phase 2 — Frontend

#### 2.1 Project Configuration
- [x] Install additional dependencies: `npm install recharts`
- [x] Install dev dependencies: `npm install -D vitest @testing-library/react @testing-library/jest-dom @vitejs/plugin-react jsdom`
- [x] Create `frontend/.env.example` with `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [x] Create `frontend/.env.local` with the actual API URL (git-ignored)

#### 2.2 Shared Types & Server Actions
- [x] Create `frontend/lib/types.ts` — `Transaction`, `TransactionCreate`, `Summary` TypeScript interfaces
- [x] Create `frontend/lib/actions.ts` — Server Action: `getTransactions(filters?)` → fetch GET `/transactions`
- [x] Add Server Action: `createTransaction(data)` → fetch POST `/transactions`
- [x] Add Server Action: `updateTransaction(id, data)` → fetch PUT `/transactions/{id}`
- [x] Add Server Action: `deleteTransaction(id)` → fetch DELETE `/transactions/{id}`
- [x] Add Server Action: `getSummary()` → fetch GET `/summary`

#### 2.3 Layout & Navigation
- [x] Create `frontend/components/Navbar.tsx` — nav links: Dashboard, Transactions, Add Transaction
- [x] Update `frontend/app/layout.tsx` — include Navbar, set page title, global font/styles

#### 2.4 Dashboard Page
- [x] Create `frontend/components/SummaryCards.tsx` — three cards: Total Income, Total Expenses, Balance
- [x] Create `frontend/components/CategoryChart.tsx` — Recharts pie/donut chart showing category breakdown
- [x] Update `frontend/app/page.tsx` — Dashboard page that calls `getSummary()` and renders SummaryCards + CategoryChart

#### 2.5 Transactions List Page
- [x] Create `frontend/components/TransactionFilters.tsx` — filter by type, category; search by description
- [x] Create `frontend/components/TransactionList.tsx` — table/list of transactions with edit/delete actions
- [x] Create `frontend/app/transactions/page.tsx` — page that calls `getTransactions()`, renders filters + list
- [x] Wire up delete button to `deleteTransaction()` Server Action with confirmation

#### 2.6 Add / Edit Transaction Page
- [x] Create `frontend/components/TransactionForm.tsx` — form with fields: description, amount, type (dropdown), category (dropdown), date
- [x] Create `frontend/app/transactions/new/page.tsx` — renders TransactionForm, calls `createTransaction()` on submit
- [x] Add edit mode: `frontend/app/transactions/[id]/edit/page.tsx` — loads existing transaction, pre-fills form, calls `updateTransaction()` on submit

#### 2.7 Styling & Polish
- [x] Style Navbar with Tailwind (responsive, active link indicator)
- [x] Style SummaryCards with Tailwind (grid layout, colored accents for income/expense/balance)
- [x] Style TransactionList table with Tailwind (striped rows, hover states, responsive)
- [x] Style TransactionForm with Tailwind (form layout, input focus states, submit button)
- [x] Style TransactionFilters with Tailwind (inline filters, search input)
- [x] Add loading states / skeletons for async data fetching
- [x] Add empty states (no transactions yet message)

---

### Phase 3 — Integration

#### 3.1 End-to-End Data Flow
- [x] Verify: Creating a transaction on frontend persists to Neon DB and appears in list
- [x] Verify: Editing a transaction updates the DB and reflects on frontend
- [x] Verify: Deleting a transaction removes from DB and disappears from frontend
- [x] Verify: Dashboard summary cards show correct totals from DB
- [x] Verify: Category chart renders correct breakdown from DB
- [x] Verify: Filters and search work correctly against backend query params

#### 3.2 Error Handling
- [x] Add error handling in Server Actions (try/catch, user-friendly error messages)
- [x] Display error messages on frontend when API calls fail
- [x] Handle 404 gracefully on edit page (transaction not found)

---

### Phase 4 — Testing

#### 4.1 Backend Tests (pytest)
- [x] Create `backend/tests/__init__.py`
- [x] Create `backend/tests/conftest.py` — test database setup (SQLite in-memory), TestClient fixture
- [x] Write test: `POST /transactions` creates a transaction successfully
- [x] Write test: `POST /transactions` with invalid data returns 422
- [x] Write test: `GET /transactions` returns list of transactions
- [x] Write test: `GET /transactions?type=income` filters correctly
- [x] Write test: `GET /transactions?search=...` searches correctly
- [x] Write test: `GET /transactions/{id}` returns the correct transaction
- [x] Write test: `GET /transactions/{id}` with nonexistent ID returns 404
- [x] Write test: `PUT /transactions/{id}` updates a transaction
- [x] Write test: `PUT /transactions/{id}` with nonexistent ID returns 404
- [x] Write test: `DELETE /transactions/{id}` deletes a transaction
- [x] Write test: `DELETE /transactions/{id}` with nonexistent ID returns 404
- [x] Write test: `GET /summary` returns correct totals and category breakdown
- [x] Run all backend tests and confirm they pass: `cd backend && uv run pytest -v`

#### 4.2 Frontend Tests (Vitest)
- [x] Configure Vitest in `frontend/vitest.config.ts`
- [x] Create `frontend/__tests__/SummaryCards.test.tsx` — renders income, expense, balance values
- [x] Create `frontend/__tests__/TransactionList.test.tsx` — renders list of transactions, shows empty state
- [x] Create `frontend/__tests__/TransactionForm.test.tsx` — renders form fields, validates required inputs
- [x] Run all frontend tests and confirm they pass: `cd frontend && npx vitest run`

---

### Phase 5 — Submission Prep

- [ ] Create `README.md` in project root with: project description, setup instructions, screenshots, tech stack
- [ ] Create `backend/.env.example` and `frontend/.env.example` with placeholder values
- [ ] Verify `.gitignore` covers `.env`, `.env.local`, `node_modules/`, `.venv/`, `__pycache__/`
- [ ] Confirm all SPEC.md tasks are checked off
- [ ] Confirm clean `git status` (no uncommitted sensitive files)
- [ ] Final commit with meaningful message
