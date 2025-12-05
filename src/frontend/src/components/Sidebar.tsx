import React from 'react';

const Sidebar = () => {
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-4 flex flex-col gap-4">
      <div className="font-bold text-lg mb-2">Node Palette</div>
      <div className="text-sm text-gray-500 mb-4">Drag nodes to the canvas</div>

      <div
        className="p-3 border-2 border-stone-400 rounded cursor-move bg-white hover:bg-stone-50 transition-colors"
        onDragStart={(event) => onDragStart(event, 'LLMNode')}
        draggable
      >
        <div className="font-bold text-stone-700">LLM Node</div>
        <div className="text-xs text-gray-500">Calls an LLM model</div>
      </div>

      <div
        className="p-3 border-2 border-blue-400 rounded cursor-move bg-white hover:bg-blue-50 transition-colors"
        onDragStart={(event) => onDragStart(event, 'CodeNode')}
        draggable
      >
        <div className="font-bold text-blue-700">Code Node</div>
        <div className="text-xs text-gray-500">Executes Python code</div>
      </div>

      <div
        className="p-3 border-2 border-green-400 rounded cursor-move bg-white hover:bg-green-50 transition-colors"
        onDragStart={(event) => onDragStart(event, 'RAGNode')}
        draggable
      >
        <div className="font-bold text-green-700">RAG Node</div>
        <div className="text-xs text-gray-500">Retrieves documents</div>
      </div>
    </aside>
  );
};

export default Sidebar;
