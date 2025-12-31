import * as vscode from "vscode";
import { Evidence, Question } from "../types";

/**
 * Base class for all items in the Knowledge Graph tree
 */
export type KnowledgeGraphItem = GroupItem | EvidenceTreeItem | QuestionTreeItem;

/**
 * Tree item for top-level groups (Questions, Evidence)
 */
export class GroupItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly type: "questions" | "evidence",
  ) {
    super(label, vscode.TreeItemCollapsibleState.Collapsed);
    this.contextValue = "group";
  }
}

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
 * Tree item representing a Question entity
 */
export class QuestionTreeItem extends vscode.TreeItem {
  public readonly question: Question;

  constructor(question: Question) {
    super(question.label, vscode.TreeItemCollapsibleState.None);

    this.question = question;
    this.iconPath = new vscode.ThemeIcon("question");
    this.contextValue = "question";
    this.description = question.agent ? `(by ${question.agent})` : "";
  }
}

/**
 * Tree data provider for Knowledge Graph
 */
export class KnowledgeGraphTreeProvider
  implements vscode.TreeDataProvider<KnowledgeGraphItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<
    KnowledgeGraphItem | undefined
  > = new vscode.EventEmitter<KnowledgeGraphItem | undefined>();
  readonly onDidChangeTreeData: vscode.Event<KnowledgeGraphItem | undefined> =
    this._onDidChangeTreeData.event;

  private evidence: Evidence[] = [];
  private questions: Question[] = [];

  getTreeItem(element: KnowledgeGraphItem): vscode.TreeItem {
    return element;
  }

  async getChildren(element?: KnowledgeGraphItem): Promise<KnowledgeGraphItem[]> {
    if (!element) {
      // Root level: return groups
      return [
        new GroupItem(`Questions (${this.questions.length})`, "questions"),
        new GroupItem(`Evidence (${this.evidence.length})`, "evidence"),
      ];
    }

    if (element instanceof GroupItem) {
      if (element.type === "questions") {
        return this.questions.map((q) => new QuestionTreeItem(q));
      } else if (element.type === "evidence") {
        return this.evidence.map((e) => new EvidenceTreeItem(e));
      }
    }

    return [];
  }

  setData(evidence: Evidence[], questions: Question[]): void {
    this.evidence = evidence;
    this.questions = questions;
    this.refresh();
  }

  refresh(): void {
    this._onDidChangeTreeData.fire(undefined);
  }
}
