import uvicorn

from resc_backend.resc_web_service.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
