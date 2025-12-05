import React, { useCallback, useRef, useState } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Controls,
  Background,
  MiniMap,
  Node,
} from 'reactflow';
import 'reactflow/dist/style.css';

import Sidebar from './Sidebar';
import { useGraphStore } from '../store/graphStore';
import LLMNode from './nodes/LLMNode';
import CodeNode from './nodes/CodeNode';
import { graphService } from '../services/api';
import { Play, Save, Loader2 } from 'lucide-react';

const nodeTypes = {
  LLMNode: LLMNode,
  CodeNode: CodeNode,
  // RAGNode: RAGNode, // Placeholder
};

const GraphEditor = () => {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [isRunning, setIsRunning] = useState(false);

  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    addNode,
    toGraphConfig,
  } = useGraphStore();

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');

      // check if the dropped element is valid
      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode: Node = {
        id: `${type}_${Math.random().toString(36).substr(2, 9)}`,
        type,
        position,
        data: { label: `${type} node` },
      };

      addNode(newNode);
    },
    [reactFlowInstance, addNode]
  );

  const handleSave = async () => {
    const config = toGraphConfig();
    try {
      await graphService.createGraph(config);
      alert('Graph saved successfully!');
    } catch (error) {
      console.error('Failed to save graph', error);
      alert('Failed to save graph');
    }
  };

  const handleRun = async () => {
    const config = toGraphConfig();
    setIsRunning(true);
    try {
      // First save/update the graph
      await graphService.createGraph(config);
      
      // Then execute
      const result = await graphService.executeGraph(config.id, { messages: [] });
      console.log("Execution Result:", result);
      alert(`Execution successful! Result: ${JSON.stringify(result, null, 2)}`);
    } catch (error) {
      console.error('Failed to execute graph', error);
      alert('Failed to execute graph');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="dndflow w-full h-screen flex flex-col">
      <header className="h-14 border-b border-gray-200 flex items-center justify-between px-4 bg-white z-10">
        <div className="font-bold text-xl">Dynamic LangGraph Builder</div>
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded text-sm font-medium transition-colors"
          >
            <Save size={16} />
            Save
          </button>
          <button
            onClick={handleRun}
            disabled={isRunning}
            className="flex items-center gap-2 px-3 py-1.5 bg-green-500 hover:bg-green-600 text-white rounded text-sm font-medium transition-colors disabled:opacity-50"
          >
            {isRunning ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
            Run
          </button>
        </div>
      </header>
      
      <div className="flex-1 flex overflow-hidden">
        <ReactFlowProvider>
          <Sidebar />
          <div className="flex-1 h-full" ref={reactFlowWrapper}>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onInit={setReactFlowInstance}
              onDrop={onDrop}
              onDragOver={onDragOver}
              nodeTypes={nodeTypes}
              fitView
            >
              <Controls />
              <MiniMap />
              <Background gap={12} size={1} />
            </ReactFlow>
          </div>
        </ReactFlowProvider>
      </div>
    </div>
  );
};

export default GraphEditor;
