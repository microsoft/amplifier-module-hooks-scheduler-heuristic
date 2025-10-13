"""Selection strategies for heuristic scheduler."""

import random
from typing import Any


class SelectionStrategy:
    """Base class for selection strategies."""

    def select_tool(self, available_tools: list[str], context: dict[str, Any]) -> str:
        """Select a tool from available options. Default to first available."""
        return available_tools[0] if available_tools else ""

    def select_agent(self, available_agents: list[str], task: str, context: dict[str, Any]) -> str:
        """Select an agent from available options. Default to first available."""
        return available_agents[0] if available_agents else ""


class FirstAvailableStrategy(SelectionStrategy):
    """Always select the first available option."""

    def select_tool(self, available_tools: list[str], context: dict[str, Any]) -> str:
        return available_tools[0]

    def select_agent(self, available_agents: list[str], task: str, context: dict[str, Any]) -> str:
        return available_agents[0]


class RoundRobinStrategy(SelectionStrategy):
    """Round-robin selection across options."""

    def __init__(self):
        self.tool_index = 0
        self.agent_index = 0

    def select_tool(self, available_tools: list[str], context: dict[str, Any]) -> str:
        selected = available_tools[self.tool_index % len(available_tools)]
        self.tool_index += 1
        return selected

    def select_agent(self, available_agents: list[str], task: str, context: dict[str, Any]) -> str:
        selected = available_agents[self.agent_index % len(available_agents)]
        self.agent_index += 1
        return selected


class RandomStrategy(SelectionStrategy):
    """Random selection with optional seed for reproducibility."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def select_tool(self, available_tools: list[str], context: dict[str, Any]) -> str:
        return self.rng.choice(available_tools)

    def select_agent(self, available_agents: list[str], task: str, context: dict[str, Any]) -> str:
        return self.rng.choice(available_agents)
