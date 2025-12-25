# Scimantic

**Scimantic** is a comprehensive Python framework for orchestrating **Genuine Semantic Publishing (GSP)** research workflows.

It is designed to be driven by an external AI Agent via the **Model Context Protocol (MCP)**, allowing researchers to perform "Semantic First" science directly from their IDE.

## Features
*   **Headless Orchestration**: Define research steps as Python objects.
*   **Auto-Provenance**: Automatically generates W3C PROV-O RDF graphs for every execution.
*   **MCP Server**: Exposes an interface for AI agents to mint Hypotheses, Designs, and run experiments.
*   **Nanopublications**: First-class support for signing and publishing immutable assertions.

## Installation & Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run --extra dev pytest

# Run the CLI
uv run scimantic
```
