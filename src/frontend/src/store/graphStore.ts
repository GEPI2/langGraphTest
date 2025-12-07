import { create } from 'zustand';
import {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';
import { GraphConfig, NodeConfig, EdgeConfig } from '../services/api';

interface GraphState {
  nodes: Node[];
  edges: Edge[];
  graphId: string;
  graphName: string;
  
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: (connection: Connection) => void;
  addNode: (node: Node) => void;
  updateNodeData: (id: string, data: any) => void;
  
  // Serialization
  toGraphConfig: () => GraphConfig;
  loadGraphConfig: (config: GraphConfig) => void;
}

export const useGraphStore = create<GraphState>((set, get) => ({
  nodes: [
    {
      id: 'start-node',
      type: 'StartNode',
      position: { x: 100, y: 200 },
      data: { label: 'Start' },
    },
    {
      id: 'llm-node',
      type: 'LLMNode',
      position: { x: 400, y: 200 },
      data: { 
        label: 'LLM Node',
        model: 'gpt-4o',
        system_prompt: "You are a helpful assistant named Jarvis."
      },
    },
    {
      id: 'end-node',
      type: 'EndNode',
      position: { x: 700, y: 200 },
      data: { label: 'End' },
    },
  ],
  edges: [
    { id: 'e1', source: 'start-node', target: 'llm-node' },
    { id: 'e2', source: 'llm-node', target: 'end-node' },
  ],
  graphId: 'graph_' + Math.random().toString(36).substr(2, 9),
  graphName: 'Auto-Run Graph',

  onNodesChange: (changes: NodeChange[]) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
  },

  onEdgesChange: (changes: EdgeChange[]) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },

  onConnect: (connection: Connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
  },

  addNode: (node: Node) => {
    set({
      nodes: [...get().nodes, node],
    });
  },

  updateNodeData: (id: string, data: any) => {
    set({
      nodes: get().nodes.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: { ...node.data, ...data },
          };
        }
        return node;
      }),
    });
  },

  toGraphConfig: () => {
    const { nodes, edges, graphId, graphName } = get();
    
    const configNodes: NodeConfig[] = nodes.map((node) => ({
      id: node.id,
      type: node.type as any, // Assumes node.type matches NodeConfig type
      config: node.data,
      position: node.position,
    }));

    const configEdges: EdgeConfig[] = edges.map((edge) => ({
      source: edge.source,
      target: edge.target,
    }));

    return {
      id: graphId,
      name: graphName,
      nodes: configNodes,
      edges: configEdges,
    };
  },

  loadGraphConfig: (config: GraphConfig) => {
    const nodes: Node[] = config.nodes.map((node) => ({
      id: node.id,
      type: node.type,
      position: node.position || { x: 0, y: 0 },
      data: node.config,
    }));

    const edges: Edge[] = config.edges.map((edge) => ({
      id: `e${edge.source}-${edge.target}`,
      source: edge.source,
      target: edge.target,
    }));

    set({
      nodes,
      edges,
      graphId: config.id,
      graphName: config.name,
    });
  },
}));
