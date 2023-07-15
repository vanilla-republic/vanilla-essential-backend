#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional
import pathlib


# In[ ]:


def create_logger(
    log_parent_path: pathlib.PosixPath = None,
    log_file: str = None,
    logger: Optional[logging.Logger] = None,
) -> logging.Logger:
    """
    Return logger
    Example
    --------
    ```python
    >>> from utilities.utils import creat_logger
    >>> logger = creat_logger('<some parent path>', '<some file name>.log')
    ```
    """
    ### Logging toolbox 🔊
    if not logger:
        logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

    # verbose
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # set file handler
    if not log_file or not log_parent_path:
        logger.warning(
            "If either `log_parent_path` or `log_file` is/are not specified, no log file will be created. Only log streams are printed."
        )

    if log_file:
        log_parent_path = (
            log_parent_path
            if isinstance(log_parent_path, pathlib.PosixPath)
            else pathlib.Path(log_parent_path)
        )

    if log_file and log_parent_path:
        try:
            if not log_parent_path.exists():
                log_parent_path.mkdir()
            log_file = log_file.rpartition("/")[-1].rpartition(".")[0] + ".log"
        except:
            log_file = "fallback.log"

        log_file_path = log_parent_path / log_file
        ## Rotation
        log_handler = TimedRotatingFileHandler(
            log_file_path, when="midnight", backupCount=365
        )
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

    return logger
