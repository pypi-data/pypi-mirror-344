from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

def main() -> None:
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Health Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    
if __name__ == "__main__":
    main()
