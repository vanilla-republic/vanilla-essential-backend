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

import asyncio
import logging
import pandas as pd


# # Project Utilities 🛰

# In[ ]:


from utilities.utils import create_logger


# # Logging toolbox 🔊

# In[ ]:


try:
    logger = create_logger(Path(LOG_PATH), __file__, logging.getLogger(__name__))
except:
    logger = create_logger()


# # Vanilla Tooljet Convert Utils ✨

# In[ ]:
