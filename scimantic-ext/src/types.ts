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
 * Question entity from the knowledge graph
 */
export interface Question {
  uri: string;
  label: string;
  agent?: string;
}

/**
 * Graph response from scimantic-core MCP server
 */
export interface GraphResponse {
  evidence: Evidence[];
  questions: Question[];
}
