# main installation: 
`$ pip install -U pip "pandas[performance, computation, excel, html, postgresql, mysql, sql-other]" jupyter httpx "black[jupyter]" "fastapi[all]" aioboto3 aioredis asyncpg`

# Pre-requisites
* "Directus" service is expected to be readily available
    * Bearer Token is also expected to be generated
* OpenAI API is expected to be readily available, if you would like to utilise its functionalities
* HuggingFace Token is expected to be readily available, if you would like to utilise its functionalities

# Features
* async-first APIs
* Directus-Auth compatible
* parse files (.xlsx, .csv) to JSON (API-ready)
* parse bytes (from .xlsx, .csv) to JSON (API-ready)

# Folder organization explained
* `utilites/` : pre-cooked ingredients for handy usages. all files in the folder will not cross-import between modules
* `cookbooks/` : combinations of utilites or anything within `backend/` folder. 1 cookbook will most-likely do only 1 thing
* `models/` : definitions of (pydantic) schemas. Useful for request validations
* `routers/` : API Endpoints to handle requests. They often utilise `models/`, `cookbooks/` and `utilites/` to correctly handle incoming requests
