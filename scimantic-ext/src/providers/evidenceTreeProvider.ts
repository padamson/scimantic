import * as vscode from "vscode";
import { Evidence } from "../types";

/**
 * Tree item representing an Evidence entity from the knowledge graph
 */
export class EvidenceTreeItem extends vscode.TreeItem {
  public readonly evidence: Evidence;

  constructor(evidence: Evidence) {
    super(evidence.citation, vscode.TreeItemCollapsibleState.None);

    this.evidence = evidence;
    this.description = evidence.timestamp;
    this.tooltip = this.createTooltip(evidence);
    this.contextValue = "evidence";

    // Command to show evidence details when clicked
    this.command = {
      command: "scimantic.showEvidence",
      title: "Show Evidence Details",
      arguments: [evidence],
    };
  }

  private createTooltip(evidence: Evidence): string {
    return `${evidence.content}\n\nSource: ${evidence.source}\nAgent: ${evidence.agent}`;
  }
}

/**
 * Tree data provider for Evidence entities in the knowledge graph
 */
export class EvidenceTreeDataProvider
  implements vscode.TreeDataProvider<EvidenceTreeItem>
{
  private _onDidChangeTreeData: vscode.EventEmitter<
    EvidenceTreeItem | undefined
  > = new vscode.EventEmitter<EvidenceTreeItem | undefined>();
  readonly onDidChangeTreeData: vscode.Event<EvidenceTreeItem | undefined> =
    this._onDidChangeTreeData.event;

  private evidence: Evidence[] = [];

  /**
   * Get tree item representation
   */
  getTreeItem(element: EvidenceTreeItem): vscode.TreeItem {
    return element;
  }

  /**
   * Get children (evidence items)
   */
  async getChildren(element?: EvidenceTreeItem): Promise<EvidenceTreeItem[]> {
    // No hierarchical structure - just return evidence items
    if (element) {
      return [];
    }

    return this.evidence.map((e) => new EvidenceTreeItem(e));
  }

  /**
   * Set evidence data and refresh tree view
   */
  setEvidence(evidence: Evidence[]): void {
    this.evidence = evidence;
    this.refresh();
  }

  /**
   * Refresh the tree view
   */
  refresh(): void {
    this._onDidChangeTreeData.fire(undefined);
  }
}
