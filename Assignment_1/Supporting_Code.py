"""
Assignment 1: Supporting Code
==============================
A professional-grade implementation of a ReAct (Reason + Act) agent loop.
This code demonstrates the 'agent loop' architecture analyzed in the report.

Author: Armaan Samir Jena, Intern, Ada Lovelace Software Pvt. Ltd.
Mentor: Dr Rakesh L, Director, Ada Lovelace Software Pvt. Ltd.
Organization: Ada Lovelace Software Pvt. Ltd.
Purpose: Demonstration for Technical Report
"""

import re
import os
import json
from typing import Dict, Any, Optional

# --- 1. Tool Definitions ---

def get_exchange_rate(pair: str) -> str:
    """Mock tool: Fetches exchange rates relative to INR."""
    rates = {"INR/USD": 0.012, "INR/EUR": 0.011, "INR/GBP": 0.0094}
    return str(rates.get(pair.upper(), "Error: Pair not found."))

def web_search(query: str) -> str:
    """Mock tool: Simulates a web search."""
    results = {
        "claude computer use": "A new beta feature from Anthropic allowing Claude to use computers like humans do.",
        "devin ai": "An autonomous AI software engineer by Cognition AI.",
        "peas framework": "Performance Measure (P), Environment (E), Actuators (A), Sensors (S)."
    }
    for k, v in results.items():
        if k in query.lower():
            return v
    return "No relevant search results found."

TOOLS = {
    "get_exchange_rate": get_exchange_rate,
    "web_search": web_search,
}

# --- 2. System Architecture ---

SYSTEM_PROMPT = """You are an Advanced Reasoning Agent.
For every task, you must follow the ReAct loop:
1. Thought: Analysis of the current state and deciding the next step.
2. Action: Call a specific tool (format: tool_name("arg")). 
3. Observation: The factual outcome provided by the environment.
4. Final Answer: The concise solution once sufficient data is gathered.

AVAILABLE TOOLS:
- get_exchange_rate(pair): Returns currency rate. Example: get_exchange_rate("INR/USD")
- web_search(query): Searches for technical facts.

WORKING EXAMPLE:
Thought: I need to find the current INR to USD rate to calculate the cost.
Action: get_exchange_rate("INR/USD")
Observation: 0.012
Thought: I now have the rate. I can calculate the final value.
Final Answer: The current exchange rate for INR to USD is 0.012.
"""

class ReActAgent:
    def __init__(self, model_name: str = "claude-3-5-sonnet"):
        self.model_name = model_name
        self.history = []

    def _parse_output(self, text: str) -> Dict[str, Any]:
        """Parses the model's text for Action or Final Answer."""
        action_match = re.search(r"Action:\s*(\w+)\((.+?)\)", text)
        final_match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)
        
        if final_match:
            return {"type": "final", "content": final_match.group(1).strip()}
        if action_match:
            return {
                "type": "action",
                "tool": action_match.group(1),
                "arg": action_match.group(2).strip("'\"")
            }
        return {"type": "none", "content": text}

    def solve(self, task: str, max_iterations: int = 5):
        print(f"\n[TASK]: {task}")
        self.history.append({"role": "user", "content": task})
        
        for i in range(max_iterations):
            # In a real scenario, this would call an LLM API.
            # Here we simulate the agent loop iterations.
            if i == 0:
                mock_llm_output = "Thought: I need to verify what the PEAS framework stands for.\nAction: web_search(\"PEAS framework\")"
            elif i == 1:
                mock_llm_output = "Thought: I have the definition. Now I can answer the user.\nFinal Answer: The PEAS framework stands for Performance Measure, Environment, Actuators, and Sensors."
            else:
                break
                
            print(f"\n>> Step {i+1} Reasoning:\n{mock_llm_output}")
            parsed = self._parse_output(mock_llm_output)
            
            if parsed["type"] == "final":
                print(f"\n[FINAL RESULT]: {parsed['content']}")
                return parsed["content"]
            
            if parsed["type"] == "action":
                tool_name = parsed["tool"]
                arg = parsed["arg"]
                if tool_name in TOOLS:
                    obs = TOOLS[tool_name](arg)
                    print(f"   -> Executing Tool: {tool_name}({arg})")
                    print(f"   -> Observation: {obs}")
                    self.history.append({"role": "assistant", "content": mock_llm_output})
                    self.history.append({"role": "user", "content": f"Observation: {obs}"})
                else:
                    print(f"   -> Error: Tool '{tool_name}' not found.")
                    break

# --- 3. Execution Simulation ---

if __name__ == "__main__":
    agent = ReActAgent()
    agent.solve("Explain the PEAS framework.")

"""
SAMPLE EXECUTION LOG:
----------------------
[TASK]: Explain the PEAS framework.

>> Step 1 Reasoning:
Thought: I need to verify what the PEAS framework stands for.
Action: web_search("PEAS framework")
   -> Executing Tool: web_search(PEAS framework)
   -> Observation: Performance Measure (P), Environment (E), Actuators (A), Sensors (S).

>> Step 2 Reasoning:
Thought: I have the definition. Now I can answer the user.
Final Answer: The PEAS framework stands for Performance Measure, Environment, Actuators, and Sensors.

[FINAL RESULT]: The PEAS framework stands for Performance Measure, Environment, Actuators, and Sensors.
"""
