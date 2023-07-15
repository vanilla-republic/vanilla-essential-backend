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


import asyncio
import httpx
import json
import logging
import numpy as np
import pandas as pd
from typing import List


# # Project Utilities 🛰

# In[ ]:


from utilities.utils import create_logger


# # Logging toolbox 🔊

# In[ ]:


try:
    logger = create_logger(Path(LOG_PATH), __file__, logging.getLogger(__name__))
except:
    logger = create_logger()


# # Vanilla Tooljet Directus Utils ✨

# In[ ]:


class AsyncDirectusAPI(httpx.AsyncClient):
    """
    Asynchronous Directus API object

    Reference
    --------
    1. httpx.AsyncClient()

    Parameters
    --------
    access_token: Directus's access token
    base_url: Vanilla Directus's base URL
    email: Directus's email
    password: Directus's password
    timeout: timeout in seconds

    Example
    --------
    ```python
    >>> from utilities.directus_utils import AsyncDirectusAPI
    >>> aclient = AsyncDirectusAPI(os.getenv("DIRECTUS_ACCESS_TOKEN"))
    ```
    """

    def __init__(
        self,
        access_token: str = os.getenv("DIRECTUS_ACCESS_TOKEN"),
        base_url: str = os.getenv(
            "DIRECTUS_BASE_URL", "http://vanilla-tooljet-directus:8055"
        ),
        email: str = os.getenv("DIRECTUS_EMAIL"),
        password: str = os.getenv("DIRECTUS_PASSWORD"),
        provider: str = "directus",
        timeout: int = 10,
    ):
        ## inherit from super class
        super().__init__()

        self.access_token = access_token
        self.base_url = httpx.URL(base_url.strip().strip("/"))
        self.current_user = None
        self.email = email
        self.headers = {"Content-Type": "application/json"}
        self.password = password
        self.provider = provider
        self.timeout = timeout
        self.__logged_in = False

        try:
            assert self.access_token or (self.email and self.password)
        except AssertionError as e:
            raise AssertionError(
                f"Please provide either `access_token` or `email` and `password`"
            )

    async def __first_auth(self, otp: str = None):
        """
        First authentication to get access token
        """
        ## server to server authentication
        if self.access_token:
            url = self.base_url.join("users/me")
            headers = dict(self.headers) | {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = await self.get(url, headers=headers, timeout=self.timeout)
        ## user authentication
        else:
            url = self.base_url.join("auth/login")
            data = {"email": self.email, "password": self.password, "otp": otp}
            response = await self.post(url, json=data, timeout=self.timeout)
            if response.status_code == 200:
                self.access_token = response.json().get("data")["access_token"]
                self.refresh_token = response.json().get("data")["refresh_token"]

        ## raise error if authentication fails
        response.raise_for_status()

        ## if success, update login parameters
        self.__logged_in = True
        self.current_user = response.json().get("data")
        self.headers = dict(self.headers) | {
            "Authorization": f"Bearer {self.access_token}"
        }

    async def __refresh_token(self):
        """
        Refresh token
        """
        ## check if refresh token exists
        assert hasattr(self, "refresh_token")

        url = self.base_url.join("auth/refresh")
        data = {"refresh_token": self.refresh_token}
        headers = self.default_headers
        response = await self.post(
            url, json=data, headers=headers, timeout=self.timeout
        )
        if response.status_code == 200:
            self.access_token = response.json()["data"]["access_token"]
            self.refresh_token = response.json()["data"]["refresh_token"]

        ## raise error if authentication fails
        response.raise_for_status()

        ## if success, update login parameters
        self.headers = dict(self.headers) | {
            "Authorization": f"Bearer {self.access_token}"
        }

    async def auth(self, otp: str = None):
        """
        Main authentication function. Authenticates if not logged in, refreshes token if logged in.

        if successful, `access_token` will be stored as Bearer in `self.headers`
        This helps later directus requests to be authenticated automatically

        Example
        ```python
        >>> from utilities.directus_utils import AsyncDirectusAPI
        >>> aclient = AsyncDirectusAPI(os.getenv("DIRECTUS_ACCESS_TOKEN"))
        >>> await aclient.auth()
        ```
        """
        ## if not logged in, first authenticate
        if not self.__logged_in:
            await self.__first_auth(otp=otp)

        ## if logged in, refresh token
        if hasattr(self, "refresh_token"):
            await self.__refresh_token()

    async def set_collection_visibility(
        self, ignored_collections: List[str] = ["directus_"], hidden: bool = False
    ):
        """
        Set collection visibilities in directus

        Example
        ```python
        >>> from utilities.directus_utils import AsyncDirectusAPI
        >>> aclient = AsyncDirectusAPI(os.getenv("DIRECTUS_ACCESS_TOKEN"))
        >>> await aclient.auth()
        >>> await aclient.set_collection_visibility()
        ```
        """
        df_collections_ = pd.json_normalize(
            (await self.get(self.base_url.join("/collections"))).json(), ["data"]
        )
        df_collections = df_collections_.loc[
            ~df_collections_.collection.str.contains("|".join(ignored_collections))
        ]
        tasks = []
        for col in df_collections.collection:
            task = asyncio.ensure_future(
                self.patch(
                    self.base_url.join(f"/collections/{col}"),
                    json={"meta": {"hidden": False}},
                )
            )
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return [r.json() for r in results]


# In[ ]:
