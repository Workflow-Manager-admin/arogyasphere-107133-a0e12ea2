from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React build static files (update the path as needed for your deployment)
frontend_build_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../arogyasphere-107133-919cee24/arogyamitr_frontend/build")
)
if os.path.exists(frontend_build_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")

@app.get("/")
def health_check():
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(full_path: str, request: Request):
    """
    Serves the React SPA for all non-API routes (fallback route).
    """
    index_path = os.path.join(frontend_build_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Frontend build not found"}, 404
