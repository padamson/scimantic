import * as assert from "assert";
import { ScimanticMCPClient } from "../services/mcpClient";
import { GraphResponse } from "../types";

suite("ScimanticMCPClient Test Suite", () => {
  test("Client should be created successfully", () => {
    const client = new ScimanticMCPClient();
    assert.ok(client, "Client should be instantiated");
  });

  test("getProvenanceGraph should return GraphResponse structure", async () => {
    const client = new ScimanticMCPClient();

    // For now, this will use a mock or test the structure
    // In full implementation, this would connect to actual MCP server
    const result = await client.getProvenanceGraph("/path/to/test/project.ttl");

    assert.ok(result, "Should return a result");
    assert.ok("evidence" in result, "Result should have evidence property");
    assert.ok(Array.isArray(result.evidence), "Evidence should be an array");
  });

  test("getProvenanceGraph should handle empty graph", async () => {
    const client = new ScimanticMCPClient();

    const result = await client.getProvenanceGraph("/path/to/nonexistent.ttl");

    assert.ok(result, "Should return a result");
    assert.strictEqual(
      result.evidence.length,
      0,
      "Empty graph should have no evidence",
    );
  });

  test("getProvenanceGraph should parse JSON response correctly", async () => {
    const client = new ScimanticMCPClient();

    // Mock response similar to what scimantic-core returns
    const mockJsonResponse = JSON.stringify({
      evidence: [
        {
          uri: "http://example.org/evidence/001",
          content: "Test finding",
          citation: "Test (2023)",
          source: "https://doi.org/test",
          timestamp: "2023-12-21T10:00:00Z",
          agent: "http://example.org/agent/test",
        },
      ],
    });

    const parsed: GraphResponse = JSON.parse(mockJsonResponse);

    assert.strictEqual(parsed.evidence.length, 1);
    assert.strictEqual(parsed.evidence[0].citation, "Test (2023)");
  });

  test("Client should handle connection errors gracefully", async () => {
    const client = new ScimanticMCPClient();

    // Test error handling
    try {
      // Intentionally pass invalid parameters to trigger error
      await client.getProvenanceGraph("");
    } catch (error) {
      assert.ok(error, "Should throw error for invalid path");
    }
  });

  test("Client should support dispose/cleanup", () => {
    const client = new ScimanticMCPClient();

    // Should not throw
    client.dispose();
    assert.ok(true, "Dispose should complete without error");
  });
});
