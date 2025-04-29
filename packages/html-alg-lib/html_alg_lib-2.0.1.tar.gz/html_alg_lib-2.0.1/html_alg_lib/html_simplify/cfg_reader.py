from functools import lru_cache

import commentjson as json


@lru_cache()
def read_cfg(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        cfg = json.load(f)
    return cfg
