from pydantic import BaseModel
from typing import List


class EffectEnvPoint(BaseModel):
    kpi_id: int
    point: float


class KpiRequest(BaseModel):
    id: int
    name: str
    value: float
    symbol: str


class KpiCondition(BaseModel):
    id: int
    pre_condition: List[int]
    post_condition: List[int]


class Employees(BaseModel):
    id: int
    name: str
    point: float


class Environments(BaseModel):
    id: int
    name: str
    effect_point: List[EffectEnvPoint]


class KpiOutput(BaseModel):
    id: int
    name: str
    effect_point: List[EffectEnvPoint]


class Equipment(BaseModel):
    id: int
    name: str
    effect_point: List[EffectEnvPoint]
