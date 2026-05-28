from langgraph.graph import StateGraph, END
from state import AgenticState
from agent_nodes import (
    oracle_node, test_generator_node, coder_node, 
    executor_node, critic_node, console
)

def route_execution(state: AgenticState):
    if state.get("execution_status") == "success":
        console.print("\n[bold green]🏁 PIPELINE COMPLETE. C++ Code is production-ready.[/bold green]")
        return "end"
    elif state.get("iteration_count", 0) >= 3:
        console.print("\n[bold red]❌ Max iterations reached. Killing graph.[/bold red]")
        return "end"
    else:
        console.print("\n[bold yellow]🔄 Routing to Critic for self-correction...[/bold yellow]")
        return "critic"

workflow = StateGraph(AgenticState)

workflow.add_node("oracle", oracle_node)
workflow.add_node("test_generator", test_generator_node)
workflow.add_node("coder", coder_node)
workflow.add_node("executor", executor_node)
workflow.add_node("critic", critic_node)

workflow.set_entry_point("oracle")
workflow.add_edge("oracle", "test_generator")
workflow.add_edge("test_generator", "coder")
workflow.add_edge("coder", "executor")
workflow.add_conditional_edges("executor", route_execution, {"end": END, "critic": "critic"})
workflow.add_edge("critic", "coder")

app = workflow.compile()