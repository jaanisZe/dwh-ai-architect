import pandas as pd
from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


class QueryResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    question: str
    generated_sql: str
    execution_time_ms: float
    data: pd.DataFrame
