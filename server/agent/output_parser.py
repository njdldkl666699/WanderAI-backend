from langchain_core.output_parsers import JsonOutputParser

from server.agent.model import (
    ExecutorResult,
    HotspotsResult,
    IntentResult,
    PlanResult,
    SummaryResult,
)

hotspot_parser = JsonOutputParser(pydantic_object=HotspotsResult)

intent_parser = JsonOutputParser(pydantic_object=IntentResult)

plan_parser = JsonOutputParser(pydantic_object=PlanResult)

executor_parser = JsonOutputParser(pydantic_object=ExecutorResult)

summary_parser = JsonOutputParser(pydantic_object=SummaryResult)
