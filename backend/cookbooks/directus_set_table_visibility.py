#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ## for jupyter debugging
# %cd ../../utilities
# import sys

# sys.path.append("..")

# import asyncio

# if (
#     asyncio.get_event_loop().is_running()
# ):  # Only patch if needed (i.e. running in Notebook, Spyder, etc)
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


import asyncio
import httpx
from typing import List


# # Project Utilities 🛰

# In[ ]:


from utilities.directus_utils import AsyncDirectusAPI
from utilities.utils import create_logger


# # Logging toolbox 🔊

# In[ ]:


try:
    logger = create_logger(Path(LOG_PATH), __file__, logging.getLogger(__name__))
except:
    logger = create_logger()


# # Cookbook part ✨

# In[ ]:


async def directus_set_table_visibility(
    access_token: str = os.getenv("DIRECTUS_ACCESS_TOKEN"),
    base_url: str
    | httpx.URL = os.getenv(
        "DIRECTUS_BASE_URL", "http://vanilla-essential-backend-directus:8055"
    ),
    ignored_collections: List[str] = [
        "directus_",
        "database_multipleselect",
        "database_relation",
        "database_table",
    ],
    timeout: int | httpx.Timeout = httpx.AsyncClient().timeout,
):
    try:
        aclient = AsyncDirectusAPI(
            access_token=access_token, base_url=base_url, timeout=timeout
        )
        await aclient.auth()
    except Exception as e:
        logger.error(e)
        raise e
    else:
        logger.info("Current user:", aclient.current_user)

    try:
        await aclient.set_collection_visibility(ignored_collections=ignored_collections)
    except Exception as e:
        logger.error(e)
        raise e
    else:
        logger.info("Set collection visibility successfully")


# In[ ]:


if __name__ == "__main__":
    asyncio.run(
        directus_set_table_visibility(
            access_token=os.getenv("DIRECTUS_ACCESS_TOKEN"),
            base_url=os.getenv("DIRECTUS_BASE_URL"),
            ignored_collections=[
                "directus_",
                "database_multipleselect",
                "database_relation",
                "database_table",
            ],
            timeout=60,
        )
    )


# In[ ]:
