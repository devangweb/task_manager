
Structure of backend 
----------------------
backend/
├── main.py                 # FastAPI instance & app entry point
├── core/
│   ├── config.py           # Environment variables
│   ├── security.py         # JWT and password hashing
│   └── database.py         # SQLAlchemy engine and session
├── models/                 # SQLAlchemy Models (Database layer)
│   ├── user.py
│   └── task.py
├── schemas/                # Pydantic Models (Data validation/DTOs)
│   ├── user.py
│   └── task.py
├── repositories/           # Data Access Layer (DB queries)
│   ├── user_repo.py
│   └── task_repo.py
├── services/               # Business Logic Layer
│   ├── user_service.py
│   └── task_service.py
└── api/                    # Presentation Layer (Controllers/Routes)
    ├── dependencies.py     # get_db, get_current_user
    └── routes/
        ├── auth.py
        └── tasks.py
        
-----------------------------