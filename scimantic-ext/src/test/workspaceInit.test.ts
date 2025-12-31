import * as assert from "assert";
import * as path from "path";
import * as fs from "fs";
import * as os from "os";
import { initializeScimanticWorkspace } from "../extension";

suite("Workspace Initialization Test Suite", () => {
  let tempDir: string;

  setup(() => {
    // Create a temporary directory for each test
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "scimantic-test-"));
  });

  teardown(() => {
    // Clean up temporary directory after each test
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test("should create .mcp.json with correct configuration", async () => {
    await initializeScimanticWorkspace(tempDir);

    const mcpConfigPath = path.join(tempDir, ".mcp.json");
    assert.ok(fs.existsSync(mcpConfigPath), ".mcp.json should exist");

    const mcpConfig = JSON.parse(fs.readFileSync(mcpConfigPath, "utf-8"));
    assert.ok(mcpConfig.mcpServers, "should have mcpServers");
    assert.ok(mcpConfig.mcpServers.scimantic, "should have scimantic server");
    assert.strictEqual(
      mcpConfig.mcpServers.scimantic.command,
      "uv",
      "command should be uv",
    );
    assert.deepStrictEqual(
      mcpConfig.mcpServers.scimantic.args,
      ["run", "python", "-m", "scimantic.mcp"],
      "args should be correct",
    );
  });

  test("should create CLAUDE.md with research assistant instructions", async () => {
    await initializeScimanticWorkspace(tempDir);

    const claudeMdPath = path.join(tempDir, "CLAUDE.md");
    assert.ok(fs.existsSync(claudeMdPath), "CLAUDE.md should exist");

    const content = fs.readFileSync(claudeMdPath, "utf-8");
    assert.ok(
      content.includes("Scimantic Research Assistant"),
      "should have title",
    );
    assert.ok(
      content.includes("QuestionFormation"),
      "should reference QuestionFormation activity",
    );
    assert.ok(
      content.includes("add_question"),
      "should reference add_question MCP tool",
    );
    assert.ok(
      content.includes("PROV-O"),
      "should reference PROV-O provenance",
    );
  });

  test("should create claude/agents directory structure", async () => {
    await initializeScimanticWorkspace(tempDir);

    const agentsDir = path.join(tempDir, "claude", "agents");
    assert.ok(fs.existsSync(agentsDir), "claude/agents directory should exist");

    const stats = fs.statSync(agentsDir);
    assert.ok(stats.isDirectory(), "should be a directory");
  });

  test("should create question-formation.md agent", async () => {
    await initializeScimanticWorkspace(tempDir);

    const agentPath = path.join(tempDir, "claude", "agents", "question-formation.md");
    assert.ok(fs.existsSync(agentPath), "question-formation.md should exist");

    const content = fs.readFileSync(agentPath, "utf-8");
    assert.ok(
      content.includes("Question Formation Agent"),
      "should have agent title",
    );
    assert.ok(
      content.includes("scimantic:QuestionFormation"),
      "should reference ontology class",
    );
    assert.ok(
      content.includes("add_question"),
      "should reference MCP tool",
    );
    assert.ok(
      content.includes("Workflow"),
      "should have workflow section",
    );
  });

  test("should not overwrite existing .mcp.json", async () => {
    const mcpConfigPath = path.join(tempDir, ".mcp.json");
    const customConfig = { custom: "config" };
    fs.writeFileSync(mcpConfigPath, JSON.stringify(customConfig));

    await initializeScimanticWorkspace(tempDir);

    const content = JSON.parse(fs.readFileSync(mcpConfigPath, "utf-8"));
    assert.deepStrictEqual(
      content,
      customConfig,
      "should not overwrite existing config",
    );
  });

  test("should not overwrite existing CLAUDE.md", async () => {
    const claudeMdPath = path.join(tempDir, "CLAUDE.md");
    const customContent = "# Custom Claude.md";
    fs.writeFileSync(claudeMdPath, customContent);

    await initializeScimanticWorkspace(tempDir);

    const content = fs.readFileSync(claudeMdPath, "utf-8");
    assert.strictEqual(
      content,
      customContent,
      "should not overwrite existing CLAUDE.md",
    );
  });

  test("should not overwrite existing question-formation.md agent", async () => {
    const agentsDir = path.join(tempDir, "claude", "agents");
    fs.mkdirSync(agentsDir, { recursive: true });
    const agentPath = path.join(agentsDir, "question-formation.md");
    const customContent = "# Custom Agent";
    fs.writeFileSync(agentPath, customContent);

    await initializeScimanticWorkspace(tempDir);

    const content = fs.readFileSync(agentPath, "utf-8");
    assert.strictEqual(
      content,
      customContent,
      "should not overwrite existing agent",
    );
  });

  test("should create all files in a single invocation", async () => {
    await initializeScimanticWorkspace(tempDir);

    // Verify all expected files exist
    assert.ok(
      fs.existsSync(path.join(tempDir, ".mcp.json")),
      ".mcp.json should exist",
    );
    assert.ok(
      fs.existsSync(path.join(tempDir, "CLAUDE.md")),
      "CLAUDE.md should exist",
    );
    assert.ok(
      fs.existsSync(path.join(tempDir, "claude", "agents")),
      "agents directory should exist",
    );
    assert.ok(
      fs.existsSync(path.join(tempDir, "claude", "agents", "question-formation.md")),
      "question-formation.md should exist",
    );
  });

  test("should handle multiple calls idempotently", async () => {
    // First call
    await initializeScimanticWorkspace(tempDir);

    // Modify a file
    const mcpConfigPath = path.join(tempDir, ".mcp.json");
    const originalConfig = fs.readFileSync(mcpConfigPath, "utf-8");
    const modifiedConfig = { modified: true };
    fs.writeFileSync(mcpConfigPath, JSON.stringify(modifiedConfig));

    // Second call should not overwrite
    await initializeScimanticWorkspace(tempDir);

    const finalConfig = JSON.parse(fs.readFileSync(mcpConfigPath, "utf-8"));
    assert.deepStrictEqual(
      finalConfig,
      modifiedConfig,
      "should be idempotent",
    );
  });

  test(".mcp.json should have correct cwd relative to workspace root", async () => {
    await initializeScimanticWorkspace(tempDir);

    const mcpConfigPath = path.join(tempDir, ".mcp.json");
    const mcpConfig = JSON.parse(fs.readFileSync(mcpConfigPath, "utf-8"));

    const expectedCwd = path.join(tempDir, "scimantic-core");
    assert.strictEqual(
      mcpConfig.mcpServers.scimantic.cwd,
      expectedCwd,
      "cwd should be relative to workspace root",
    );
  });
});
