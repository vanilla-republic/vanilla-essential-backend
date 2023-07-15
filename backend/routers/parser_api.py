## paths and credentials related
import os
from pathlib import Path
from dotenv import load_dotenv

try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass
ENV_PATH = "."  ## for .py use; service-based .env
LOG_PATH = "./.logs/"  ## service-based .logs/
CRED_PATH = "./.credentials"  ## service-based .credentials/
env_path = Path(ENV_PATH) / ".env"
load_dotenv(dotenv_path=env_path)

## main packages
from fastapi import APIRouter, Body, Depends, File, Query, Request, UploadFile, status
from fastapi.exceptions import HTTPException
import logging
import orjson
from typing import Annotated


## project modules
from dependencies import aget_directus_curret_user
from cookbooks.convert_uploaded_file_to_json import convert_uploaded_file_to_json
from models.convert_model import JSONOrient, PandasReadFuntions
from utilities import utils

## Logging toolbox 🔊
logger = utils.create_logger(LOG_PATH, __file__, logging.getLogger(__name__))

router = APIRouter(
    prefix="/parser-api",
    tags=["parser-api"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(aget_directus_curret_user)],
)


## Helper fuctions
async def parse_body(request: Request):
    data: bytes = await request.body()
    return data


## Endpoints
@router.post("/file-to-json", status_code=200)
async def parse_file(
    request: Request,
    file: UploadFile = File(...),
    orient: JSONOrient = Query("records"),
    pandas_read_function: Annotated[
        PandasReadFuntions | None,
        Query(description="pandas read function; see API schema"),
    ] = None,
):
    """
    Convert uploaded file to json.
    """
    query_params_ = dict(request.query_params)
    query_params = {
        k: v
        for k, v in query_params_.items()
        if k not in ["orient", "pandas_read_function"]
    }
    try:
        ## Check if file is supported
        if not pandas_read_function:
            if file.filename.endswith(".csv"):
                pandas_read_function = "read_csv"

            elif file.filename.endswith((".xlsx", ".xls")):
                pandas_read_function = "read_excel"

            elif file.filename.endswith(".html"):
                pandas_read_function = "read_html"

            elif file.filename.endswith(".json"):
                pandas_read_function = "read_json"

            else:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail="File extension unrecognized. Please specify pandas_read_function.",
                )

        # Convert file to json
        dct_output = convert_uploaded_file_to_json(
            file.file.read(), orient, pandas_read_function, **query_params
        )

        return dct_output

    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


## Endpoints
@router.post("/byte-to-json", status_code=200)
async def parse_byte(
    request: Request,
    data: bytes = Depends(parse_body),
    orient: JSONOrient = Query("records"),
    pandas_read_function: Annotated[
        PandasReadFuntions,
        Query(description="pandas read function; see API schema"),
    ] = "read_excel",
):
    """
    Convert uploaded file to json.
    """
    query_params_ = dict(request.query_params)
    query_params = {
        k: v
        for k, v in query_params_.items()
        if k not in ["orient", "pandas_read_function"]
    }
    try:
        # Convert byte to json
        dct_output = convert_uploaded_file_to_json(
            data, orient, pandas_read_function, **query_params
        )

        return dct_output

    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
