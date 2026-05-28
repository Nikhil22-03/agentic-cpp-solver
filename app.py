import streamlit as st
from graph import app

st.set_page_config(page_title="Agentic Code Sandbox", page_icon="🚀", layout="wide")

st.title("🚀 Multi-Agent C++ Code Sandbox")
st.markdown("Write, containerize, and self-correct C++ algorithms dynamically.")

problem = st.text_area("Enter a LeetCode Problem:", height=150)

if st.button("Generate & Test Pipeline"):
    if not problem.strip():
        st.warning("Please enter a problem description.")
    else:
        initial_state = {
            "problem_description": problem,
            "test_cases": [],
            "current_code": "",
            "execution_status": None,
            "execution_logs": None,
            "critic_feedback": None,
            "iteration_count": 0,
            "oracle_code": None
        }

        with st.status("Initializing Autonomous Agents...", expanded=True) as status:
            with st.status("Initializing Autonomous Agents...", expanded=True) as status:
                for event in app.stream(initial_state):
                    for node_name, state_update in event.items():
                        st.write(f"**🟢 Active Node:** {node_name.upper()}")
                        
                        # Show the generated tests in the UI
                        if node_name == "test_generator" and "test_cases" in state_update:
                            if len(state_update["test_cases"]) > 0:
                                st.success(f"Generated {len(state_update['test_cases'])} mathematically verified test cases!")
                                with st.expander("View Test Suite"):
                                    st.json(state_update["test_cases"])
                            else:
                                st.error("🚨 CRASH: Test Generator or Oracle failed to produce valid tests.")

                        elif node_name == "coder" and "current_code" in state_update:
                            with st.expander("View Generated C++ Code"):
                                st.code(state_update["current_code"], language="cpp")
                            
                        elif node_name == "critic" and "critic_feedback" in state_update:
                            st.markdown(f"**Critic Feedback:**\n{state_update['critic_feedback']}")
                            
                        elif node_name == "executor":
                            if state_update.get("execution_status") == "success":
                                st.success("All test cases passed inside Docker! 🎉")
                            else:
                                st.error(f"Sandbox Error: {state_update.get('execution_status')}")
                                st.code(state_update.get('execution_logs', ''))
                            
            status.update(label="Pipeline Execution Complete", state="complete", expanded=False)
                            
            status.update(label="Pipeline Execution Complete", state="complete", expanded=False)