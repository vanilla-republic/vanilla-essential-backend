## Path + Creadentials loading
from dotenv import load_dotenv
import os
from pathlib import Path

## Main Packages
from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
import orjson
import uvicorn

## project modules
from routers import parser_api
from utilities import utils

### loading credentials
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass
ENV_PATH = "."  ## for .py use; service-based .env
LOG_PATH = "./.logs/"  ## service-based .logs/
env_path = Path(ENV_PATH) / ".env"
load_dotenv(dotenv_path=env_path)

## Logging toolbox 🔊
logger = utils.create_logger(Path(LOG_PATH), __file__, logging.getLogger(__name__))


## init app
class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(parser_api.router)


## -------- start fastAPI --------
@app.get("/")
async def home():
    return {"repository": "https://github.com/vanilla-republic/vanilla-tooljet"}


if __name__ == "__main__":
    uvicorn.run(
        f"{__file__.replace('.py', '').rpartition('/')[-1]}:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
