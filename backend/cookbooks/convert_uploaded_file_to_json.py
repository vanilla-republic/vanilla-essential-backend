#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ## for jupyter debugging
# %cd ../../utilities
# import sys
# sys.path.append('..')

# import asyncio
# if asyncio.get_event_loop().is_running(): # Only patch if needed (i.e. running in Notebook, Spyder, etc)
#     import nest_asyncio
#     nest_asyncio.apply()


# # Path + Creadentials loading 🧑🏻‍🚀

# In[ ]:


from dotenv import load_dotenv
import os
from pathlib import Path

### loading credentials
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

# CRED_PATH = "../.credentials"  ## .credentials folder is in service directory
# CRED_FILE = "directus_credentials.json"
ENV_PATH = ".."  ## .env file is in service directory
LOG_PATH = "../.logs"
env_path = Path(ENV_PATH) / ".env"
load_dotenv(dotenv_path=env_path)


# # Main Packages 🚀

# In[ ]:


from typing import List
import inspect
import logging
import pandas as pd


# # Project Utilities 🛰

# In[ ]:


from models.convert_model import JSONOrient, PandasReadFuntions
from utilities.utils import create_logger


# # Logging toolbox 🔊

# In[ ]:


try:
    logger = create_logger(Path(LOG_PATH), __file__, logging.getLogger(__name__))
except:
    logger = create_logger()


# # Cookbook part ✨

# In[ ]:


def convert_uploaded_file_to_json(
    io: str | bytes | Path,
    orient: JSONOrient = "records",
    pandas_read_function: PandasReadFuntions = "read_csv",
    **kwargs,
) -> dict | List[dict]:
    """
    Read the uploaded file into a Pandas DataFrame and convert it to JSON.
    """
    # Read file into a Pandas DataFrame
    assert pandas_read_function
    if pandas_read_function == "read_csv":
        func = pd.read_csv

    elif pandas_read_function == "read_excel":
        func = pd.read_excel

    elif pandas_read_function == "read_html":
        func = pd.read_html

    else:
        func = pd.read_json

    # pandas.read_x
    pd_read_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in inspect.signature(pd.read_excel).parameters
    }
    df = func(io, **pd_read_kwargs)

    # Convert the DataFrame to JSON
    dct_output = df.to_dict(orient=orient)
    return dct_output


# In[ ]:


# if __name__ == "__main__":
#     json_output = convert_uploaded_file_to_json()
