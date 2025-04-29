from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Literal, Optional

from ..utils.utils import filter_params, request_category, week_dates

# from .models import ()

if TYPE_CHECKING:
    from datetime import datetime

    from ..idp.auth_session import Auth_Session

mobile_request = partial(
    request_category,
    "https://kretadktapi.e-kreta.hu/dktapi/",
)
