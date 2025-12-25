import * as vscode from "vscode";
import { EvidenceTreeDataProvider } from "./providers/evidenceTreeProvider";
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

  // Initialize Evidence tree view provider
  const evidenceProvider = new EvidenceTreeDataProvider();

  // Register tree view
  const treeView = vscode.window.createTreeView("scimanticKnowledgeGraph", {
    treeDataProvider: evidenceProvider,
    showCollapseAll: true,
  });

  // Register command: Refresh graph
  const refreshCommand = vscode.commands.registerCommand(
    "scimantic.refreshGraph",
    async () => {
      await loadAndRefreshEvidence(evidenceProvider, mcpClient);
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

  // Load evidence when extension activates
  loadAndRefreshEvidence(evidenceProvider, mcpClient);

  // Watch for changes to project.ttl files
  const fileWatcher =
    vscode.workspace.createFileSystemWatcher("**/project.ttl");
  fileWatcher.onDidChange(() => {
    loadAndRefreshEvidence(evidenceProvider, mcpClient);
  });
  fileWatcher.onDidCreate(() => {
    loadAndRefreshEvidence(evidenceProvider, mcpClient);
  });

  // Add to subscriptions for cleanup
  context.subscriptions.push(
    treeView,
    refreshCommand,
    showEvidenceCommand,
    openSourceCommand,
    fileWatcher,
    { dispose: () => mcpClient.dispose() },
  );
}

/**
 * Load evidence from project.ttl and refresh tree view
 */
async function loadAndRefreshEvidence(
  provider: EvidenceTreeDataProvider,
  client: ScimanticMCPClient,
): Promise<void> {
  try {
    // Find project.ttl in workspace
    const projectPath = findProjectTtl();
    if (!projectPath) {
      provider.setEvidence([]);
      return;
    }

    // Get provenance graph from MCP server
    const graph = await client.getProvenanceGraph(projectPath);
    provider.setEvidence(graph.evidence);
  } catch (error) {
    console.error("Error loading evidence:", error);
    provider.setEvidence([]);
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
