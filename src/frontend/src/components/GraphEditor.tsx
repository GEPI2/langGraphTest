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
import { Play, Save, Loader2, Settings } from 'lucide-react';
import { Button } from './ui/button';
// Actually, let's stick to standard alert for now to avoid missing dependency 'use-toast' which I haven't created yet.

import RAGNode from './nodes/RAGNode';
import StartNode from './nodes/StartNode';
import EndNode from './nodes/EndNode';
import ToolNode from './nodes/ToolNode';

const nodeTypes = {
  LLMNode: LLMNode,
  CodeNode: CodeNode,
  RAGNode: RAGNode,
  ToolNode: ToolNode,
  StartNode: StartNode,
  EndNode: EndNode,
};

const GraphEditor = () => {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [executionResult, setExecutionResult] = useState<string | null>(null);
  const hasAutoRun = useRef(false);

  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    addNode,
    toGraphConfig,
  } = useGraphStore();

  // Auto-run on initial load
  React.useEffect(() => {
    if (!hasAutoRun.current && nodes.length > 0) {
        console.log("Auto-running graph on init...");
        hasAutoRun.current = true;
        
        // Small delay to ensure ReactFlow is ready
        setTimeout(() => {
            handleRun("안녕하세요");
        }, 1000);
    }
  }, [nodes]);

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

  const runGraph = async (inputMessage?: string) => {
    const config = toGraphConfig();
    setIsRunning(true);
    setExecutionResult(null); // Clear previous result
    try {
      // First save/update the graph
      await graphService.createGraph(config);
      
      // Then execute
      const messageContent = inputMessage || "Hello";
      const payload = { messages: [{ role: "user", content: messageContent }] };
      
      console.log("Executing with payload:", payload);
      const result = await graphService.executeGraph(config.id, payload);
      console.log("Execution Result:", result);
      
      // Show result
      const lastMessage = result.messages && result.messages.length > 0 
        ? result.messages[result.messages.length - 1] 
        : null;
      
      const responseText = lastMessage 
        ? (typeof lastMessage.content === 'string' ? lastMessage.content : JSON.stringify(lastMessage.content, null, 2))
        : JSON.stringify(result, null, 2);

      setExecutionResult(responseText);
    } catch (error: any) {
      console.error('Failed to execute graph', error);
      setExecutionResult(`Error: ${error.message || 'Failed to execute graph'}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleRunClick = () => {
    runGraph();
  };

  // Auto-run on initial load
  React.useEffect(() => {
    if (!hasAutoRun.current && nodes.length > 0) {
        console.log("Auto-running graph on init...");
        hasAutoRun.current = true;
        
        // Small delay to ensure ReactFlow is ready
        setTimeout(() => {
            runGraph("안녕하세요");
        }, 1000);
    }
  }, [nodes]);

  return (
    <div className="dndflow w-full h-screen flex flex-col bg-background text-foreground">
      <header className="h-16 border-b flex items-center justify-between px-6 bg-card z-10 shadow-sm">
        <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Settings className="text-primary-foreground w-5 h-5" />
            </div>
            <div className="font-bold text-xl tracking-tight">Dynamic LangGraph Builder</div>
        </div>
        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={handleSave}
            className="gap-2"
          >
            <Save size={16} />
            Save
          </Button>
          <Button
            onClick={handleRunClick}
            disabled={isRunning}
            className="gap-2"
          >
            {isRunning ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
            Run
          </Button>
        </div>
      </header>
      
      <div className="flex-1 flex overflow-hidden">
        <ReactFlowProvider>
          <Sidebar />
          <div className="flex-1 h-full relative flex flex-col" ref={reactFlowWrapper}>
            <div className="flex-1 relative">
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
                className="bg-slate-50"
                >
                <Controls className="bg-white border-none shadow-md rounded-lg overflow-hidden" />
                <MiniMap className="border-none shadow-md rounded-lg overflow-hidden" />
                <Background gap={16} size={1} color="#e2e8f0" />
                </ReactFlow>
            </div>
            
            {/* Execution Result Panel */}
            {executionResult && (
                <div className="h-1/3 border-t bg-card p-4 overflow-auto shadow-inner z-20">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-lg">Execution Result</h3>
                        <Button 
                            variant="ghost" 
                            size="sm" 
                            onClick={() => setExecutionResult(null)}
                            className="h-8 w-8 p-0"
                        >
                            ✕
                        </Button>
                    </div>
                    <pre className="bg-muted p-4 rounded-md overflow-auto text-sm font-mono whitespace-pre-wrap">
                        {executionResult}
                    </pre>
                </div>
            )}
          </div>
        </ReactFlowProvider>
      </div>
    </div>
  );
};

export default GraphEditor;
