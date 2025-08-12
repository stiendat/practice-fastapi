import asyncio
import sys
from fastapi import FastAPI
import uvicorn
from src.api.main_router import router as main_router

app = FastAPI()
app.include_router(main_router)

if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="127.0.0.1", port=8000)