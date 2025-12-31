import * as assert from "assert";
import * as vscode from "vscode";
import {
  KnowledgeGraphTreeProvider,
  EvidenceTreeItem,
  GroupItem,
  QuestionTreeItem,
  KnowledgeGraphItem,
} from "../providers/knowledgeGraphTreeProvider";
import { Evidence, Question } from "../types";

suite("KnowledgeGraphTreeProvider Test Suite", () => {
  test("Provider should be created successfully", () => {
    const provider = new KnowledgeGraphTreeProvider();
    assert.ok(provider, "Provider should be instantiated");
  });

  test("getTreeItem should return EvidenceTreeItem with correct label", () => {
    const provider = new KnowledgeGraphTreeProvider();
    const mockEvidence: Evidence = {
      uri: "http://example.org/evidence/001",
      content: "Test finding",
      citation: "Smith et al. (2023). Test Paper.",
      source: "https://doi.org/10.1234/test",
      timestamp: "2023-12-21T10:00:00Z",
      agent: "http://example.org/agent/test",
    };

    const treeItem = new EvidenceTreeItem(mockEvidence);
    const result = provider.getTreeItem(treeItem);

    assert.strictEqual(result.label, "Smith et al. (2023). Test Paper.");
    assert.strictEqual(result.description, "2023-12-21T10:00:00Z");
  });

  test("getChildren should return groups when empty", async () => {
    const provider = new KnowledgeGraphTreeProvider();
    const children = await provider.getChildren();

    assert.ok(Array.isArray(children), "Should return an array");
    assert.strictEqual(children.length, 2, "Should return 2 groups (Questions, Evidence)");
    assert.ok(children[0] instanceof GroupItem);
    assert.ok(children[1] instanceof GroupItem);
  });

  test("getChildren should return EvidenceTreeItems when in Evidence group", async () => {
    const provider = new KnowledgeGraphTreeProvider();
    const mockEvidence: Evidence[] = [
      {
        uri: "http://example.org/evidence/001",
        content: "Finding A",
        citation: "Author A (2023).",
        source: "https://doi.org/10.1234/a",
        timestamp: "2023-12-21T10:00:00Z",
        agent: "http://example.org/agent/test",
      },
      {
        uri: "http://example.org/evidence/002",
        content: "Finding B",
        citation: "Author B (2024).",
        source: "https://doi.org/10.1234/b",
        timestamp: "2024-01-15T14:30:00Z",
        agent: "http://example.org/agent/test",
      },
    ];

    // Set mock data
    provider.setData(mockEvidence, []);

    // Get root groups first
    const groups = await provider.getChildren();
    const evidenceGroup = groups.find(
      (g) => g instanceof GroupItem && g.type === "evidence",
    ) as GroupItem;

    // Get children of Evidence group
    const children = await provider.getChildren(evidenceGroup);

    assert.strictEqual(children.length, 2, "Should return 2 evidence items");
    assert.ok(
      children[0] instanceof EvidenceTreeItem,
      "Items should be EvidenceTreeItem instances",
    );
  });

  test("EvidenceTreeItem should have correct properties", () => {
    const mockEvidence: Evidence = {
      uri: "http://example.org/evidence/001",
      content: "Nanopublications are smallest publishable units.",
      citation: "Kuhn et al. (2016). Nanopubs.",
      source: "https://doi.org/10.7717/peerj-cs.78",
      timestamp: "2023-12-21T10:00:00Z",
      agent: "http://example.org/agent/claude",
    };

    const treeItem = new EvidenceTreeItem(mockEvidence);

    assert.strictEqual(treeItem.label, "Kuhn et al. (2016). Nanopubs.");
    assert.strictEqual(treeItem.description, "2023-12-21T10:00:00Z");
    assert.ok(treeItem.tooltip);
    const tooltipStr =
      typeof treeItem.tooltip === "string"
        ? treeItem.tooltip
        : treeItem.tooltip.value;
    assert.ok(
      tooltipStr.includes("Nanopublications are smallest publishable units."),
    );
    assert.ok(tooltipStr.includes("https://doi.org/10.7717/peerj-cs.78"));
    assert.strictEqual(
      treeItem.collapsibleState,
      vscode.TreeItemCollapsibleState.None,
    );
  });

  test("EvidenceTreeItem should have command to show details", () => {
    const mockEvidence: Evidence = {
      uri: "http://example.org/evidence/001",
      content: "Test content",
      citation: "Test citation",
      source: "https://doi.org/test",
      timestamp: "2023-12-21T10:00:00Z",
      agent: "http://example.org/agent/test",
    };

    const treeItem = new EvidenceTreeItem(mockEvidence);

    assert.ok(treeItem.command, "TreeItem should have a command");
    assert.strictEqual(treeItem.command.command, "scimantic.showEvidence");
    assert.strictEqual(treeItem.command.title, "Show Evidence Details");
    assert.deepStrictEqual(treeItem.command.arguments, [mockEvidence]);
  });

  test("refresh should fire onDidChangeTreeData event", (done) => {
    const provider = new KnowledgeGraphTreeProvider();

    // Subscribe to tree data change event
    provider.onDidChangeTreeData((_item: KnowledgeGraphItem | undefined) => {
      assert.strictEqual(
        _item,
        undefined,
        "Refresh should fire with undefined to refresh all",
      );
      done();
    });

    // Trigger refresh
    provider.refresh();
  });

  test("setData should trigger refresh", (done) => {
    const provider = new KnowledgeGraphTreeProvider();
    const mockEvidence: Evidence[] = [
      {
        uri: "http://example.org/evidence/001",
        content: "Test",
        citation: "Test (2023)",
        source: "https://doi.org/test",
        timestamp: "2023-12-21T10:00:00Z",
        agent: "http://example.org/agent/test",
      },
    ];

    // Subscribe to tree data change event
    provider.onDidChangeTreeData((_item: KnowledgeGraphItem | undefined) => {
      assert.strictEqual(_item, undefined);
      done();
    });

    // Set data should trigger refresh
    provider.setData(mockEvidence, []);
  });

  test("EvidenceTreeItem contextValue should be set for context menu", () => {
    const mockEvidence: Evidence = {
      uri: "http://example.org/evidence/001",
      content: "Test",
      citation: "Test citation",
      source: "https://doi.org/test",
      timestamp: "2023-12-21T10:00:00Z",
      agent: "http://example.org/agent/test",
    };

    const treeItem = new EvidenceTreeItem(mockEvidence);

    assert.strictEqual(treeItem.contextValue, "evidence");
  });

  test("EvidenceTreeItem should store evidence data", () => {
    const mockEvidence: Evidence = {
      uri: "http://example.org/evidence/001",
      content: "Test content",
      citation: "Test citation",
      source: "https://doi.org/test",
      timestamp: "2023-12-21T10:00:00Z",
      agent: "http://example.org/agent/test",
    };

    const treeItem = new EvidenceTreeItem(mockEvidence);

    assert.deepStrictEqual(treeItem.evidence, mockEvidence);
  });
});
