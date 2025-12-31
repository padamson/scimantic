import * as vscode from "vscode";
import { KnowledgeGraphTreeProvider } from "./providers/knowledgeGraphTreeProvider";
import { ScimanticMCPClient } from "./services/mcpClient";
import { Evidence } from "./types";
import * as path from "path";
import * as fs from "fs";

/**
 * Activate the Scimantic extension
 */
export function activate(context: vscode.ExtensionContext) {
  console.log("Scimantic extension is now active!");

  // Initialize MCP client
  const mcpClient = new ScimanticMCPClient();

  // Initialize Knowledge Graph tree view provider
  const knowledgeGraphProvider = new KnowledgeGraphTreeProvider();

  // Register tree view
  const treeView = vscode.window.createTreeView("scimanticKnowledgeGraph", {
    treeDataProvider: knowledgeGraphProvider,
    showCollapseAll: true,
  });

  // Register command: Refresh graph
  const refreshCommand = vscode.commands.registerCommand(
    "scimantic.refreshGraph",
    async () => {
      await loadAndRefreshGraph(knowledgeGraphProvider, mcpClient);
      vscode.window.showInformationMessage("Knowledge graph refreshed");
    },
  );

  // Register command: Show evidence details
  const showEvidenceCommand = vscode.commands.registerCommand(
    "scimantic.showEvidence",
    (evidence: Evidence) => {
      const panel = vscode.window.createWebviewPanel(
        "evidenceDetails",
        "Evidence Details",
        vscode.ViewColumn.One,
        {},
      );

      panel.webview.html = getEvidenceDetailsHtml(evidence);
    },
  );

  // Register command: Open source URL
  const openSourceCommand = vscode.commands.registerCommand(
    "scimantic.openSource",
    (sourceUrl: string) => {
      vscode.env.openExternal(vscode.Uri.parse(sourceUrl));
    },
  );

  // Check Claude Code MCP setup
  checkClaudeCodeSetup();

  // Register command: Setup Claude Code MCP
  const setupMcpCommand = vscode.commands.registerCommand(
    "scimantic.setupClaudeCodeMCP",
    async () => {
      await checkClaudeCodeSetup(true);
    },
  );

  // Load graph when extension activates
  loadAndRefreshGraph(knowledgeGraphProvider, mcpClient);

  // Watch for changes to project.ttl files
  const fileWatcher =
    vscode.workspace.createFileSystemWatcher("**/project.ttl");
  fileWatcher.onDidChange(() => {
    loadAndRefreshGraph(knowledgeGraphProvider, mcpClient);
  });
  fileWatcher.onDidCreate(() => {
    loadAndRefreshGraph(knowledgeGraphProvider, mcpClient);
  });

  // Add to subscriptions for cleanup
  context.subscriptions.push(
    treeView,
    refreshCommand,
    showEvidenceCommand,
    openSourceCommand,
    setupMcpCommand,
    fileWatcher,
    { dispose: () => mcpClient.dispose() },
  );
}

/**
 * Load evidence from project.ttl and refresh tree view
 */
async function loadAndRefreshGraph(
  provider: KnowledgeGraphTreeProvider,
  client: ScimanticMCPClient,
): Promise<void> {
  try {
    // Find project.ttl in workspace
    const projectPath = findProjectTtl();
    if (!projectPath) {
      provider.setData([], []);
      return;
    }

    // Get provenance graph from MCP server
    const graph = await client.getProvenanceGraph(projectPath);
    provider.setData(graph.evidence, graph.questions || []);
  } catch (error) {
    console.error("Error loading evidence:", error);
    provider.setData([], []);
  }
}

/**
 * Find project.ttl in workspace
 */
function findProjectTtl(): string | undefined {
  const workspaceFolders = vscode.workspace.workspaceFolders;
  if (!workspaceFolders) {
    return undefined;
  }

  // Check each workspace folder for project.ttl
  for (const folder of workspaceFolders) {
    const projectPath = path.join(folder.uri.fsPath, "project.ttl");
    if (fs.existsSync(projectPath)) {
      return projectPath;
    }

    // Also check examples/scimantic-paper/project.ttl
    const examplePath = path.join(
      folder.uri.fsPath,
      "examples",
      "scimantic-paper",
      "project.ttl",
    );
    if (fs.existsSync(examplePath)) {
      return examplePath;
    }
  }

  return undefined;
}

/**
 * Check if Claude Code MCP server is configured and prompt to set it up
 */
