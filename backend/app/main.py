from fastapi import FastAPI

app = FastAPI(
    title="RepoPilot AI",
    description="AI-powered GitHub repository understanding and engineering assistant",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "RepoPilot AI",
    }