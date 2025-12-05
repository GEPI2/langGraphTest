import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { useGraphStore } from '../../store/graphStore';

const LLMNode = ({ id, data }: NodeProps) => {
  const updateNodeData = useGraphStore((state) => state.updateNodeData);

  const handleChange = (key: string, value: string) => {
    updateNodeData(id, { [key]: value });
  };

  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-stone-400 w-64">
      <div className="flex items-center justify-between mb-2">
        <div className="font-bold text-sm text-stone-600">LLM Node</div>
      </div>
      
      <div className="flex flex-col gap-2">
        <div>
          <label className="text-xs text-gray-500">Model</label>
          <input
            className="nodrag w-full text-xs border rounded p-1"
            value={data.model || 'gemini-2.0-flash-exp'}
            onChange={(evt) => handleChange('model', evt.target.value)}
          />
        </div>
        <div>
          <label className="text-xs text-gray-500">System Prompt</label>
          <textarea
            className="nodrag w-full text-xs border rounded p-1 h-20"
            value={data.system_prompt || ''}
            onChange={(evt) => handleChange('system_prompt', evt.target.value)}
            placeholder="You are a helpful assistant..."
          />
        </div>
      </div>

      <Handle type="target" position={Position.Top} className="w-16 !bg-teal-500" />
      <Handle type="source" position={Position.Bottom} className="w-16 !bg-teal-500" />
    </div>
  );
};

export default memo(LLMNode);
