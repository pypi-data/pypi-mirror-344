from typing import Annotated, Any

from fastapi import Depends

from ...config import cache_config, db_config
from .utils import get_client_info, set_headers_no_client_cache

# HTTP dependencies
client_info = Annotated[
    dict[str, Any],
    Depends(get_client_info),
]
set_headers = Depends(set_headers_no_client_cache)

# Repos dependencies
redis = Annotated[
    cache_config.aioredis.Redis,
    Depends(cache_config.get_aioredis),
]
async_session = Annotated[
    db_config.AsyncSession,
    Depends(db_config.get_async_session),
]
