# Scimantic VS Code Extension

VS Code extension for visualizing semantic knowledge graphs and enabling Claude Code integration for research workflows.

## Features

- **Knowledge Graph Visualization**: Tree view of Evidence and Questions from `project.ttl`
- **Claude Code Integration**: Automatic workspace initialization with research assistant configuration
- **Ontology-Aligned Agents**: Specialized agents for research activities (QuestionFormation, EvidenceExtraction, etc.)
- **Real-time Updates**: Watches `project.ttl` for changes and updates visualization

## Prerequisites

- **Node.js**: v20 or higher
- **pnpm**: v9 or higher
- **VS Code**: v1.60.0 or higher

## Installation

```bash
cd scimantic-ext
pnpm install
```

## Development

### Running Tests

```bash
# Run all tests
pnpm test

# Run tests with coverage
pnpm run test:coverage

# Run type checking
pnpm run check-types

# Run linter
pnpm run lint
```

### Launching Extension Development Host

Press **F5** in VS Code to launch the Extension Development Host with the extension loaded.

The extension will:
1. Activate in the development workspace
2. Prompt to initialize Scimantic research workspace (if not already set up)
3. Create `.mcp.json`, `CLAUDE.md`, and `claude/agents/` directory
4. Display knowledge graph in the Scimantic sidebar

### Building

```bash
# Development build (with watch mode)
pnpm run watch

# Production build
pnpm run package
```

### Packaging for Distribution

```bash
# Create .vsix package
pnpm run package
```

The packaged extension will be created in the root directory as `scimantic-ext-*.vsix`.

## Architecture

```
scimantic-ext/
├── src/
│   ├── extension.ts              # Main activation logic
│   ├── providers/
│   │   └── knowledgeGraphTreeProvider.ts  # Tree view for RDF graph
│   ├── services/
│   │   └── mcpClient.ts          # MCP client for scimantic-core
│   ├── types.ts                  # TypeScript type definitions
│   └── test/                     # Test suites
└── package.json                  # Extension manifest
```

## Testing Strategy

Following TDD principles from [CLAUDE.md](../CLAUDE.md):

- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test component interactions (MCP client, providers)
- **Idempotency Tests**: Ensure workspace initialization is safe to run multiple times

All tests run automatically in CI/CD and pre-commit hooks.

## Commands

- `Scimantic: Refresh Knowledge Graph` - Manually refresh the graph view
- `Scimantic: Initialize Research Workspace` - Set up Claude Code integration

## Contributing

See the [monorepo README](../README.md) for overall project structure and contribution guidelines.

## Links

- [Scimantic Documentation](../docs/)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [MCP Specification](https://modelcontextprotocol.io/)
