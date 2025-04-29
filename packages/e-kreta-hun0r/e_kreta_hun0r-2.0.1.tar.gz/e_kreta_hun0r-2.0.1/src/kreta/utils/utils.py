from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal, Type, TypeVar, get_args, get_origin

from requests import Response

if TYPE_CHECKING:
    from pydantic import BaseModel

    from ..idp.auth_session import Auth_Session

T = TypeVar("T")


def request_category(
    url_start: str,
    session: Auth_Session,
    method: Literal["GET", "DELETE", "POST", "PUT"],
    url: str,
    *args,
    model: Type[T] = Response,
    **kwargs,
) -> T:
    url = url_start + url

    r = session.request(method, url, *args, **kwargs)

    if model is Response:
        return r

    data = r.json()

    origin = get_origin(model)
    if origin is list:
        inner_model: BaseModel = get_args(model)[0]
        return [inner_model.model_validate(item) for item in data]

    return model(data)


def filter_params(**kwargs) -> dict[str, Any]:
    return {
        k: (v.isoformat() if isinstance(v, datetime) else v)
        for k, v in kwargs.items()
        if v is not None
    }


def week_dates(date_in_first_week: datetime, weeks: int) -> tuple[datetime, datetime]:
    monday = date_in_first_week.date() - timedelta(days=date_in_first_week.weekday())
    sunday = monday + timedelta(days=6, weeks=weeks - 1)
    return monday, sunday
