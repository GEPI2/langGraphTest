import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface GraphConfig {
  id: string;
  name: string;
  description?: string;
  nodes: NodeConfig[];
  edges: EdgeConfig[];
  metadata?: Record<string, any>;
}

export interface NodeConfig {
  id: string;
  type: 'LLMNode' | 'CodeNode' | 'RAGNode' | 'HumanNode';
  config: Record<string, any>;
  position?: { x: number; y: number };
}

export interface EdgeConfig {
  source: string;
  target: string;
  condition?: string;
}

export const graphService = {
  createGraph: async (config: GraphConfig) => {
    const response = await api.post('/graphs', config);
    return response.data;
  },

  getGraph: async (graphId: string) => {
    const response = await api.get(`/graphs/${graphId}`);
    return response.data;
  },

  executeGraph: async (graphId: string, input: Record<string, any>) => {
    const response = await api.post(`/graphs/${graphId}/execute`, { input });
    return response.data;
  },

  generateNodeCode: async (description: string) => {
    const response = await api.post('/nodes/generate', { description });
    return response.data;
  },
};
