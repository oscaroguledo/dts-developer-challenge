from fastapi import FastAPI
from core.config import Settings
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from routes import task_router

from core.utils.response import Response, RequestValidationError 
from models import engine_db1 ,Base,create_tables

app = FastAPI()
settings = Settings()


# Add CORS middleware if configured
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

        
# Include the routers
app.include_router(task_router, prefix='/api/v1')

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the HMCTS Caseworker Task Management API Solution",
        "version": "1.0.0",
        "description": "This API allows you to create, view, update, and delete tasks efficiently.",
        "endpoints": {
            "GET /tasks/": "List all tasks",
            "POST /tasks/": "Create a new task",
            "GET /tasks/{task_id}": "Get details of a task by ID",
            "PUT /tasks/{task_id}/status": "Update status of a task",
            "DELETE /tasks/{task_id}": "Delete a task by ID"
        },
        "documentation_url": "/docs"
    }


# Handle validation errors globally
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        e = {}
        e['type'] = error['type']
        e['loc'] = error['loc']
        e['msg'] = error['msg']
        if 'ctx' in error.keys():
            err = error['ctx']
            if 'error' in err.keys():
                e['ctx'] = err['error']
            else:
                e['ctx'] = err

        errors.append(e)
    errors = errors[0] if len(errors) == 1 else errors

    return Response(message=errors, success=False, code=422)

@app.on_event("startup")
async def startup():
    await create_tables()    

