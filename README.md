# Amplifier Heuristic Scheduler Module

Simple heuristic-based scheduling for tool and agent selection in Amplifier.

## Prerequisites

- **Python 3.11+**
- **[UV](https://github.com/astral-sh/uv)** - Fast Python package manager

### Installing UV

```bash
# macOS/Linux/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Purpose

Provides basic scheduling strategies for event-driven orchestration:

- First-available selection
- Round-robin distribution
- Random selection with seed support

## Contract

**Module Type:** Hook
**Mount Point:** `hooks` registry
**Entry Point:** `amplifier_module_hooks_scheduler_heuristic:mount`

## Configuration

```toml
[[hooks]]
module = "hooks-scheduler-heuristic"
config = {
    strategy = "first"  # "first", "round-robin", or "random"
    seed = 42           # Optional: for reproducible random selection
}
```

## Behavior

Registers handlers for decision events:

- `decision:tool_resolution` - Select tool from available options
- `decision:agent_resolution` - Select agent for task delegation
- `decision:context_resolution` - Decide context compaction strategy

Returns `ToolResolutionResponse`, `AgentResolutionResponse`, or `ContextResolutionResponse` with:

- Selected option
- Score (0.0-1.0)
- Rationale explaining selection
- Metadata for observability

## Dependencies

- `amplifier-core>=1.0.0`

## Contributing

> [!NOTE]
> This project is not currently accepting external contributions, but we're actively working toward opening this up. We value community input and look forward to collaborating in the future. For now, feel free to fork and experiment!

Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
