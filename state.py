from typing import TypedDict, Optional
class AgenticState(TypedDict):
    problem_description: str
    test_cases: list[dict]
    current_code: str
    execution_status: Optional[str]
    execution_logs: Optional[str]
    critic_feedback: Optional[str]
    iteration_count: int
    oracle_code: Optional[str]