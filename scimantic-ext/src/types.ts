/**
 * Type definitions for Scimantic extension
 */

/**
 * Evidence entity from the knowledge graph
 */
export interface Evidence {
  uri: string;
  content: string;
  citation: string;
  source: string;
  timestamp: string;
  agent: string;
}

/**
 * Graph response from scimantic-core MCP server
 */
export interface GraphResponse {
  evidence: Evidence[];
}
