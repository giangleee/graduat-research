from pydantic import BaseModel


class KpiRequest(BaseModel):
    id: int
    name: str
    value: float
    symbol: str
