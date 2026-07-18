# 📝 Task Manager Application

A production-ready, full-stack, dockerized Task Management application built using a decoupled architecture. It features a high-performance **FastAPI** backend, a responsive **React (Vite)** frontend, and a persistent **MySQL** relational database.

---

## 🏗️ System Architecture & Workflow

The application operates across three fully isolated, interconnected networks managed entirely by Docker:

```text
  [ React Client ]  📱 Web Interface (Port 3000)
         │
         ▼ (Fetch Requests / JSON Data via REST APIs)
  [ FastAPI Server ] ⚙️ Business Logic & Routing (Port 8000)
         │
         ▼ (SQL Queries via SQLAlchemy ORM / PyMySQL)
  [ MySQL Instance ] 💾 Persistent Storage Layer (Port 3306)
```

---

## 🗄️ Database Schema & Data Models

### 1. `users` Table
Stores authenticated application users.
*   `id`: `INT`, Primary Key, Auto-Increment.
*   `name`: `VARCHAR(100)`, Non-Null. *(Added)*
*   `email`: `VARCHAR(255)`, Unique, Indexed, Non-Null.
*   `hashed_password`: `VARCHAR(255)`, Non-Null.
*   `created_at`: `TIMESTAMP`, Default: Current Timestamp.

### 2. `tasks` Table
Stores task items linked via foreign key constraints to their respective creators.
*   `id`: `INT`, Primary Key, Auto-Increment.
*   `user_id`: `INT`, Foreign Key references `users(id)`, Non-Null.
*   `title`: `VARCHAR(100)`, Non-Null.
*   `description`: `TEXT`, Nullable.
*   `due_date`: `DATE`, Non-Null.
*   `priority`: `ENUM('High', 'Medium', 'Low')`, Default: `'Medium'`.
*   `status`: `ENUM('Pending', 'Completed')`, Default: `'Pending'`.
*   `updated_at`: `TIMESTAMP`, On Update: Current Timestamp.

---

## 🔌 API Endpoints Specifications

All API payloads and responses communicate using structured JSON format.

### Authentication Endpoints

| HTTP Method | Endpoint | Description | Payload Constraints / Validation |
| :--- | :--- | :--- | :--- |
| **POST** | `/register` | Register a new account | Required: `name` (required string), `email`, `password` (min 6 chars). Unique email check. |
| **POST** | `/login` | Authenticate & get token | Required: `email`, `password`. Returns JWT or session state. |

### Task Management Endpoints (Requires Auth Header/Token)

| HTTP Method | Endpoint | Description | Payload / Path Constraints |
| :--- | :--- | :--- | :--- |
| **GET** | `/tasks` | Fetch user's task registry | Optional Query Filters: `status` (`Pending`/`Completed`). |
| **POST** | `/tasks` | Create a new task entry | Required: `title`, `due_date`. Optional: `description`, `priority`. |
| **PUT** | `/tasks/:id` | Modify an existing task item | Path: `id`. Payload: Any structural field updates or status toggle. |
| **DELETE** | `/tasks/:id` | Permanently drop a task item | Path: `id`. Restricts deletion to task owner only. |

---

## 🎨 UI Layout & User Experience Workflow

The interface is built on standard CSS/Flexbox conventions ensuring fluid scaling between compact mobile contexts and large desktop layouts. 

### 📱 Views & Interface Hierarchies
1.  **Authentication Gate (`/login` & `/register` tabs):**
    *   Unified input forms displaying proactive validation states.
    *   The `/register` pane contains an explicit input field for the user's **Full Name**.
    *   Visual indicators flag weak passwords (<6 characters) or missing values before network transmission.
2.  **Dashboard Shell (`/tasks` view):**
    *   **Header Module:** Personalization message ("Welcome back, `[User Name]`!"), navigation links, brand logo, and an intuitive "Logout" action.
    *   **Control Panel Section:** An "Add Task" triggering button, coupled with toggle chips to filter between **View All**, **Pending**, and **Completed** pools.
    *   **Task List / Grid Interface:** Chronologically sorted card layouts containing visual badges denoting Priority weights (`High` = Red, `Medium` = Orange, `Low` = Blue).
3.  **Task Interactive Cards:**
    *   Inline checkboxes to execute immediate status toggles.
    *   Dedicated action icons for triggering edit configurations and item deletion routines.

### 🔄 UX Micro-Interactions
*   **Loading State Overlays:** Global skeleton structures and spinner layouts replace interactive controls while awaiting async API resolve states.
*   **Disabled States:** Action targets and submit mechanisms enter a distinct disabled state during processing to eliminate duplicate data insertion calls.

---

## ⚙️ Local Configuration & Orchestration

### Prerequisites
*   Ensure **Docker Desktop** is running locally on your computer.

### Quick Start Deployment
Execute this command sequence inside the directory root containing this file:

```bash
# Force compile and instantiate all running application layers
docker compose up --build
```

### Access Matrix
*   **React Frontend Application Canvas:** Open [http://localhost:3000](http://localhost:3000)
*   **FastAPI Documentation / Test Suite:** Open [http://localhost:8000/docs](http://localhost:8000/docs)
*   **MySQL Server Pipeline Entry:** `localhost:3306` (Credentials outlined in `docker-compose.yml`)
