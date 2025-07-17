from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from server.agent.model import (
    ExecutorResult,
    HotspotsResult,
    IntentResult,
    PlanResult,
    SummaryResult,
)

hotspot_parser = JsonOutputParser(pydantic_object=HotspotsResult)

title_parser = StrOutputParser()

intent_parser = JsonOutputParser(pydantic_object=IntentResult)

plan_parser = JsonOutputParser(pydantic_object=PlanResult)

executor_parser = JsonOutputParser(pydantic_object=ExecutorResult)

summary_parser = JsonOutputParser(pydantic_object=SummaryResult)
