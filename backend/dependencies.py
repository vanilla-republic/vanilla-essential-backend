## Path + Creadentials loading
from dotenv import load_dotenv
import os
from pathlib import Path

## Main Packages
from typing import Annotated
from fastapi import Security
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

## project modules
from utilities.directus_utils import AsyncDirectusAPI
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

## Dependencies
directus_auth = HTTPBearer()


async def aget_directus_curret_user(
    access_token: Annotated[HTTPAuthorizationCredentials, Security(directus_auth)]
):
    ## Check if the request was successful
    async with AsyncDirectusAPI(access_token=access_token.credentials) as aclient:
        await aclient.auth()

    ## Return the credentials inputted by the user
    yield access_token