async function checkClaudeCodeSetup(force: boolean = false): Promise<void> {
  const workspaceFolders = vscode.workspace.workspaceFolders;
  if (!workspaceFolders) {
    return;
  }

  const workspaceRoot = workspaceFolders[0].uri.fsPath;
  const mcpConfigPath = path.join(workspaceRoot, ".mcp.json");
  const claudeMdPath = path.join(workspaceRoot, "CLAUDE.md");
  const agentsDir = path.join(workspaceRoot, "claude", "agents");

  // Check if already set up
  const isSetup =
    fs.existsSync(mcpConfigPath) &&
    fs.existsSync(claudeMdPath) &&
    fs.existsSync(agentsDir);

  // If config exists and not forcing, skip
  if (isSetup && !force) {
    return;
  }

  // Prompt user to set up
  const message = force
    ? "Initialize Scimantic research workspace for Claude Code?"
    : "Scimantic research workspace not initialized. Set it up?";

  const result = await vscode.window.showInformationMessage(
    message,
    "Setup Now",
    "Later",
  );

  if (result === "Setup Now") {
    try {
      await initializeScimanticWorkspace(workspaceRoot);
      vscode.window.showInformationMessage(
        "✓ Scimantic workspace initialized! Run 'claude' to start research chat or 'claude --agent question-formation' for guided workflows.",
      );
    } catch (error) {
      vscode.window.showErrorMessage(
        `Failed to initialize workspace: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
  }
}

/**
 * Initialize Scimantic research workspace
 * Exported for testing
 */
export async function initializeScimanticWorkspace(
  workspaceRoot: string,
): Promise<void> {
  // Create .mcp.json
  const mcpConfigPath = path.join(workspaceRoot, ".mcp.json");
  if (!fs.existsSync(mcpConfigPath)) {
    const mcpConfig = {
      mcpServers: {
        scimantic: {
          command: "uv",
          args: ["run", "python", "-m", "scimantic.mcp"],
          cwd: path.join(workspaceRoot, "scimantic-core"),
          env: {},
        },
      },
    };
    fs.writeFileSync(mcpConfigPath, JSON.stringify(mcpConfig, null, 2));
  }

  // Create CLAUDE.md
  const claudeMdPath = path.join(workspaceRoot, "CLAUDE.md");
  if (!fs.existsSync(claudeMdPath)) {
    fs.writeFileSync(claudeMdPath, generateClaudeMd());
  }

  // Create claude/agents directory
  const agentsDir = path.join(workspaceRoot, "claude", "agents");
  if (!fs.existsSync(agentsDir)) {
    fs.mkdirSync(agentsDir, { recursive: true });
  }

  // Create QuestionFormation agent
  const questionFormationPath = path.join(agentsDir, "question-formation.md");
  if (!fs.existsSync(questionFormationPath)) {
    fs.writeFileSync(questionFormationPath, generateQuestionFormationAgent());
  }
}

/**
 * Generate CLAUDE.md template for research workspace
 */
function generateClaudeMd(): string {
  return `# Scimantic Research Assistant

You are a research assistant specialized in **semantic scientific workflows**.

## Your Role

You help researchers build **machine-readable knowledge graphs** using the Scimantic framework:
- **RDF/OWL**: All research artifacts are semantic from inception
- **W3C PROV-O**: Mandatory provenance tracking for all activities
- **Scimantic Ontology**: Research entities and activities aligned with scientific method

## Scimantic Ontology Activities

Your workflows are aligned with PROV-O activities in the Scimantic ontology:

### QuestionFormation
Guides researchers in formulating research questions that drive evidence gathering.
- **Agent available**: \`claude --agent question-formation\`
- **MCP tool**: \`add_question\`

### EvidenceExtraction (Coming Soon)
Captures evidence from literature with full provenance metadata.
- **MCP tool**: \`add_evidence\`

### HypothesisFormation (Coming Soon)
Forms hypotheses from evidence with uncertainty quantification.
- **MCP tool**: \`mint_hypothesis\`

### DesignFormulation (Coming Soon)
Designs experiments to test hypotheses.
- **MCP tool**: \`mint_design\`

## Available MCP Tools

You have access to the **scimantic MCP server** with these tools:
- \`add_question\`: Add research question to knowledge graph
- \`add_evidence\`: Capture evidence with provenance
- \`mint_hypothesis\`: Form hypothesis from evidence
- \`mint_design\`: Create experiment design
- \`get_provenance_graph\`: Query the knowledge graph

## Core Principles

1. **Provenance is mandatory**: Every artifact must have PROV-O metadata
2. **Ontology-aligned**: Use Scimantic activity classes (QuestionFormation, etc.)
3. **Semantic-first**: RDF/OWL from inception, not retrofitted
4. **Always persist**: Use MCP tools to persist to knowledge graph
5. **Uncertainty explicit**: Annotate confidence and assumptions

## Research Workflow

**When helping with research:**
1. Understand the activity type (QuestionFormation, EvidenceExtraction, etc.)
2. Guide through the semantic capture process
3. Ensure all required metadata is present
4. Use MCP tools to persist with provenance
5. Confirm RDF persistence to \`project.ttl\`

**Example - Adding a research question:**
\`\`\`
User: "I want to track the question: How does basis set size affect DCS accuracy?"

You:
1. Identify activity: QuestionFormation
2. Extract question label
3. Call add_question MCP tool:
   {
     "label": "How does basis set size affect DCS accuracy?",
     "agent": "http://example.org/agent/researcher_001",
     "project_path": "project.ttl"
   }
4. Confirm: "✓ Question added with URI: http://example.org/research/question/abc123"
\`\`\`

## Important

- You are **actively building the semantic knowledge graph**, not just explaining workflows
- Always use MCP tools to persist data
- Validate completeness before confirming
- Link entities using PROV-O relationships

For specialized workflows, use the dedicated agents:
- \`claude --agent question-formation\`: Guided question formulation
- More agents coming as activities are implemented
`;
}

/**
 * Generate QuestionFormation agent template
 */
function generateQuestionFormationAgent(): string {
  return `# Question Formation Agent

You guide researchers through **formulating research questions** using the Scimantic QuestionFormation activity.

## Ontology Context

**Activity Class**: \`scimantic:QuestionFormation\`
**Generates**: \`scimantic:Question\` (Entity)
**Provenance**: Creates \`prov:Activity\` with \`prov:wasGeneratedBy\` link

## Workflow

1. **Understand context**: Ask about the research domain and current focus
2. **Identify gap**: What's unknown or needs investigation?
3. **Formulate question**: Collaboratively craft a clear, specific question
4. **Validate specificity**: Ensure question is answerable and measurable
5. **Persist to graph**: Use \`add_question\` MCP tool
6. **Confirm provenance**: Show URI and verify in knowledge graph

## Key Questions to Ask

- "What area of research are you focusing on?"
- "What specific aspect are you investigating?"
- "What would a good answer to this question look like?"
- "How would you measure or observe the answer?"
- "Is this question specific enough to guide evidence gathering?"

## Example Interaction

**User**: "I'm researching differential cross sections in electron-molecule collisions."

**You**: "Great! What specific aspect of DCS are you investigating?"

**User**: "I want to know if my computational method is accurate enough."

**You**: "Let's formulate a specific question. How about: 'How does basis set size affect DCS calculation accuracy for electron-H2O collisions?' Does that capture your research question?"

**User**: "Yes, that's it!"

**You**:
\`\`\`
Calling add_question MCP tool:
{
  "label": "How does basis set size affect DCS calculation accuracy for electron-H2O collisions?",
  "agent": "http://example.org/agent/researcher_001",
  "project_path": "project.ttl"
}

✓ Question added to knowledge graph!
URI: http://example.org/research/question/a1b2c3d4
Activity: QuestionFormation (http://example.org/research/question/a1b2c3d4/generation)

Next steps:
- Start gathering evidence related to this question
- Use 'add_evidence' with 'relates_to_question' parameter to link evidence
\`\`\`

## Validation Checklist

Before persisting, ensure:
- ✓ Question is specific and clear
- ✓ Question is answerable (not purely philosophical)
- ✓ Question guides evidence gathering
- ✓ Agent attribution is present
- ✓ Project path is correct

## Scimantic Principles

- **Semantic-first**: Question is RDF/OWL from creation
- **Provenance tracking**: QuestionFormation activity captures who/when/how
- **Knowledge graph integration**: Question becomes a queryable entity
- **Evidence linkage**: Future evidence can reference this question

Remember: You're not just recording questions, you're building a semantic research workflow!
`;
}

/**
 * Generate HTML for evidence details webview
 */
function getEvidenceDetailsHtml(evidence: Evidence): string {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Evidence Details</title>
	<style>
		body {
			font-family: var(--vscode-font-family);
			padding: 20px;
		}
		h1 {
			font-size: 18px;
			margin-bottom: 10px;
		}
		.section {
			margin-bottom: 20px;
		}
		.label {
			font-weight: bold;
			margin-bottom: 5px;
		}
		.content {
			margin-left: 10px;
			color: var(--vscode-foreground);
		}
		a {
			color: var(--vscode-textLink-foreground);
		}
		a:hover {
			color: var(--vscode-textLink-activeForeground);
		}
		.metadata {
			font-size: 12px;
			color: var(--vscode-descriptionForeground);
			margin-top: 20px;
			padding-top: 10px;
			border-top: 1px solid var(--vscode-panel-border);
		}
	</style>
</head>
<body>
	<h1>${escapeHtml(evidence.citation)}</h1>

	<div class="section">
		<div class="label">Content:</div>
		<div class="content">${escapeHtml(evidence.content)}</div>
	</div>

	<div class="section">
		<div class="label">Source:</div>
		<div class="content"><a href="${escapeHtml(evidence.source)}">${escapeHtml(evidence.source)}</a></div>
	</div>

	<div class="metadata">
		<div><strong>URI:</strong> ${escapeHtml(evidence.uri)}</div>
		<div><strong>Captured:</strong> ${escapeHtml(evidence.timestamp)}</div>
		<div><strong>Agent:</strong> ${escapeHtml(evidence.agent)}</div>
	</div>
</body>
</html>`;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text: string): string {
  const map: { [key: string]: string } = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

/**
 * Deactivate the extension
 */
export function deactivate() {
  // Cleanup handled by subscriptions
}
