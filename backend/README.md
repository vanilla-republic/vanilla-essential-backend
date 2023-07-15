# main installation: 
`$ pip install -U pip "pandas[performance, computation, excel, html, postgresql, mysql, sql-other]" jupyter httpx "black[jupyter]" "fastapi[all]"`

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