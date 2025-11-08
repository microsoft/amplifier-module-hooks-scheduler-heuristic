"""
Heuristic scheduler module for Amplifier.
Observes and can veto/modify tool selections.
"""

import logging
from typing import Any

from amplifier_core import HookResult
from amplifier_core import ModuleCoordinator

from .strategies import FirstAvailableStrategy
from .strategies import RandomStrategy
from .strategies import RoundRobinStrategy

logger = logging.getLogger(__name__)


async def mount(coordinator: ModuleCoordinator, config: dict[str, Any] | None = None):
    """
    Mount the heuristic scheduler module.

    Args:
        coordinator: Module coordinator
        config: Scheduler configuration

    Returns:
        Optional cleanup function
    """
    config = config or {}
    scheduler = HeuristicScheduler(config)
    await scheduler.register(coordinator)
    logger.info("Mounted HeuristicScheduler")
    return


class HeuristicScheduler:
    """
    Heuristic-based scheduler that observes tool selections.
    Can veto or modify selections based on configured strategy.
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize heuristic scheduler.

        Args:
            config: Scheduler configuration
        """
        self.config = config
        strategy_name = config.get("strategy", "first")
        seed = config.get("seed")

        # Whether to actively override selections (default: observe only)
        self.override_enabled = config.get("override_enabled", False)

        # Initialize selected strategy
        if strategy_name == "first":
            self.strategy = FirstAvailableStrategy()
        elif strategy_name == "round-robin":
            self.strategy = RoundRobinStrategy()
        elif strategy_name == "random":
            self.strategy = RandomStrategy(seed=seed)
        else:
            logger.warning(f"Unknown strategy '{strategy_name}', using 'first'")
            self.strategy = FirstAvailableStrategy()

        logger.info(f"HeuristicScheduler using strategy: {strategy_name}, override: {self.override_enabled}")

    async def register(self, coordinator: ModuleCoordinator):
        """Register hook handlers with the coordinator."""
        hooks = coordinator.get("hooks")
        if not hooks:
            logger.warning("No hook registry found in coordinator")
            return

        # Register for tool:selecting event (observe and optionally veto/modify)
        hooks.register(
            "tool:selecting",
            self.on_tool_selecting,
            priority=50,  # Medium priority
            name="heuristic:tool_selecting",
        )

        logger.debug("Registered heuristic scheduler handlers")

    async def on_tool_selecting(self, event: str, data: dict[str, Any]) -> HookResult:
        """
        Observe tool selection, optionally veto or modify.

        Args:
            event: Event name
            data: Contains tool_name, tool_input, available_tools

        Returns:
            HookResult with action (continue, deny, or modify)
        """
        tool_name = data.get("tool_name")
        available_tools = data.get("available_tools", [])

        # Log the LLM's selection
        logger.debug(f"Heuristic scheduler observing LLM selection: {tool_name}")

        # Check if tool is valid
        if tool_name not in available_tools:
            return HookResult(action="deny", reason=f"Tool {tool_name} not in available tools")

        # If override is not enabled, just observe
        if not self.override_enabled:
            return HookResult(action="continue")

        # Use strategy to determine what tool should be used
        context = {"llm_selection": tool_name}
        preferred_tool = self.strategy.select_tool(available_tools, context)

        # If strategy prefers a different tool, modify
        if preferred_tool != tool_name:
            logger.info(f"Heuristic scheduler overriding: {tool_name} → {preferred_tool}")
            return HookResult(
                action="modify",
                data={"tool_name": preferred_tool},
                reason=f"Strategy {self.strategy.__class__.__name__} prefers {preferred_tool}",
            )

        # Otherwise continue with LLM's selection
        return HookResult(action="continue")
