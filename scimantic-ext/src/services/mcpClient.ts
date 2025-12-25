import { GraphResponse } from "../types";
import * as childProcess from "child_process";
import * as path from "path";

/**
 * MCP Client for communicating with scimantic-core Python MCP server
 */
export class ScimanticMCPClient {
  private disposed: boolean = false;

  constructor() {
    // Constructor - initialize client
  }

  /**
   * Get the provenance graph from a project.ttl file
   *
   * @param projectPath Path to project.ttl file
   * @returns GraphResponse with evidence array
   */
  async getProvenanceGraph(projectPath: string): Promise<GraphResponse> {
    if (this.disposed) {
      throw new Error("MCP Client has been disposed");
    }

    if (!projectPath || projectPath.trim() === "") {
      throw new Error("Invalid project path");
    }

    try {
      // Call scimantic-core MCP server's get_provenance_graph_json function
      // For now, we'll use a direct Python subprocess call
      // TODO: Replace with proper MCP protocol communication
      const result = await this.callPythonMCPTool(projectPath);
      return result;
    } catch (error) {
      // Return empty graph on error for now
      console.error("Error getting provenance graph:", error);
      return { evidence: [] };
    }
  }

  /**
   * Call Python MCP tool directly using subprocess
   * Uses uv to ensure correct virtual environment
   */
  private async callPythonMCPTool(projectPath: string): Promise<GraphResponse> {
    return new Promise((resolve, reject) => {
      // Construct Python command to call the function directly
      // uv run will automatically activate the correct virtual environment
      const pythonCode = `
import json
from scimantic.mcp import get_provenance_graph_json

result = get_provenance_graph_json('${projectPath}')
print(result)
`;

      // Use 'uv run python' to ensure correct virtual environment
      // cwd is set to monorepo root so uv can find pyproject.toml
      const monorepoRoot = this.getMonorepoRoot();

      const python = childProcess.spawn(
        "uv",
        ["run", "python", "-c", pythonCode],
        {
          cwd: monorepoRoot,
        },
      );

      let stdout = "";
      let stderr = "";

      python.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      python.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      python.on("close", (code) => {
        if (code !== 0) {
          reject(
            new Error(`Python process exited with code ${code}: ${stderr}`),
          );
          return;
        }

        try {
          const result: GraphResponse = JSON.parse(stdout.trim());
          resolve(result);
        } catch (error) {
          reject(new Error(`Failed to parse JSON response: ${error}`));
        }
      });

      python.on("error", (error) => {
        reject(error);
      });
    });
  }

  /**
   * Get monorepo root directory
   * Needed for uv to find pyproject.toml and activate virtual environment
   */
  private getMonorepoRoot(): string {
    // Navigate from dist/ to monorepo root
    // When bundled, __dirname points to scimantic-ext/dist/
    return path.resolve(__dirname, "../..");
  }

  /**
   * Dispose of the client and clean up resources
   */
  dispose(): void {
    this.disposed = true;
  }
}
