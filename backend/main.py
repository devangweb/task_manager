from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import os
from core.database import engine, Base
from api.routes import auth, tasks

# This automatically generates the MySQL tables based on your models
# Be sure all models are imported before this line if you add more
import models.user 
import models.task
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication endpoints"},
        {"name": "Tasks", "description": "Task management endpoints"},
    ]
)

# Include the routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Enable CORS with dynamic origins for development and production
allowed_origins = [
    "http://localhost:5173",      # Local React dev server (Vite)
    "http://localhost:3000",      # Local React dev server (traditional)
    "http://localhost:8000",      # Local FastAPI dev
]

# Add production frontend URL if available
frontend_domain = os.getenv("REACT_APP_API_URL")
if frontend_domain:
    # REACT_APP_API_URL is the backend URL, so get the frontend from environment or construct it
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        allowed_origins.append(frontend_url)
    # Also allow requests from Railway's frontend service domain
    if "railway.app" in frontend_domain:
        # Extract domain and add it
        backend_domain = frontend_domain.replace("http://", "").replace("https://", "")
        allowed_origins.append(f"https://{backend_domain}")

# Accept any Railway domain in production (more permissive but safe for internal Railway domains)
allowed_origins.extend([
    "https://frontend-production-e2459.up.railway.app",  # Your specific frontend
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI schema to configure OAuth2 security
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Task Manager API",
        version="1.0.0",
        description="Task management API with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token obtained from /auth/login endpoint",
        }
    }
    
    # Add security to protected endpoints
    protected_paths = ["/auth/refresh", "/auth/logout"]
    for path in protected_paths:
        if path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                if method in ["post", "get", "put", "delete", "patch"]:
                    if "security" not in openapi_schema["paths"][path][method]:
                        openapi_schema["paths"][path][method]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}

