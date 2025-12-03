import uvicorn
from fastapi import APIRouter, FastAPI


def create_app():
    app = FastAPI()
    from router import router

    version_router = APIRouter()
    version_router.include_router(router, prefix="/spotify", tags=["spotify"])

    app.include_router(version_router, prefix="/api/v0")

    return app


def main():
    print("Hello from spotify-money-calculator!")
    uvicorn.run(
        "main:create_app",
        host="0.0.0.0",
        port=8888,
        factory=True,
        log_level="debug",
    )


if __name__ == "__main__":
    main()
