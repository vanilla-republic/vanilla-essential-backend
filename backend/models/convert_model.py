from enum import Enum
from pydantic import BaseModel


class PandasReadFuntions(str, Enum):
    read_csv = "read_csv"
    read_excel = "read_excel"
    read_html = "read_html"
    read_json = "read_json"


class JSONOrient(str, Enum):
    # dict = "dict" ## not supported
    list = "list"
    # series = "series" ## not supported
    split = "split"
    tight = "tight"
    records = "records"
    # index = "index" ## not supported
