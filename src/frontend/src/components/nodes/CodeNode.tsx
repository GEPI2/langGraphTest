import { memo, useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { useGraphStore } from '../../store/graphStore';
import { graphService } from '../../services/api';
import { Wand2, Loader2 } from 'lucide-react';

const CodeNode = ({ id, data }: NodeProps) => {
  const updateNodeData = useGraphStore((state) => state.updateNodeData);
  const [isGenerating, setIsGenerating] = useState(false);
  const [description, setDescription] = useState('');

  const handleChange = (key: string, value: string) => {
    updateNodeData(id, { [key]: value });
  };

  const handleGenerate = async () => {
    if (!description) return;
    setIsGenerating(true);
    try {
      const result = await graphService.generateNodeCode(description);
      handleChange('code', result.code);
    } catch (error) {
      console.error("Failed to generate code", error);
      alert("Failed to generate code");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-blue-400 w-80">
      <div className="flex items-center justify-between mb-2">
        <div className="font-bold text-sm text-blue-600">Code Node</div>
      </div>
      
      <div className="flex flex-col gap-2">
        <div>
          <label className="text-xs text-gray-500">Description (for AI)</label>
          <div className="flex gap-1">
            <input
              className="nodrag flex-1 text-xs border rounded p-1"
              value={description}
              onChange={(evt) => setDescription(evt.target.value)}
              placeholder="Describe what this node should do..."
            />
            <button 
              onClick={handleGenerate}
              disabled={isGenerating}
              className="bg-blue-500 text-white p-1 rounded hover:bg-blue-600 disabled:bg-gray-300"
            >
              {isGenerating ? <Loader2 size={14} className="animate-spin"/> : <Wand2 size={14}/>}
            </button>
          </div>
        </div>

        <div>
          <label className="text-xs text-gray-500">Python Code</label>
          <textarea
            className="nodrag w-full text-xs border rounded p-1 h-32 font-mono bg-gray-50"
            value={data.code || ''}
            onChange={(evt) => handleChange('code', evt.target.value)}
            placeholder="def process(state): ..."
          />
        </div>
      </div>

      <Handle type="target" position={Position.Top} className="w-16 !bg-teal-500" />
      <Handle type="source" position={Position.Bottom} className="w-16 !bg-teal-500" />
    </div>
  );
};

export default memo(CodeNode);
