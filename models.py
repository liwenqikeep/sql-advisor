from pydantic import BaseModel, Field

class Suggestion(BaseModel):
    action: str = Field(description="建议动作，如：添加索引 (user_id)")
    reason: str = Field(description="依据，必须引用执行计划中的具体字段值")
    impact: str = Field(description="high / medium / low")

class SqlAnalysis(BaseModel):
    problems: list[str] = Field(description="发现的问题列表")
    table_scan: bool = Field(description="是否存在全表扫描")
    suggestions: list[Suggestion]
    summary: str = Field(description="一句话总结")